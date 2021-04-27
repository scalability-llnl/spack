% Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% This logic program implements Spack's concretizer
%=============================================================================

%-----------------------------------------------------------------------------
% Version semantics
%-----------------------------------------------------------------------------

% versions are declared w/priority -- declared with priority implies declared
version_declared(Package, Version) :- version_declared(Package, Version, _).

% If something is a package, it has only one version and that must be a
% declared version.
1 { version(Package, Version) : version_declared(Package, Version) } 1
 :- node(Package).

possible_version_weight(Package, Weight)
 :- version(Package, Version), version_declared(Package, Version, Weight),
    not preferred_version_declared(Package, Version, _).

possible_version_weight(Package, Weight)
  :- version(Package, Version), preferred_version_declared(Package, Version, Weight).

1 { version_weight(Package, Weight) : possible_version_weight(Package, Weight) } 1 :- node(Package).

% version_satisfies implies that exactly one of the satisfying versions
% is the package's version, and vice versa.
1 { version(Package, Version) : version_satisfies(Package, Constraint, Version) } 1
  :- version_satisfies(Package, Constraint).
version_satisfies(Package, Constraint)
  :- version(Package, Version), version_satisfies(Package, Constraint, Version).

#defined preferred_version_declared/3.
#defined version_satisfies/3.

%-----------------------------------------------------------------------------
% Spec conditions and imposed constraints
%
% Given Spack directives like these:
%    depends_on("foo@1.0+bar", when="@2.0+variant")
%    provides("mpi@2:", when="@1.9:")
%
% The conditions are `@2.0+variant` and `@1.9:`, and the imposed constraints
% are `@1.0+bar` on `foo` and `@2:` on `mpi`.
%-----------------------------------------------------------------------------
% conditions are specified with `condition_requirement` and hold when
% corresponding spec attributes hold.
condition_holds(ID) :-
  condition(ID);
  attr(Name, A1)         : condition_requirement(ID, Name, A1);
  attr(Name, A1, A2)     : condition_requirement(ID, Name, A1, A2);
  attr(Name, A1, A2, A3) : condition_requirement(ID, Name, A1, A2, A3).

% condition_holds(ID) implies all imposed_constraints, unless do_not_impose(ID)
% is derived. This allows imposed constraints to be canceled in special cases.
impose(ID) :- condition_holds(ID), not do_not_impose(ID).

% conditions that hold impose constraints on other specs
attr(Name, A1)         :- impose(ID), imposed_constraint(ID, Name, A1).
attr(Name, A1, A2)     :- impose(ID), imposed_constraint(ID, Name, A1, A2).
attr(Name, A1, A2, A3) :- impose(ID), imposed_constraint(ID, Name, A1, A2, A3).

#defined condition/1.
#defined condition_requirement/3.
#defined condition_requirement/4.
#defined condition_requirement/5.
#defined imposed_constraint/3.
#defined imposed_constraint/4.
#defined imposed_constraint/5.

%-----------------------------------------------------------------------------
% Dependency semantics
%-----------------------------------------------------------------------------
% Dependencies of any type imply that one package "depends on" another
depends_on(Package, Dependency) :- depends_on(Package, Dependency, _).

% a dependency holds if its condition holds
dependency_holds(Package, Dependency, Type) :-
  dependency_condition(ID, Package, Dependency),
  dependency_type(ID, Type),
  condition_holds(ID),
  not external(Package).

% We cut off dependencies of externals (as we don't really know them).
% Don't impose constraints on dependencies that don't exist.
do_not_impose(ID) :-
  not dependency_holds(Package, Dependency, _),
  dependency_condition(ID, Package, Dependency).

% declared dependencies are real if they're not virtual AND
% the package is not an external.
% They're only triggered if the associated dependnecy condition holds.
depends_on(Package, Dependency, Type)
 :- dependency_holds(Package, Dependency, Type),
    not virtual(Dependency).

% every root must be a node
node(Package) :- root(Package).

% dependencies imply new nodes
node(Dependency) :- node(Package), depends_on(Package, Dependency).

% all nodes in the graph must be reachable from some root
% this ensures a user can't say `zlib ^libiconv` (neither of which have any
% dependencies) and get a two-node unconnected graph
needed(Package) :- root(Package).
needed(Dependency) :- needed(Package), depends_on(Package, Dependency).
:- node(Package), not needed(Package).

% Avoid cycles in the DAG
% some combinations of conditional dependencies can result in cycles;
% this ensures that we solve around them
path(Parent, Child) :- depends_on(Parent, Child).
path(Parent, Descendant) :- path(Parent, A), depends_on(A, Descendant).
:- path(A, B), path(B, A).

#defined dependency_type/2.
#defined dependency_condition/3.

%-----------------------------------------------------------------------------
% Conflicts
%-----------------------------------------------------------------------------
:- node(Package),
   not external(Package),
   conflict(Package, TriggerID, ConstraintID),
   condition_holds(TriggerID),
   condition_holds(ConstraintID).

#defined conflict/3.

%-----------------------------------------------------------------------------
% Virtual dependencies
%-----------------------------------------------------------------------------

% if a package depends on a virtual, it's not external and we have a
% provider for that virtual then it depends on the provider
depends_on(Package, Provider, Type)
  :- dependency_holds(Package, Virtual, Type),
     provides_virtual(Provider, Virtual),
     not external(Package).

% dependencies on virtuals also imply that the virtual is a virtual node
virtual_node(Virtual)
  :- dependency_holds(Package, Virtual, Type),
     virtual(Virtual), not external(Package).

% if there's a virtual node, we must select one provider
1 { provides_virtual(Package, Virtual) : possible_provider(Package, Virtual) } 1
 :- virtual_node(Virtual).

% virtual roots imply virtual nodes, and that one provider is a root
virtual_node(Virtual) :- virtual_root(Virtual).
1 { root(Package) : provides_virtual(Package, Virtual) } 1
  :- virtual_root(Virtual).

% The provider provides the virtual if some provider condition holds.
provides_virtual(Provider, Virtual) :-
   provider_condition(ID, Provider, Virtual),
   condition_holds(ID),
   virtual(Virtual).

% a node that provides a virtual is a provider
provider(Package, Virtual)
  :- node(Package), provides_virtual(Package, Virtual).

% for any virtual, there can be at most one provider in the DAG
0 { node(Package) : provides_virtual(Package, Virtual) } 1 :- virtual(Virtual).

#defined possible_provider/2.

%-----------------------------------------------------------------------------
% Virtual dependency weights
%-----------------------------------------------------------------------------
% give dependents the virtuals they want
provider_weight(Dependency, 0)
 :- virtual(Virtual), depends_on(Package, Dependency),
    provider(Dependency, Virtual),
    external(Dependency).

provider_weight(Dependency, Weight)
 :- virtual(Virtual), depends_on(Package, Dependency),
    provider(Dependency, Virtual),
    pkg_provider_preference(Package, Virtual, Dependency, Weight),
    not external(Dependency).

provider_weight(Dependency, Weight)
 :- virtual(Virtual), depends_on(Package, Dependency),
    provider(Dependency, Virtual),
    not pkg_provider_preference(Package, Virtual, Dependency, _),
    not external(Dependency),
    default_provider_preference(Virtual, Dependency, Weight).

% if there's no preference for something, it costs 100 to discourage its
% use with minimization
provider_weight(Dependency, 100)
 :- virtual(Virtual),
    provider(Dependency, Virtual),
    depends_on(Package, Dependency),
    not external(Dependency),
    not pkg_provider_preference(Package, Virtual, Dependency, _),
    not default_provider_preference(Virtual, Dependency, _).

% Do the same for virtual roots
provider_weight(Package, Weight)
 :- virtual_root(Virtual),
    provider(Package, Virtual),
    default_provider_preference(Virtual, Package, Weight).

provider_weight(Package, 100)
 :- virtual_root(Virtual),
    provider(Package, Virtual),
    not default_provider_preference(Virtual, Package, _).

#defined possible_provider/2.
#defined provider_condition/3.
#defined required_provider_condition/3.
#defined required_provider_condition/4.
#defined required_provider_condition/5.

%-----------------------------------------------------------------------------
% Spec Attributes
%-----------------------------------------------------------------------------
% Equivalencies of the form:
%
%   name(Arg1, Arg2, ...) :- attr("name", Arg1, Arg2, ...).
%   attr("name", Arg1, Arg2, ...) :- name(Arg1, Arg2, ...).
%
% These allow us to easily define conditional dependency and conflict rules
% without enumerating all spec attributes every time.
node(Package)                          :- attr("node", Package).
version(Package, Version)              :- attr("version", Package, Version).
version_satisfies(Package, Constraint) :- attr("version_satisfies", Package, Constraint).
node_platform(Package, Platform)       :- attr("node_platform", Package, Platform).
node_os(Package, OS)                   :- attr("node_os", Package, OS).
node_target(Package, Target)           :- attr("node_target", Package, Target).
node_target_satisfies(Package, Target) :- attr("node_target_satisfies", Package, Target).
variant_value(Package, Variant, Value) :- attr("variant_value", Package, Variant, Value).
variant_set(Package, Variant, Value)   :- attr("variant_set", Package, Variant, Value).
node_flag(Package, FlagType, Flag)     :- attr("node_flag", Package, FlagType, Flag).
node_compiler(Package, Compiler)       :- attr("node_compiler", Package, Compiler).
node_compiler_version(Package, Compiler, Version)
  :- attr("node_compiler_version", Package, Compiler, Version).
node_compiler_version_satisfies(Package, Compiler, Version)
  :- attr("node_compiler_version_satisfies", Package, Compiler, Version).

attr("node", Package)                          :- node(Package).
attr("version", Package, Version)              :- version(Package, Version).
attr("version_satisfies", Package, Constraint) :- version_satisfies(Package, Constraint).
attr("node_platform", Package, Platform)       :- node_platform(Package, Platform).
attr("node_os", Package, OS)                   :- node_os(Package, OS).
attr("node_target", Package, Target)           :- node_target(Package, Target).
attr("node_target_satisfies", Package, Target) :- node_target_satisfies(Package, Target).
attr("variant_value", Package, Variant, Value) :- variant_value(Package, Variant, Value).
attr("variant_set", Package, Variant, Value)   :- variant_set(Package, Variant, Value).
attr("node_flag", Package, FlagType, Flag)     :- node_flag(Package, FlagType, Flag).
attr("node_compiler", Package, Compiler)       :- node_compiler(Package, Compiler).
attr("node_compiler_version", Package, Compiler, Version)
  :- node_compiler_version(Package, Compiler, Version).
attr("node_compiler_version_satisfies", Package, Compiler, Version)
  :- node_compiler_version_satisfies(Package, Compiler, Version).

% do not warn if generated program contains none of these.
#defined depends_on/3.
#defined declared_dependency/3.
#defined virtual/1.
#defined virtual_node/1.
#defined virtual_root/1.
#defined provides_virtual/2.
#defined external/1.
#defined external_spec/2.
#defined external_version_declared/4.
#defined external_only/1.
#defined pkg_provider_preference/4.
#defined default_provider_preference/3.
#defined version_satisfies/2.
#defined node_compiler_version_satisfies/3.
#defined root/1.

%-----------------------------------------------------------------------------
% External semantics
%-----------------------------------------------------------------------------

% if an external version is declared, it is also declared globally
version_declared(Package, Version, Weight) :- external_version_declared(Package, Version, Weight, _).

% if a package is external its version must be one of the external versions
1 { version(Package, Version): external_version_declared(Package, Version, _, _) } 1 :- external(Package).

% if a package is not buildable (external_only), only externals are allowed
external(Package) :- external_only(Package), node(Package).

% a package is a real_node if it is not external
real_node(Package) :- node(Package), not external(Package).

% a package is external if we are using an external spec for it
external(Package) :- external_spec_selected(Package, _).

% we can't use the weight for an external version if we don't use the
% corresponding external spec.
:- version(Package, Version),
   version_weight(Package, Weight),
   external_version_declared(Package, Version, Weight, ID),
   not external(Package).

% determine if an external spec has been selected
external_spec_selected(Package, LocalIndex) :-
    external_conditions_hold(Package, LocalIndex),
    node(Package).

external_conditions_hold(Package, LocalIndex) :-
    possible_external(ID, Package, LocalIndex), condition_holds(ID).

% it cannot happen that a spec is external, but none of the external specs
% conditions hold.
:- external(Package), not external_conditions_hold(Package, _).

#defined possible_external/3.
#defined external_spec_index/3.
#defined external_spec_condition/3.
#defined external_spec_condition/4.
#defined external_spec_condition/5.

%-----------------------------------------------------------------------------
% Variant semantics
%-----------------------------------------------------------------------------
% one variant value for single-valued variants.
1 {
  variant_value(Package, Variant, Value)
  : variant_possible_value(Package, Variant, Value)
} 1
 :- node(Package),
    variant(Package, Variant),
    variant_single_value(Package, Variant).

% at least one variant value for multi-valued variants.
1 {
 variant_value(Package, Variant, Value)
 : variant_possible_value(Package, Variant, Value)
}
 :- node(Package),
    variant(Package, Variant),
    not variant_single_value(Package, Variant).

% if a variant is set to anything, it is considered 'set'.
variant_set(Package, Variant) :- variant_set(Package, Variant, _).

% A variant cannot have a value that is not also a possible value
:- variant_value(Package, Variant, Value), not variant_possible_value(Package, Variant, Value).

% Some multi valued variants accept multiple values from disjoint sets.
% Ensure that we respect that constraint and we don't pick values from more
% than one set at once
:- variant_value(Package, Variant, Value1),
   variant_value(Package, Variant, Value2),
   variant_value_from_disjoint_sets(Package, Variant, Value1, Set1),
   variant_value_from_disjoint_sets(Package, Variant, Value2, Set2),
   Set1 != Set2.

% variant_set is an explicitly set variant value. If it's not 'set',
% we revert to the default value. If it is set, we force the set value
variant_value(Package, Variant, Value)
 :- node(Package),
    variant(Package, Variant),
    variant_set(Package, Variant, Value).

% The rules below allow us to prefer default values for variants
% whenever possible. If a variant is set in a spec, or if it is
% specified in an external, we score it as if it was a default value.
variant_not_default(Package, Variant, Value, 1)
 :- variant_value(Package, Variant, Value),
    not variant_default_value(Package, Variant, Value),
    not variant_set(Package, Variant, Value),
    not external_with_variant_set(Package, Variant, Value),
    node(Package).

% We are using the default value for a variant
variant_not_default(Package, Variant, Value, 0)
 :- variant_value(Package, Variant, Value),
    variant_default_value(Package, Variant, Value),
    node(Package).

% The variant is set in the spec
variant_not_default(Package, Variant, Value, 0)
 :- variant_value(Package, Variant, Value),
    variant_set(Package, Variant, Value),
    node(Package).

% The variant is set in an external spec
external_with_variant_set(Package, Variant, Value)
 :- variant_value(Package, Variant, Value),
    condition_requirement(ID, "variant_value", Package, Variant, Value),
    possible_external(ID, Package, _),
    external(Package),
    node(Package).

variant_not_default(Package, Variant, Value, 0)
 :- variant_value(Package, Variant, Value),
    external_with_variant_set(Package, Variant, Value),
    node(Package).

% The default value for a variant in a package is what is written
% in the package.py file, unless some preference is set in packages.yaml
variant_default_value(Package, Variant, Value)
 :- variant_default_value_from_package_py(Package, Variant, Value),
    not variant_default_value_from_packages_yaml(Package, Variant, _).

variant_default_value(Package, Variant, Value)
 :- variant_default_value_from_packages_yaml(Package, Variant, Value).

% Treat 'none' in a special way - it cannot be combined with other
% values even if the variant is multi-valued
:- 2 {variant_value(Package, Variant, Value): variant_possible_value(Package, Variant, Value)},
   variant_value(Package, Variant, "none").

% patches and dev_path are special variants -- they don't have to be
% declared in the package, so we just allow them to spring into existence
% when assigned a value.
auto_variant("dev_path").
auto_variant("patches").
variant(Package, Variant)
  :- variant_set(Package, Variant, _), auto_variant(Variant).
variant_single_value(Package, "dev_path")
  :- variant_set(Package, "dev_path", _).

% suppress warnings about this atom being unset.  It's only set if some
% spec or some package sets it, and without this, clingo will give
% warnings like 'info: atom does not occur in any rule head'.
#defined variant/2.
#defined variant_set/3.
#defined variant_single_value/2.
#defined variant_default_value/3.
#defined variant_possible_value/3.
#defined variant_default_value_from_packages_yaml/3.
#defined variant_default_value_from_package_py/3.
#defined variant_value_from_disjoint_sets/4.

%-----------------------------------------------------------------------------
% Platform semantics
%-----------------------------------------------------------------------------

% one platform per node
:- M = #count { Platform : node_platform(Package, Platform) }, M !=1, node(Package).

% if no platform is set, fall back to the default
node_platform(Package, Platform)
 :- node(Package),
    not node_platform_set(Package),
    node_platform_default(Platform).

% setting platform on a node is a hard constraint
node_platform(Package, Platform)
 :- node(Package), node_platform_set(Package, Platform).

% platform is set if set to anything
node_platform_set(Package) :- node_platform_set(Package, _).

#defined node_platform_set/2.  % avoid warnings

%-----------------------------------------------------------------------------
% OS semantics
%-----------------------------------------------------------------------------
% one os per node
1 { node_os(Package, OS) : os(OS) } 1 :- node(Package).

% node_os_set implies that the node must have that os
node_os(Package, OS) :- node(Package), node_os_set(Package, OS).
node_os_set(Package) :- node_os_set(Package, _).

% inherit OS along dependencies
node_os_inherit(Package, OS) :- node_os_set(Package, OS).
node_os_inherit(Dependency, OS)
  :- node_os_inherit(Package, OS), depends_on(Package, Dependency),
     not node_os_set(Dependency).
node_os_inherit(Package) :- node_os_inherit(Package, _).

node_os(Package, OS) :- node_os_inherit(Package, OS).

% fall back to default if not set or inherited
node_os(Package, OS)
  :- node(Package),
     not node_os_set(Package), not node_os_inherit(Package),
     node_os_default(OS).

#defined node_os_set/2.

%-----------------------------------------------------------------------------
% Target semantics
%-----------------------------------------------------------------------------
% one target per node -- optimization will pick the "best" one
1 { node_target(Package, Target) : target(Target) } 1 :- node(Package).

% node_target_satisfies semantics
1 { node_target(Package, Target) : node_target_satisfies(Package, Constraint, Target) } 1
  :- node_target_satisfies(Package, Constraint).
node_target_satisfies(Package, Constraint)
  :- node_target(Package, Target), node_target_satisfies(Package, Constraint, Target).
#defined node_target_satisfies/3.

% The target weight is either the default target weight
% or a more specific per-package weight if set
target_weight(Target, Package, Weight)
  :- default_target_weight(Target, Weight),
     node(Package),
     not derive_target_from_parent(_, Package),
     not package_target_weight(Target, Package, _).

% TODO: Need to account for the case of more than one parent
% TODO: each of which sets different targets
target_weight(Target, Dependency, Weight)
  :- depends_on(Package, Dependency),
     derive_target_from_parent(Package, Dependency),
     target_weight(Target, Package, Weight).

target_weight(Target, Package, Weight)
  :- package_target_weight(Target, Package, Weight).

% can't use targets on node if the compiler for the node doesn't support them
:- node_target(Package, Target),
   not compiler_supports_target(Compiler, Version, Target),
   node_compiler(Package, Compiler),
   node_compiler_version(Package, Compiler, Version).

% if a target is set explicitly, respect it
node_target(Package, Target)
 :- node(Package), node_target_set(Package, Target).

% each node has the weight of its assigned target
node_target_weight(Package, Weight)
 :- node(Package),
    node_target(Package, Target),
    target_weight(Target, Package, Weight).

% compatibility rules for targets among nodes
node_target_match_pref(Dependency, Target)
  :- depends_on(Package, Dependency),
     node_target_match_pref(Package, Target),
     not node_target_set(Dependency, _).

node_target_match_pref(Dependency, Target)
  :- depends_on(Package, Dependency),
     node_target_set(Package, Target),
     not node_target_match_pref(Package, Target),
     not node_target_set(Dependency, _).

node_target_match_pref(Dependency, Target)
  :- depends_on(Package, Dependency),
     root(Package), node_target(Package, Target),
     not node_target_match_pref(Package, _).

node_target_match(Package, 1)
  :- node_target(Package, Target), node_target_match_pref(Package, Target).

derive_target_from_parent(Parent, Package)
  :- depends_on(Parent, Package), not package_target_weight(_, Package, _).


#defined node_target_set/2.
#defined package_target_weight/3.

%-----------------------------------------------------------------------------
% Compiler semantics
%-----------------------------------------------------------------------------
compiler(Compiler) :- compiler_version(Compiler, _).

% There must be only one compiler set per node. The compiler
% is chosen among available versions.
1 { node_compiler_version(Package, Compiler, Version)
    : compiler_version(Compiler, Version) } 1 :- node(Package).

% Sometimes we just need to know the compiler and not the version
node_compiler(Package, Compiler) :- node_compiler_version(Package, Compiler, _).

% We can't have a compiler be enforced and select the version from another compiler
:- node_compiler(Package, Compiler1),
   node_compiler_version(Package, Compiler2, _),
   Compiler1 != Compiler2.

% define node_compiler_version_satisfies/3 from node_compiler_version_satisfies/4
% version_satisfies implies that exactly one of the satisfying versions
% is the package's version, and vice versa.
1 { node_compiler_version(Package, Compiler, Version)
    : node_compiler_version_satisfies(Package, Compiler, Constraint, Version) } 1
  :- node_compiler_version_satisfies(Package, Compiler, Constraint).
node_compiler_version_satisfies(Package, Compiler, Constraint)
  :- node_compiler_version(Package, Compiler, Version),
     node_compiler_version_satisfies(Package, Compiler, Constraint, Version).

#defined node_compiler_version_satisfies/4.

% If the compiler version was set from the command line,
% respect it verbatim
node_compiler_version(Package, Compiler, Version) :- node_compiler_version_set(Package, Compiler, Version).

% Cannot select a compiler if it is not supported on the OS
% Compilers that are explicitly marked as allowed
% are excluded from this check
:- node_compiler_version(Package, Compiler, Version), node_os(Package, OS),
   not compiler_supports_os(Compiler, Version, OS),
   not allow_compiler(Compiler, Version).

% If a package and one of its dependencies don't have the
% same compiler there's a mismatch.
compiler_mismatch(Package, Dependency)
  :- depends_on(Package, Dependency),
     node_compiler_version(Package, Compiler1, _),
     node_compiler_version(Dependency, Compiler2, _),
     Compiler1 != Compiler2.

compiler_mismatch(Package, Dependency)
  :- depends_on(Package, Dependency),
     node_compiler_version(Package, Compiler, Version1),
     node_compiler_version(Dependency, Compiler, Version2),
     Version1 != Version2.

#defined node_compiler_set/2.
#defined node_compiler_version_set/3.
#defined compiler_supports_os/3.
#defined allow_compiler/2.

% compilers weighted by preference according to packages.yaml
compiler_weight(Package, Weight)
 :- node_compiler_version(Package, Compiler, V),
    node_compiler_preference(Package, Compiler, V, Weight).
compiler_weight(Package, Weight)
 :- node_compiler_version(Package, Compiler, V),
    not node_compiler_preference(Package, Compiler, V, _),
    default_compiler_preference(Compiler, V, Weight).
compiler_weight(Package, 100)
 :- node_compiler_version(Package, Compiler, Version),
    not node_compiler_preference(Package, Compiler, Version, _),
    not default_compiler_preference(Compiler, Version, _).

#defined node_compiler_preference/4.
#defined default_compiler_preference/3.

%-----------------------------------------------------------------------------
% Compiler flags
%-----------------------------------------------------------------------------
% propagate flags when compilers match
inherit_flags(Package, Dependency)
 :- depends_on(Package, Dependency),
    node_compiler(Package, Compiler),
    node_compiler(Dependency, Compiler),
    compiler(Compiler), flag_type(FlagType).
node_flag_inherited(Dependency, FlagType, Flag)
 :- node_flag_set(Package, FlagType, Flag), inherit_flags(Package, Dependency).
node_flag_inherited(Dependency, FlagType, Flag)
 :- node_flag_inherited(Package, FlagType, Flag),
    inherit_flags(Package, Dependency).

% node with flags set to anythingg is "set"
node_flag_set(Package) :- node_flag_set(Package, _, _).

% remember where flags came from
node_flag_source(Package, Package) :- node_flag_set(Package).
node_flag_source(Dependency, Q)
 :- node_flag_source(Package, Q), inherit_flags(Package, Dependency).

% compiler flags from compilers.yaml are put on nodes if compiler matches
node_flag(Package, FlagType, Flag)
 :- not node_flag_set(Package),
    compiler_version_flag(Compiler, Version, FlagType, Flag),
    node_compiler_version(Package, Compiler, Version),
    flag_type(FlagType),
    compiler(Compiler),
    compiler_version(Compiler, Version).

node_flag_compiler_default(Package)
 :- not node_flag_set(Package),
    compiler_version_flag(Compiler, Version, FlagType, Flag),
    node_compiler_version(Package, Compiler, Version),
    flag_type(FlagType),
    compiler(Compiler),
    compiler_version(Compiler, Version).

% if a flag is set to something or inherited, it's included
node_flag(Package, FlagType, Flag) :- node_flag_set(Package, FlagType, Flag).
node_flag(Package, FlagType, Flag)
 :- node_flag_inherited(Package, FlagType, Flag).

% if no node flags are set for a type, there are no flags.
no_flags(Package, FlagType)
 :- not node_flag(Package, FlagType, _), node(Package), flag_type(FlagType).

#defined compiler_version_flag/4.
#defined node_flag/3.
#defined node_flag_set/3.

%-----------------------------------------------------------------------------
% How to optimize the spec (high to low priority)
%-----------------------------------------------------------------------------
% Each criterion below has:
%   1. an opt_criterion(ID, Name) fact that describes the criterion, and
%   2. a `#minimize{ 0@2 : #true }.` statement that ensures the criterion
%      is displayed (clingo doesn't display sums over empty sets by default)

% The highest priority is to minimize the:
% 1. Version weight
% 2. Number of variants with a non default value, if not set
% for the root(Package)
opt_criterion(15, "version weight").
#minimize{ 0@15 : #true }.
#minimize { Weight@15 : root(Package),version_weight(Package, Weight) }.

opt_criterion(14, "number of non-default variants (roots)").
#minimize{ 0@14 : #true }.
#minimize {
    Weight@14,Package,Variant,Value
    : variant_not_default(Package, Variant, Value, Weight), root(Package)
}.

% If the value is a multivalued variant there could be multiple
% values set as default. Since a default value has a weight of 0 we
% need to maximize their number below to ensure they're all set
opt_criterion(13, "multi-valued variants + preferred providers for roots").
#minimize{ 0@13 : #true }.
#maximize {
    1@13,Package,Variant,Value
    : variant_not_default(Package, Variant, Value, Weight),
    not variant_single_value(Package, Variant),
    root(Package)
}.
#minimize{
    Weight@13,Provider
    : provider_weight(Provider, Weight), root(Provider)
}.

% Try to use default variants or variants that have been set
opt_criterion(11, "number of non-default variants (non-roots)").
#minimize{ 0@11 : #true }.
#minimize {
    Weight@11,Package,Variant,Value
    : variant_not_default(Package, Variant, Value, Weight), not root(Package)
}.

% Minimize the weights of the providers, i.e. use as much as
% possible the most preferred providers
opt_criterion(9, "number of non-default providers (non-roots)").
#minimize{ 0@9 : #true }.
#minimize{
    Weight@9,Provider
    : provider_weight(Provider, Weight), not root(Provider)
}.

% If the value is a multivalued variant there could be multiple
% values set as default. Since a default value has a weight of 0 we
% need to maximize their number below to ensure they're all set
opt_criterion(8, "count of non-root multi-valued variants").
#minimize{ 0@8 : #true }.
#maximize {
    1@8,Package,Variant,Value
    : variant_not_default(Package, Variant, Value, Weight),
    not variant_single_value(Package, Variant),
    not root(Package)
}.

% Try to minimize the number of compiler mismatches in the DAG.
opt_criterion(7, "compiler mismatches").
#minimize{ 0@7 : #true }.
#minimize{ 1@7,Package,Dependency : compiler_mismatch(Package, Dependency) }.

% Choose more recent versions for nodes
opt_criterion(6, "version badness").
#minimize{ 0@6 : #true }.
#minimize{
    Weight@6,Package : version_weight(Package, Weight)
}.

% Try to use preferred compilers
opt_criterion(5, "non-preferred compilers").
#minimize{ 0@5 : #true }.
#minimize{ Weight@5,Package : compiler_weight(Package, Weight) }.

% Maximize the number of matches for targets in the DAG, try
% to select the preferred target.
opt_criterion(4, "target matches").
#minimize{ 0@4 : #true }.
#maximize{ Weight@4,Package : node_target_match(Package, Weight) }.

opt_criterion(3, "non-preferred targets").
#minimize{ 0@3 : #true }.
#minimize{ Weight@3,Package : node_target_weight(Package, Weight) }.
