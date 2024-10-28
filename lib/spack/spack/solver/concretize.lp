% Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
% Spack Project Developers. See the top-level COPYRIGHT file for details.
%
% SPDX-License-Identifier: (Apache-2.0 OR MIT)

%=============================================================================
% This logic program implements Spack's concretizer
%=============================================================================

% ID of the nodes in the "root" link-run sub-DAG
#const min_dupe_id = 0.

#const direct_link_run = 0.
#const direct_build = 1.

% Allow clingo to create nodes
{ attr("node", node(0..X-1, Package))         } :- max_dupes(Package, X), not virtual(Package).
{ attr("virtual_node", node(0..X-1, Package)) } :- max_dupes(Package, X), virtual(Package).

% Integrity constraints on DAG nodes
:- attr("root", PackageNode),
   not attr("node", PackageNode),
   internal_error("Every root must be a node").
:- attr("version", PackageNode, _),
   not attr("node", PackageNode),
   not attr("virtual_node", PackageNode),
   internal_error("Only nodes and virtual_nodes can have versions").
:- attr("node_version_satisfies", PackageNode, _),
   not attr("node", PackageNode),
   not attr("virtual_node", PackageNode),
   internal_error("Only nodes and virtual_nodes can have version satisfaction").
:- attr("hash", PackageNode, _),
   not attr("node", PackageNode),
   internal_error("Only nodes can have hashes").
:- attr("node_platform", PackageNode, _),
   not attr("node", PackageNode),
   internal_error("Only nodes can have platforms").
:- attr("node_os", PackageNode, _), not attr("node", PackageNode),
   internal_error("Only nodes can have node_os").
:- attr("node_target", PackageNode, _), not attr("node", PackageNode),
   internal_error("Only nodes can have node_target").
:- attr("node_compiler_version", PackageNode, _, _), not attr("node", PackageNode),
   internal_error("Only nodes can have node_compiler_version").
:- attr("variant_value", PackageNode, _, _), not attr("node", PackageNode),
   internal_error("variant_value true for a non-node").
:- attr("node_flag", PackageNode, _), not attr("node", PackageNode),
   internal_error("node_flag assigned for non-node").
:- attr("external_spec_selected", PackageNode, _), not attr("node", PackageNode),
   internal_error("external_spec_selected for non-node").
:- attr("depends_on", ParentNode, _, _), not attr("node", ParentNode),
   internal_error("non-node depends on something").
:- attr("depends_on", _, ChildNode, _), not attr("node", ChildNode),
   internal_error("something depends_on a non-node").
:- attr("virtual_node", VirtualNode), not provider(_, VirtualNode),
   internal_error("virtual node with no provider").
:- provider(_, VirtualNode), not attr("virtual_node", VirtualNode),
   internal_error("provider with no virtual node").
:- provider(PackageNode, _), not attr("node", PackageNode),
   internal_error("provider with no real node").

:- attr("root", node(ID, PackageNode)), ID > min_dupe_id,
   internal_error("root with a non-minimal duplicate ID").

% Nodes in the "root" unification set cannot depend on non-root nodes if the dependency is "link" or "run"
:- attr("depends_on", node(min_dupe_id, Package), node(ID, _), "link"), ID != min_dupe_id, unification_set("root", node(min_dupe_id, Package)), internal_error("link dependency out of the root unification set").
:- attr("depends_on", node(min_dupe_id, Package), node(ID, _), "run"),  ID != min_dupe_id, unification_set("root", node(min_dupe_id, Package)), internal_error("run dependency out of the root unification set").

% Namespaces are statically assigned by a package fact if not otherwise set
error(100, "{0} does not have a namespace", Package) :- attr("node", node(ID, Package)),
   not attr("namespace", node(ID, Package), _),
   internal_error("A node must have a namespace").
error(100, "{0} cannot come from both {1} and {2} namespaces", Package, NS1, NS2) :- attr("node", node(ID, Package)),
   attr("namespace", node(ID, Package), NS1),
   attr("namespace", node(ID, Package), NS2),
   NS1 != NS2,
   internal_error("A node cannot have two namespaces").

attr("namespace", node(ID, Package), Namespace) :- attr("namespace_set", node(ID, Package), Namespace).
attr("namespace", node(ID, Package), Namespace)
  :- attr("node", node(ID, Package)),
     not attr("namespace_set", node(ID, Package), _),
     pkg_fact(Package, namespace(Namespace)).

% Rules on "unification sets", i.e. on sets of nodes allowing a single configuration of any given package
unify(SetID, PackageName) :- unification_set(SetID, node(_, PackageName)).
:- 2 { unification_set(SetID, node(_, PackageName)) }, unify(SetID, PackageName),
   internal_error("Cannot have multiple unification sets IDs for one set").

unification_set("root", PackageNode) :- attr("root", PackageNode).
unification_set(SetID, ChildNode) :- attr("depends_on", ParentNode, ChildNode, Type), Type != "build", unification_set(SetID, ParentNode).

unification_set(("build", node(X, Child)), node(X, Child))
  :- attr("depends_on", ParentNode, node(X, Child), Type),
     Type == "build",
     multiple_unification_sets(Child),
     unification_set(SetID, ParentNode).

unification_set("generic_build", node(X, Child))
  :- attr("depends_on", ParentNode, node(X, Child), Type),
     Type == "build",
     not multiple_unification_sets(Child),
     unification_set(_, ParentNode).

unification_set(SetID, VirtualNode)
  :- provider(PackageNode, VirtualNode),
     unification_set(SetID, PackageNode).

% Do not allow split dependencies, for now. This ensures that we don't construct graphs where e.g.
% a python extension depends on setuptools@63.4 as a run dependency, but uses e.g. setuptools@68
% as a build dependency.
%
% We'll need to relax the rule before we get to actual cross-compilation
:- depends_on(ParentNode, node(X, Dependency)), depends_on(ParentNode, node(Y, Dependency)), X < Y,
   internal_error("Cannot split link/build deptypes for a single edge (yet)").


#defined multiple_unification_sets/1.
#defined runtime/1.

%----
% Rules to break symmetry and speed-up searches
%----

% In the "root" unification set only ID = 0 are allowed
:- unification_set("root", node(ID, _)), ID != 0, internal_error("root unification set has node with non-zero unification set ID").

% In the "root" unification set we allow only packages from the link-run possible subDAG
:- unification_set("root", node(_, Package)), not possible_in_link_run(Package), not virtual(Package), internal_error("package outside possible link/run graph in root unification set").

% Each node must belong to at least one unification set
:- attr("node", PackageNode), not unification_set(_, PackageNode), internal_error("node belongs to no unification set").

% Cannot have a node with an ID, if lower ID of the same package are not used
:- attr("node", node(ID1, Package)),
   not attr("node", node(ID2, Package)),
   max_dupes(Package, X), ID1=0..X-1, ID2=0..X-1, ID2 < ID1,
   internal_error("node skipped id number").

:- attr("virtual_node", node(ID1, Package)),
   not attr("virtual_node", node(ID2, Package)),
   max_dupes(Package, X), ID1=0..X-1, ID2=0..X-1, ID2 < ID1,
   internal_error("virtual node skipped id number").

%-----------------------------------------------------------------------------
% Map literal input specs to facts that drive the solve
%-----------------------------------------------------------------------------

% TODO: literals, at the moment, can only influence the "root" unification set. This needs to be extended later.

% Node attributes that have multiple node arguments (usually, only the first argument is a node)
multiple_nodes_attribute("depends_on").
multiple_nodes_attribute("virtual_on_edge").
multiple_nodes_attribute("provider_set").

trigger_condition_holds(TriggerID, node(min_dupe_id, Package)) :-
  solve_literal(TriggerID),
  pkg_fact(Package, condition_trigger(_, TriggerID)),
  literal(TriggerID).

trigger_node(TriggerID, Node, Node) :-
  trigger_condition_holds(TriggerID, Node),
  literal(TriggerID).

% Since we trigger the existence of literal nodes from a condition, we need to construct the condition_set/2
mentioned_in_literal(Root, Mentioned) :- mentioned_in_literal(TriggerID, Root, Mentioned), solve_literal(TriggerID).
condition_set(node(min_dupe_id, Root), node(min_dupe_id, Root)) :-  mentioned_in_literal(Root, Root).

1 { condition_set(node(min_dupe_id, Root), node(0..Y-1, Mentioned)) : max_dupes(Mentioned, Y) } 1 :-
  mentioned_in_literal(Root, Mentioned), Mentioned != Root,
  internal_error("must have exactly one condition_set for literals").

% Discriminate between "roots" that have been explicitly requested, and roots that are deduced from "virtual roots"
explicitly_requested_root(node(min_dupe_id, Package)) :-
  solve_literal(TriggerID),
  trigger_and_effect(Package, TriggerID, EffectID),
  imposed_constraint(EffectID, "root", Package).


% Keep track of which nodes are associated with which root DAG
associated_with_root(RootNode, RootNode) :- attr("root", RootNode).

associated_with_root(RootNode, ChildNode) :-
   depends_on(ParentNode, ChildNode),
   associated_with_root(RootNode, ParentNode).

% We cannot have a node in the root condition set, that is not associated with that root
:- attr("root", RootNode),
   condition_set(RootNode, node(X, Package)),
   not virtual(Package),
   not associated_with_root(RootNode, node(X, Package)),
   internal_error("nodes in root condition set must be associated with root").

#defined concretize_everything/0.
#defined literal/1.

% Attributes for node packages which must have a single value
attr_single_value("version").
attr_single_value("node_platform").
attr_single_value("node_os").
attr_single_value("node_target").

% Error when no attribute is selected
error(100, no_value_error, Attribute, Package)
  :- attr("node", node(ID, Package)),
     attr_single_value(Attribute),
     not attr(Attribute, node(ID, Package), _).

% Error when multiple attr need to be selected
error(100, multiple_values_error, Attribute, Package)
  :- attr("node", node(ID, Package)),
     attr_single_value(Attribute),
     2 { attr(Attribute, node(ID, Package), Value) }.

%-----------------------------------------------------------------------------
% Languages used
%-----------------------------------------------------------------------------

attr("language", node(X, Package), Language) :-
  condition_holds(ConditionID, node(X, Package)),
  pkg_fact(Package,language(ConditionID, Language)).

%-----------------------------------------------------------------------------
% Version semantics
%-----------------------------------------------------------------------------

% Versions are declared with a weight and an origin, which indicates where the
% version was declared (e.g. "package_py" or "external").
pkg_fact(Package, version_declared(Version, Weight)) :- pkg_fact(Package, version_declared(Version, Weight, _)).

% We can't emit the same version **with the same weight** from two different sources
:- pkg_fact(Package, version_declared(Version, Weight, Origin1)),
   pkg_fact(Package, version_declared(Version, Weight, Origin2)),
   Origin1 < Origin2,
   internal_error("Two versions with identical weights").

% We cannot use a version declared for an installed package if we end up building it
:- pkg_fact(Package, version_declared(Version, Weight, "installed")),
   attr("version", node(ID, Package), Version),
   version_weight(node(ID, Package), Weight),
   not attr("hash", node(ID, Package), _),
   internal_error("Reuse version weight used for built package").

% versions are declared w/priority -- declared with priority implies declared
pkg_fact(Package, version_declared(Version)) :- pkg_fact(Package, version_declared(Version, _)).

% If something is a package, it has only one version and that must be a
% declared version.
% We allow clingo to choose any version(s), and infer an error if there
% is not precisely one version chosen. Error facts are heavily optimized
% against to ensure they cannot be inferred when a non-error solution is
% possible
{ attr("version", node(ID, Package), Version) : pkg_fact(Package, version_declared(Version)) }
 :- attr("node", node(ID, Package)).

% A virtual package may or may not have a version, but never has more than one
error(100, "Cannot select a single version for virtual '{0}'", Virtual)
  :- attr("virtual_node", node(ID, Virtual)),
     2 { attr("version", node(ID, Virtual), Version) }.

% If we select a deprecated version, mark the package as deprecated
attr("deprecated", node(ID, Package), Version) :-
     attr("version", node(ID, Package), Version),
     pkg_fact(Package, deprecated_version(Version)).

error(100, "Package '{0}' needs the deprecated version '{1}', and this is not allowed", Package, Version)
  :- deprecated_versions_not_allowed(),
     attr("version", node(ID, Package), Version),
     not external(node(ID, Package)),
     not concrete(node(ID, Package)),
     pkg_fact(Package, deprecated_version(Version)).

possible_version_weight(node(ID, Package), Weight)
 :- attr("version", node(ID, Package), Version),
    pkg_fact(Package, version_declared(Version, Weight)).

% we can't use the weight for an external version if we don't use the
% corresponding external spec.
:- attr("version", node(ID, Package), Version),
   version_weight(node(ID, Package), Weight),
   pkg_fact(Package, version_declared(Version, Weight, "external")),
   not external(node(ID, Package)),
   internal_error("External weight used for built package").

% we can't use a weight from an installed spec if we are building it
% and vice-versa
:- attr("version", node(ID, Package), Version),
   version_weight(node(ID, Package), Weight),
   pkg_fact(Package, version_declared(Version, Weight, "installed")),
   build(node(ID, Package)),
   internal_error("Reuse version weight used for build package").

:- attr("version", node(ID, Package), Version),
   version_weight(node(ID, Package), Weight),
   not pkg_fact(Package, version_declared(Version, Weight, "installed")),
   not pkg_fact(Package, version_declared(Version, Weight, "installed_git_version")),
   not build(node(ID, Package)),
   internal_error("Build version weight used for reused package").

1 { version_weight(node(ID, Package), Weight) : pkg_fact(Package, version_declared(Version, Weight)) } 1
  :- attr("version", node(ID, Package), Version),
     attr("node", node(ID, Package)),
     internal_error("version weights must exist and be unique").

% node_version_satisfies implies that exactly one of the satisfying versions
% is the package's version, and vice versa.
% While this choice rule appears redundant with the initial choice rule for
% versions, virtual nodes with version constraints require this rule to be
% able to choose versions
{ attr("version", node(ID, Package), Version) : pkg_fact(Package, version_satisfies(Constraint, Version)) }
  :- attr("node_version_satisfies", node(ID, Package), Constraint).

% If there is at least a version that satisfy the constraint, impose a lower
% bound on the choice rule to avoid false positives with the error below
1 { attr("version", node(ID, Package), Version) : pkg_fact(Package, version_satisfies(Constraint, Version)) }
  :- attr("node_version_satisfies", node(ID, Package), Constraint),
     pkg_fact(Package, version_satisfies(Constraint, _)),
     internal_error("must choose a single version to satisfy version constraints").

% More specific error message if the version cannot satisfy some constraint
% Otherwise covered by `no_version_error` and `versions_conflict_error`.
error(10, "Cannot satisfy '{0}@{1}'", Package, Constraint)
  :- attr("node_version_satisfies", node(ID, Package), Constraint),
     attr("version", node(ID, Package), Version),
     not pkg_fact(Package, version_satisfies(Constraint, Version)).

attr("node_version_satisfies", node(ID, Package), Constraint)
  :- attr("version", node(ID, Package), Version),
     pkg_fact(Package, version_satisfies(Constraint, Version)).

#defined version_satisfies/3.
#defined deprecated_versions_not_allowed/0.
#defined deprecated_version/2.

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

% A "condition_set(PackageNode, _)" is the set of nodes on which PackageNode can require / impose conditions
% Currently, for a given node, this is the link-run sub-DAG of PackageNode and its direct build dependencies
condition_set(PackageNode, PackageNode, direct_link_run) :- attr("node", PackageNode).

condition_set(PackageNode, PackageNode, direct_link_run) :- provider(PackageNode, VirtualNode).
condition_set(PackageNode, VirtualNode, direct_link_run) :- provider(PackageNode, VirtualNode).

condition_set(PackageNode, DependencyNode, direct_build) :- condition_set(PackageNode, PackageNode, direct_link_run), attr("depends_on", PackageNode, DependencyNode, "build").
condition_set(PackageNode, DependencyNode, direct_link_run) :- condition_set(PackageNode, PackageNode, direct_link_run), attr("depends_on", PackageNode, DependencyNode, Type), Type != "build".

condition_set(ID, VirtualNode, Type) :- condition_set(ID, PackageNode, Type), provider(PackageNode, VirtualNode).

condition_set(ID, PackageNode) :- condition_set(ID, PackageNode, _).

condition_set(VirtualNode, X) :- provider(PackageNode, VirtualNode), condition_set(PackageNode, X).

condition_packages(ID, A1) :- condition_requirement(ID, _, A1).
condition_packages(ID, A1) :- condition_requirement(ID, _, A1, _).
condition_packages(ID, A1) :- condition_requirement(ID, _, A1, _, _).
condition_packages(ID, A1) :- condition_requirement(ID, _, A1, _, _, _).

trigger_node(ID, node(PackageID, Package), node(PackageID, Package)) :- pkg_fact(Package, trigger_id(ID)), attr("node", node(PackageID, Package)).
trigger_node(ID, node(PackageID, Package), node(VirtualID, Virtual)) :- pkg_fact(Virtual, trigger_id(ID)), provider(node(PackageID, Package), node(VirtualID, Virtual)).

condition_nodes(TriggerID, PackageNode, node(X, A1))
  :- condition_packages(TriggerID, A1),
     condition_set(PackageNode, node(X, A1)),
     trigger_node(TriggerID, PackageNode, _).

cannot_hold(TriggerID, PackageNode)
  :- condition_packages(TriggerID, A1),
     not condition_set(PackageNode, node(_, A1)),
     trigger_node(TriggerID, PackageNode, _).

trigger_condition_holds(ID, RequestorNode) :-
  trigger_node(ID, PackageNode, RequestorNode);
  attr(Name, node(X, A1))             : condition_requirement(ID, Name, A1),             condition_nodes(ID, PackageNode, node(X, A1));
  attr(Name, node(X, A1), A2)         : condition_requirement(ID, Name, A1, A2),         condition_nodes(ID, PackageNode, node(X, A1));
  attr(Name, node(X, A1), A2, A3)     : condition_requirement(ID, Name, A1, A2, A3),     condition_nodes(ID, PackageNode, node(X, A1)), not multiple_nodes_attribute(Name);
  attr(Name, node(X, A1), A2, A3, A4) : condition_requirement(ID, Name, A1, A2, A3, A4), condition_nodes(ID, PackageNode, node(X, A1));
  % Special cases
  not cannot_hold(ID, PackageNode).

condition_holds(ConditionID, node(X, Package))
  :- pkg_fact(Package, condition_trigger(ConditionID, TriggerID)),
     trigger_condition_holds(TriggerID, node(X, Package)).

trigger_and_effect(Package, TriggerID, EffectID)
  :- pkg_fact(Package, condition_trigger(ID, TriggerID)),
     pkg_fact(Package, condition_effect(ID, EffectID)).

% condition_holds(ID, node(ID, Package)) implies all imposed_constraints, unless do_not_impose(ID, node(ID, Package))
% is derived. This allows imposed constraints to be canceled in special cases.
impose(EffectID, node(X, Package))
  :- trigger_and_effect(Package, TriggerID, EffectID),
     trigger_node(TriggerID, _, node(X, Package)),
     trigger_condition_holds(TriggerID, node(X, Package)),
     not do_not_impose(EffectID, node(X, Package)).

imposed_packages(ID, A1) :- imposed_constraint(ID, _, A1).
imposed_packages(ID, A1) :- imposed_constraint(ID, _, A1, _).
imposed_packages(ID, A1) :- imposed_constraint(ID, _, A1, _, _).
imposed_packages(ID, A1) :- imposed_constraint(ID, _, A1, _, _, _).
imposed_packages(ID, A1) :- imposed_constraint(ID, "depends_on", _, A1, _).

imposed_nodes(EffectID, node(NodeID, Package), node(X, A1))
  :- pkg_fact(Package, condition_trigger(ID, TriggerID)),
     pkg_fact(Package, condition_effect(ID, EffectID)),
     imposed_packages(EffectID, A1),
     condition_set(node(NodeID, Package), node(X, A1)),
     trigger_node(TriggerID, _, node(NodeID, Package)).

imposed_nodes(ConditionID, PackageNode, node(X, A1))
  :- imposed_packages(ConditionID, A1),
     condition_set(PackageNode, node(X, A1)),
     attr("hash", PackageNode, ConditionID).

:- imposed_packages(ID, A1), impose(ID, PackageNode), not condition_set(PackageNode, node(_, A1)),
   internal_error("Imposing constraint outside of condition set").
:- imposed_packages(ID, A1), impose(ID, PackageNode), not imposed_nodes(ID, PackageNode, node(_, A1)),
   internal_error("Imposing constraint outside of imposed_nodes").

% Conditions that hold impose may impose constraints on other specs
attr(Name, node(X, A1))             :- impose(ID, PackageNode), imposed_constraint(ID, Name, A1),             imposed_nodes(ID, PackageNode, node(X, A1)).
attr(Name, node(X, A1), A2)         :- impose(ID, PackageNode), imposed_constraint(ID, Name, A1, A2),         imposed_nodes(ID, PackageNode, node(X, A1)), not multiple_nodes_attribute(Name).
attr(Name, node(X, A1), A2, A3)     :- impose(ID, PackageNode), imposed_constraint(ID, Name, A1, A2, A3),     imposed_nodes(ID, PackageNode, node(X, A1)), not multiple_nodes_attribute(Name).
attr(Name, node(X, A1), A2, A3, A4) :- impose(ID, PackageNode), imposed_constraint(ID, Name, A1, A2, A3, A4), imposed_nodes(ID, PackageNode, node(X, A1)).

% Provider set is relevant only for literals, since it's the only place where `^[virtuals=foo] bar`
% might appear in the HEAD of a rule
attr("provider_set", node(min_dupe_id, Provider), node(min_dupe_id, Virtual))
  :- solve_literal(TriggerID),
     trigger_and_effect(_, TriggerID, EffectID),
     impose(EffectID, _),
     imposed_constraint(EffectID, "provider_set", Provider, Virtual).

provider(ProviderNode, VirtualNode) :- attr("provider_set", ProviderNode, VirtualNode).

% Here we can't use the condition set because it's a recursive definition, that doesn't define the
% node index, and leads to unsatisfiability. Hence we say that one and only one node index must
% satisfy the dependency.
1 { attr("depends_on", node(X, A1), node(0..Y-1, A2), A3) : max_dupes(A2, Y) } 1
  :- impose(ID, node(X, A1)),
     imposed_constraint(ID, "depends_on", A1, A2, A3),
     internal_error("Build deps must land in exactly one duplicate").

% Reconstruct virtual dependencies for reused specs
attr("virtual_on_edge", node(X, A1), node(Y, A2), Virtual)
  :- impose(ID, node(X, A1)),
     depends_on(node(X, A1), node(Y, A2)),
     imposed_constraint(ID, "virtual_on_edge", A1, A2, Virtual),
     not build(node(X, A1)).

virtual_condition_holds(node(Y, A2), Virtual)
  :- impose(ID, node(X, A1)),
     attr("virtual_on_edge", node(X, A1), node(Y, A2), Virtual),
     not build(node(X, A1)).

% we cannot have additional variant values when we are working with concrete specs
:- attr("node", node(ID, Package)),
   attr("hash", node(ID, Package), Hash),
   attr("variant_value", node(ID, Package), Variant, Value),
   not imposed_constraint(Hash, "variant_value", Package, Variant, Value),
   internal_error("imposed hash without imposing all variant values").

% we cannot have additional flag values when we are working with concrete specs
:- attr("node", node(ID, Package)),
   attr("hash", node(ID, Package), Hash),
   attr("node_flag", node(ID, Package), node_flag(FlagType, Flag, _, _)),
   not imposed_constraint(Hash, "node_flag", Package, node_flag(FlagType, Flag, _, _)),
   internal_error("imposed hash without imposing all flag values").

#defined condition/2.
#defined condition_requirement/3.
#defined condition_requirement/4.
#defined condition_requirement/5.
#defined condition_requirement/6.
#defined imposed_constraint/3.
#defined imposed_constraint/4.
#defined imposed_constraint/5.
#defined imposed_constraint/6.

%-----------------------------------------------------------------------------
% Concrete specs
%-----------------------------------------------------------------------------
% if a package is assigned a hash, it's concrete.
concrete(PackageNode) :- attr("hash", PackageNode, _), attr("node", PackageNode).

%-----------------------------------------------------------------------------
% Dependency semantics
%-----------------------------------------------------------------------------
% Dependencies of any type imply that one package "depends on" another
depends_on(PackageNode, DependencyNode) :- attr("depends_on", PackageNode, DependencyNode, _).

% a dependency holds if its condition holds and if it is not external or
% concrete. We chop off dependencies for externals, and dependencies of
% concrete specs don't need to be resolved -- they arise from the concrete
% specs themselves.
attr("track_dependencies", Node) :- build(Node), not external(Node).

% If a dependency holds on a package node, there must be one and only one dependency node satisfying it
1 { attr("depends_on", PackageNode, node(0..Y-1, Dependency), Type) : max_dupes(Dependency, Y) } 1
  :- attr("dependency_holds", PackageNode, Dependency, Type),
     not virtual(Dependency).

% all nodes in the graph must be reachable from some root
% this ensures a user can't say `zlib ^libiconv` (neither of which have any
% dependencies) and get a two-node unconnected graph
needed(PackageNode) :- attr("root", PackageNode).
needed(DependencyNode) :- needed(PackageNode), depends_on(PackageNode, DependencyNode).
error(10, "'{0}' is not a valid dependency for any package in the DAG", Package)
  :- attr("node", node(ID, Package)),
     not needed(node(ID, Package)).

#defined dependency_type/2.

%-----------------------------------------------------------------------------
% Conflicts
%-----------------------------------------------------------------------------
error(1, Msg)
  :- attr("node", node(ID, Package)),
     pkg_fact(Package, conflict(TriggerID, ConstraintID, Msg)),
     % node(ID1, TriggerPackage) is node(ID2, Package) in most, but not all, cases
     condition_holds(TriggerID, node(ID1, TriggerPackage)),
     condition_holds(ConstraintID, node(ID2, Package)),
     unification_set(X, node(ID2, Package)),
     unification_set(X, node(ID1, TriggerPackage)),
     not external(node(ID, Package)),  % ignore conflicts for externals
     not attr("hash", node(ID, Package), _).  % ignore conflicts for installed packages

%-----------------------------------------------------------------------------
% Virtual dependencies
%-----------------------------------------------------------------------------

% If the provider is set from the command line, its weight is 0
possible_provider_weight(ProviderNode, VirtualNode, 0, "Set on the command line")
  :- attr("provider_set", ProviderNode, VirtualNode).

% Enforces all virtuals to be provided, if multiple of them are provided together
error(100, "Package '{0}' needs to provide both '{1}' and '{2}' together, but provides only '{1}'", Package, Virtual1, Virtual2)
:- condition_holds(ID, node(X, Package)),
   pkg_fact(Package, provided_together(ID, SetID, Virtual1)),
   pkg_fact(Package, provided_together(ID, SetID, Virtual2)),
   Virtual1 != Virtual2,
   attr("virtual_on_incoming_edges", node(X, Package), Virtual1),
   not attr("virtual_on_incoming_edges", node(X, Package), Virtual2),
   attr("virtual_node", node(_, Virtual1)),
   attr("virtual_node", node(_, Virtual2)).

% if a package depends on a virtual, it's not external and we have a
% provider for that virtual then it depends on the provider
node_depends_on_virtual(PackageNode, Virtual, Type)
  :- attr("dependency_holds", PackageNode, Virtual, Type),
     virtual(Virtual),
     not external(PackageNode).

node_depends_on_virtual(PackageNode, Virtual) :- node_depends_on_virtual(PackageNode, Virtual, Type).

1 { attr("depends_on", PackageNode, ProviderNode, Type) : provider(ProviderNode, node(VirtualID, Virtual)) } 1
  :- node_depends_on_virtual(PackageNode, Virtual, Type).

attr("virtual_on_edge", PackageNode, ProviderNode, Virtual)
  :- attr("dependency_holds", PackageNode, Virtual, Type),
     attr("depends_on", PackageNode, ProviderNode, Type),
     provider(ProviderNode, node(_, Virtual)),
     not external(PackageNode).

% If a virtual node is in the answer set, it must be either a virtual root,
% or used somewhere
:- attr("virtual_node", node(_, Virtual)),
   not attr("virtual_on_incoming_edges", _, Virtual),
   not attr("virtual_root", node(_, Virtual)).

attr("virtual_on_incoming_edges", ProviderNode, Virtual)
  :- attr("virtual_on_edge", _, ProviderNode, Virtual).

% dependencies on virtuals also imply that the virtual is a virtual node
1 { attr("virtual_node", node(0..X-1, Virtual)) : max_dupes(Virtual, X) }
  :- node_depends_on_virtual(PackageNode, Virtual).

% If there's a virtual node, we must select one and only one provider.
% The provider must be selected among the possible providers.

error(100, "'{0}' cannot be a provider for the '{1}' virtual", Package, Virtual)
  :-  attr("provider_set", node(min_dupe_id, Package), node(min_dupe_id, Virtual)),
      not virtual_condition_holds( node(min_dupe_id, Package), Virtual).

error(100, "Cannot find valid provider for virtual {0}", Virtual)
  :- attr("virtual_node", node(X, Virtual)),
     not provider(_, node(X, Virtual)).

error(100, "Cannot select a single provider for virtual '{0}'", Virtual)
  :- attr("virtual_node", node(X, Virtual)),
     2 { provider(P, node(X, Virtual)) }.

% virtual roots imply virtual nodes, and that one provider is a root
attr("virtual_node", VirtualNode) :- attr("virtual_root", VirtualNode).

% If we asked for a virtual root and we have a provider for that,
% then the provider is the root package.
attr("root", PackageNode) :- attr("virtual_root", VirtualNode), provider(PackageNode, VirtualNode).

% The provider is selected among the nodes for which the virtual condition holds
1 { provider(PackageNode, node(X, Virtual)) :
    attr("node", PackageNode), virtual_condition_holds(PackageNode, Virtual) } 1
  :- attr("virtual_node", node(X, Virtual)).

% The provider provides the virtual if some provider condition holds.
virtual_condition_holds(node(ProviderID, Provider), Virtual) :- virtual_condition_holds(ID, node(ProviderID, Provider), Virtual).
virtual_condition_holds(ID, node(ProviderID, Provider), Virtual) :-
   pkg_fact(Provider, provider_condition(ID, Virtual)),
   condition_holds(ID, node(ProviderID, Provider)),
   virtual(Virtual).

% If a "provider" condition holds, but this package is not a provider, do not impose the "provider" condition
do_not_impose(EffectID, node(X, Package))
  :- virtual_condition_holds(ID, node(X, Package), Virtual),
     pkg_fact(Package, condition_effect(ID, EffectID)),
     not provider(node(X, Package), node(_, Virtual)).

% Choose the provider among root specs, if possible
:- provider(ProviderNode, node(min_dupe_id, Virtual)),
   virtual_condition_holds(_, PossibleProvider, Virtual),
   PossibleProvider != ProviderNode,
   explicitly_requested_root(PossibleProvider),
   not explicitly_requested_root(ProviderNode).

% A package cannot be the actual provider for a virtual if it does not
% fulfill the conditions to provide that virtual
:- provider(PackageNode, node(VirtualID, Virtual)),
   not virtual_condition_holds(PackageNode, Virtual),
   internal_error("Virtual when provides not respected").

#defined provided_together/4.

%-----------------------------------------------------------------------------
% Virtual dependency weights
%-----------------------------------------------------------------------------

% A provider has different possible weights depending on its preference. This rule ensures that
% we select the weight, among the possible ones, that minimizes the overall objective function.
1 { provider_weight(DependencyNode, VirtualNode, Weight) :
    possible_provider_weight(DependencyNode, VirtualNode, Weight, _) } 1
 :- provider(DependencyNode, VirtualNode), internal_error("Package provider weights must be unique").

% Any configured provider has a weight based on index in the preference list
possible_provider_weight(node(ProviderID, Provider), node(VirtualID, Virtual), Weight, "default")
  :- provider(node(ProviderID, Provider), node(VirtualID, Virtual)),
     default_provider_preference(Virtual, Provider, Weight).

% Any non-configured provider has a default weight of 100
possible_provider_weight(node(ProviderID, Provider), VirtualNode, 100, "fallback")
  :- provider(node(ProviderID, Provider), VirtualNode).

% do not warn if generated program contains none of these.
#defined virtual/1.
#defined virtual_condition_holds/2.
#defined external/1.
#defined buildable_false/1.
#defined default_provider_preference/3.

%-----------------------------------------------------------------------------
% External semantics
%-----------------------------------------------------------------------------

% if a package is external its version must be one of the external versions
{ external_version(node(ID, Package), Version, Weight):
    pkg_fact(Package, version_declared(Version, Weight, "external")) }
    :- external(node(ID, Package)).

error(100, "Attempted to use external for '{0}' which does not satisfy any configured external spec version", Package)
  :- external(node(ID, Package)),
     not external_version(node(ID, Package), _, _).

error(100, "Attempted to use external for '{0}' which does not satisfy a unique configured external spec version", Package)
  :- external(node(ID, Package)),
     2 { external_version(node(ID, Package), Version, Weight) }.

version_weight(PackageNode, Weight) :- external_version(PackageNode, Version, Weight).
attr("version", PackageNode, Version) :- external_version(PackageNode, Version, Weight).

% if a package is not buildable, only externals or hashed specs are allowed
external(node(ID, Package))
  :- buildable_false(Package),
     attr("node", node(ID, Package)),
     not attr("hash", node(ID, Package), _).

% a package is a real_node if it is not external
real_node(PackageNode) :- attr("node", PackageNode), not external(PackageNode).

% a package is external if we are using an external spec for it
external(PackageNode) :- attr("external_spec_selected", PackageNode, _).

% we can't use the weight for an external version if we don't use the
% corresponding external spec.
:- attr("version",  node(ID, Package), Version),
   version_weight(node(ID, Package), Weight),
   pkg_fact(Package, version_declared(Version, Weight, "external")),
   not external(node(ID, Package)),
   internal_error("External weight used for internal spec").

% determine if an external spec has been selected
attr("external_spec_selected", node(ID, Package), LocalIndex) :-
    attr("external_conditions_hold", node(ID, Package), LocalIndex),
    attr("node", node(ID, Package)),
    not attr("hash", node(ID, Package), _).

% it cannot happen that a spec is external, but none of the external specs
% conditions hold.
error(100, "Attempted to use external for '{0}' which does not satisfy any configured external spec", Package)
 :- external(node(ID, Package)),
    not attr("external_conditions_hold", node(ID, Package), _).

%-----------------------------------------------------------------------------
% Config required semantics
%-----------------------------------------------------------------------------

package_in_dag(Node) :-  attr("node", Node).
package_in_dag(Node) :-  attr("virtual_node", Node).

activate_requirement(node(ID, Package), X) :-
  package_in_dag(node(ID, Package)),
  requirement_group(Package, X),
  not requirement_conditional(Package, X, _).

activate_requirement(node(ID, Package), X) :-
  package_in_dag(node(ID, Package)),
  requirement_group(Package, X),
  condition_holds(Y, node(ID, Package)),
  requirement_conditional(Package, X, Y).

requirement_group_satisfied(node(ID, Package), X) :-
  1 { condition_holds(Y, node(ID, Package)) : requirement_group_member(Y, Package, X) } 1,
  requirement_policy(Package, X, "one_of"),
  activate_requirement(node(ID, Package), X),
  requirement_group(Package, X).

requirement_weight(node(ID, Package), Group, W) :-
  condition_holds(Y, node(ID, Package)),
  requirement_has_weight(Y, W),
  requirement_group_member(Y, Package, Group),
  requirement_policy(Package, Group, "one_of"),
  requirement_group_satisfied(node(ID, Package), Group).

requirement_group_satisfied(node(ID, Package), X) :-
  1 { condition_holds(Y, node(ID, Package)) : requirement_group_member(Y, Package, X) } ,
  requirement_policy(Package, X, "any_of"),
  activate_requirement(node(ID, Package), X),
  requirement_group(Package, X).

% Do not impose requirements, if the conditional requirement is not active
do_not_impose(EffectID, node(ID, Package)) :-
  trigger_condition_holds(TriggerID, node(ID, Package)),
  pkg_fact(Package, condition_trigger(ConditionID, TriggerID)),
  pkg_fact(Package, condition_effect(ConditionID, EffectID)),
  requirement_group_member(ConditionID , Package, RequirementID),
  not activate_requirement(node(ID, Package), RequirementID).

% When we have a required provider, we need to ensure that the provider/2 facts respect
% the requirement. This is particularly important for packages that could provide multiple
% virtuals independently
required_provider(Provider, Virtual)
  :- requirement_group_member(ConditionID, Virtual, RequirementID),
     condition_holds(ConditionID, _),
     virtual(Virtual),
     pkg_fact(Virtual, condition_effect(ConditionID, EffectID)),
     imposed_constraint(EffectID, "node", Provider).

:- provider(node(Y, Package), node(X, Virtual)), required_provider(Provider, Virtual), Package != Provider.

% TODO: the following choice rule allows the solver to add compiler
% flags if their only source is from a requirement. This is overly-specific
% and should use a more-generic approach like in https://github.com/spack/spack/pull/37180

{ attr("node_flag", node(ID, Package), NodeFlag) } :-
  requirement_group_member(ConditionID, Package, RequirementID),
  activate_requirement(node(ID, Package), RequirementID),
  pkg_fact(Package, condition_effect(ConditionID, EffectID)),
  imposed_constraint(EffectID, "node_flag_set", Package, NodeFlag).

requirement_weight(node(ID, Package), Group, W) :-
  W = #min {
    Z : requirement_has_weight(Y, Z), condition_holds(Y, node(ID, Package)), requirement_group_member(Y, Package, Group);
    % We need this to avoid an annoying warning during the solve
    %   concretize.lp:1151:5-11: info: tuple ignored:
    %   #sup@73
    10000
  },
  requirement_policy(Package, Group, "any_of"),
  requirement_group_satisfied(node(ID, Package), Group).

error(100, "cannot satisfy a requirement for package '{0}'.", Package) :-
  activate_requirement(node(ID, Package), X),
  requirement_group(Package, X),
  not requirement_message(Package, X, _),
  not requirement_group_satisfied(node(ID, Package), X).


error(10, Message) :-
  activate_requirement(node(ID, Package), X),
  requirement_group(Package, X),
  requirement_message(Package, X, Message),
  not requirement_group_satisfied(node(ID, Package), X).


#defined requirement_group/2.
#defined requirement_conditional/3.
#defined requirement_message/3.
#defined requirement_group_member/3.
#defined requirement_has_weight/2.
#defined requirement_policy/3.

%-----------------------------------------------------------------------------
% Variant semantics
%-----------------------------------------------------------------------------
% Packages define potentially several definitions for each variant, and depending
% on their attibutes, duplicate nodes for the same package may use different
% definitions. So the variant logic has several jobs:
% A. Associate a variant definition with a node, by VariantID
% B. Associate defaults and attributes (sticky, etc.) for the selected variant ID with the node.
% C. Once these rules are established for a node, select variant value(s) based on them.

% A: Selecting a variant definition

% Variant definitions come from package facts in two ways:
% 1. unconditional variants are always defined on all nodes for a given package
variant_definition(node(NodeID, Package), Name, VariantID) :-
  pkg_fact(Package, variant_definition(Name, VariantID)),
  attr("node", node(NodeID, Package)).

% 2. conditional variants are only defined if the conditions hold for the node
variant_definition(node(NodeID, Package), Name, VariantID) :-
  pkg_fact(Package, variant_condition(Name, VariantID, ConditionID)),
  condition_holds(ConditionID, node(NodeID, Package)).

% If there are any definitions for a variant on a node, the variant is "defined".
variant_defined(PackageNode, Name) :- variant_definition(PackageNode, Name, _).

% We must select one definition for each defined variant on a node.
1 {
  node_has_variant(PackageNode, Name, VariantID) : variant_definition(PackageNode, Name, VariantID)
} 1 :-
  variant_defined(PackageNode, Name).

% Solver must pick the variant definition with the highest id. When conditions hold
% for two or more variant definitions, this prefers the last one defined.
:- node_has_variant(node(NodeID, Package), Name, SelectedVariantID),
   variant_definition(node(NodeID, Package), Name, VariantID),
   VariantID > SelectedVariantID.

% B: Associating applicable package rules with nodes

% The default value for a variant in a package is what is prescribed:
% 1. On the command line
% 2. In packages.yaml (if there's no command line settings)
% 3. In the package.py file (if there are no settings in packages.yaml and the command line)

% -- Associate the definition's default values with the node
% note that the package.py variant defaults are associated with a particular definition, but
% packages.yaml and CLI are associated with just the variant name.
% Also, settings specified on the CLI apply to all duplicates, but always have
% `min_dupe_id` as their node id.
variant_default_value(node(NodeID, Package), VariantName, Value) :-
  node_has_variant(node(NodeID, Package), VariantName, VariantID),
  pkg_fact(Package, variant_default_value_from_package_py(VariantID, Value)),
  not variant_default_value_from_packages_yaml(Package, VariantName, _),
  not attr("variant_default_value_from_cli", node(min_dupe_id, Package), VariantName, _).

variant_default_value(node(NodeID, Package), VariantName, Value) :-
  node_has_variant(node(NodeID, Package), VariantName, _),
  variant_default_value_from_packages_yaml(Package, VariantName, Value),
  not attr("variant_default_value_from_cli", node(min_dupe_id, Package), VariantName, _).

variant_default_value(node(NodeID, Package), VariantName, Value) :-
    node_has_variant(node(NodeID, Package), VariantName, _),
    attr("variant_default_value_from_cli", node(min_dupe_id, Package), VariantName, Value).

% -- Associate the definition's possible values with the node
variant_possible_value(node(NodeID, Package), VariantName, Value) :-
  node_has_variant(node(NodeID, Package), VariantName, VariantID),
  pkg_fact(Package, variant_possible_value(VariantID, Value)).

variant_value_from_disjoint_sets(node(NodeID, Package), VariantName, Value1, Set1) :-
  node_has_variant(node(NodeID, Package), VariantName, VariantID),
  pkg_fact(Package, variant_value_from_disjoint_sets(VariantID, Value1, Set1)).

% -- Associate definition's arity with the node
variant_single_value(node(NodeID, Package), VariantName) :-
  node_has_variant(node(NodeID, Package), VariantName, VariantID),
  not variant_type(VariantID, "multi").

% C: Determining variant values on each node

% if a variant is sticky, but not set, its value is the default value
attr("variant_selected", node(ID, Package), Variant, Value, VariantType, VariantID) :-
  node_has_variant(node(ID, Package), Variant, VariantID),
  variant_default_value(node(ID, Package), Variant, Value),
  pkg_fact(Package, variant_sticky(VariantID)),
  variant_type(VariantID, VariantType),
  not attr("variant_set", node(ID, Package), Variant),
  build(node(ID, Package)).

% we can choose variant values from all the possible values for the node
{
  attr("variant_selected", node(ID, Package), Variant, Value, VariantType, VariantID)
  : variant_possible_value(node(ID, Package), Variant, Value)
} :-
  attr("node", node(ID, Package)),
  node_has_variant(node(ID, Package), Variant, VariantID),
  variant_type(VariantID, VariantType),
  build(node(ID, Package)).

% variant_selected is only needed for reconstruction on the python side, so we can ignore it here
attr("variant_value", PackageNode, Variant, Value) :-
  attr("variant_selected", PackageNode, Variant, Value, VariantType, VariantID).

% a variant cannot be set if it is not a variant on the package
error(100, "Cannot set variant '{0}' for package '{1}' because the variant condition cannot be satisfied for the given spec", Variant, Package)
  :- attr("variant_set", node(ID, Package), Variant),
     not node_has_variant(node(ID, Package), Variant, _),
     build(node(ID, Package)).

% a variant cannot take on a value if it is not a variant of the package
error(100, "Cannot set variant '{0}' for package '{1}' because the variant condition cannot be satisfied for the given spec", Variant, Package)
  :- attr("variant_value", node(ID, Package), Variant, _),
     not node_has_variant(node(ID, Package), Variant, _),
     build(node(ID, Package)).

% at most one variant value for single-valued variants.
error(100, "'{0}' required multiple values for single-valued variant '{1}'", Package, Variant)
  :- attr("node", node(ID, Package)),
     node_has_variant(node(ID, Package), Variant, _),
     variant_single_value(node(ID, Package), Variant),
     build(node(ID, Package)),
     2 { attr("variant_value", node(ID, Package), Variant, Value) }.

error(100, "No valid value for variant '{1}' of package '{0}'", Package, Variant)
  :- attr("node", node(ID, Package)),
     node_has_variant(node(ID, Package), Variant, _),
     build(node(ID, Package)),
     not attr("variant_value", node(ID, Package), Variant, _).

% if a variant is set to anything, it is considered 'set'.
attr("variant_set", PackageNode, Variant) :- attr("variant_set", PackageNode, Variant, _).

% A variant cannot have a value that is not also a possible value
% This only applies to packages we need to build -- concrete packages may
% have been built w/different variants from older/different package versions.
error(10, "'Spec({1}={2})' is not a valid value for '{0}' variant '{1}'", Package, Variant, Value)
 :- attr("variant_value", node(ID, Package), Variant, Value),
    not variant_possible_value(node(ID, Package), Variant, Value),
    build(node(ID, Package)).

% Some multi valued variants accept multiple values from disjoint sets. Ensure that we
% respect that constraint and we don't pick values from more than one set at once
error(100, "{0} variant '{1}' cannot have values '{2}' and '{3}' as they come from disjoint value sets", Package, Variant, Value1, Value2)
  :- attr("variant_value", node(ID, Package), Variant, Value1),
     attr("variant_value", node(ID, Package), Variant, Value2),
     variant_value_from_disjoint_sets(node(ID, Package), Variant, Value1, Set1),
     variant_value_from_disjoint_sets(node(ID, Package), Variant, Value2, Set2),
     Set1 < Set2, % see[1]
     build(node(ID, Package)).

:- attr("variant_set", node(ID, Package), Variant, Value),
   not attr("variant_value", node(ID, Package), Variant, Value).

% The rules below allow us to prefer default values for variants
% whenever possible. If a variant is set in a spec, or if it is
% specified in an external, we score it as if it was a default value.
variant_not_default(node(ID, Package), Variant, Value)
 :- attr("variant_value", node(ID, Package), Variant, Value),
    not variant_default_value(node(ID, Package), Variant, Value),
    % variants set explicitly on the CLI don't count as non-default
    not attr("variant_set", node(ID, Package), Variant, Value),
    % variant values forced by propagation don't count as non-default
    not propagate(node(ID, Package), variant_value(Variant, Value)),
    % variants set on externals that we could use don't count as non-default
    % this makes spack prefer to use an external over rebuilding with the
    % default configuration
    not external_with_variant_set(node(ID, Package), Variant, Value),
    attr("node", node(ID, Package)).

% A default variant value that is not used
variant_default_not_used(node(ID, Package), Variant, Value)
  :- variant_default_value(node(ID, Package), Variant, Value),
     node_has_variant(node(ID, Package), Variant, _),
     not attr("variant_value", node(ID, Package), Variant, Value),
     not propagate(node(ID, Package), variant_value(Variant, _)),
     attr("node", node(ID, Package)).

% The variant is set in an external spec
external_with_variant_set(node(NodeID, Package), Variant, Value)
 :- attr("variant_value", node(NodeID, Package), Variant, Value),
    condition_requirement(TriggerID, "variant_value", Package, Variant, Value),
    trigger_and_effect(Package, TriggerID, EffectID),
    imposed_constraint(EffectID, "external_conditions_hold", Package, _),
    external(node(NodeID, Package)),
    attr("node", node(NodeID, Package)).

% Treat 'none' in a special way - it cannot be combined with other
% values even if the variant is multi-valued
error(100, "{0} variant '{1}' cannot have values '{2}' and 'none'", Package, Variant, Value)
 :- attr("variant_value", node(X, Package), Variant, Value),
    attr("variant_value", node(X, Package), Variant, "none"),
    Value != "none",
    build(node(X, Package)).

% -- Auto variants
% These don't have to be declared in the package. We allow them to spring into
% existence when assigned a value.
variant_possible_value(PackageNode, Variant, Value)
  :- attr("variant_set", PackageNode, Variant, Value), auto_variant(Variant, _).

node_has_variant(PackageNode, Variant, VariantID)
  :- attr("variant_set", PackageNode, Variant, _), auto_variant(Variant, VariantID).

variant_single_value(PackageNode, Variant)
  :- node_has_variant(PackageNode, Variant, VariantID),
     auto_variant(Variant, VariantID),
     not variant_type(VariantID, "multi").

% suppress warnings about this atom being unset.  It's only set if some
% spec or some package sets it, and without this, clingo will give
% warnings like 'info: atom does not occur in any rule head'.
#defined variant_default_value/3.
#defined variant_default_value_from_packages_yaml/3.
#defined variant_default_value_from_package_py/3.

%-----------------------------------------------------------------------------
% Propagation semantics
%-----------------------------------------------------------------------------

% Propagation roots have a corresponding attr("propagate", ...)
propagate(RootNode, PropagatedAttribute) :- attr("propagate", RootNode, PropagatedAttribute).
propagate(RootNode, PropagatedAttribute, EdgeTypes) :- attr("propagate", RootNode, PropagatedAttribute, EdgeTypes).


% Propagate an attribute along edges to child nodes
propagate(ChildNode, PropagatedAttribute) :-
  propagate(ParentNode, PropagatedAttribute),
  depends_on(ParentNode, ChildNode).

propagate(ChildNode, PropagatedAttribute, edge_types(DepType1, DepType2)) :-
  propagate(ParentNode, PropagatedAttribute, edge_types(DepType1, DepType2)),
  depends_on(ParentNode, ChildNode),
  1 { attr("depends_on", ParentNode, ChildNode, DepType1);  attr("depends_on", ParentNode, ChildNode, DepType2) }.

%-----------------------------------------------------------------------------
% Activation of propagated values
%-----------------------------------------------------------------------------

%----
% Variants
%----

% If a variant is propagated, and can be accepted, set its value
attr("variant_selected", PackageNode, Variant, Value, VariantType, VariantID) :-
  propagate(PackageNode, variant_value(Variant, Value)),
  node_has_variant(PackageNode, Variant, VariantID),
  variant_type(VariantID, VariantType),
  variant_possible_value(PackageNode, Variant, Value),
  not attr("variant_set", PackageNode, Variant).

% If a variant is propagated, we cannot have extraneous values
variant_is_propagated(PackageNode, Variant) :-
  attr("variant_value", PackageNode, Variant, Value),
  propagate(PackageNode, variant_value(Variant, Value)),
  not attr("variant_set", PackageNode, Variant).

:- variant_is_propagated(PackageNode, Variant),
   attr("variant_selected", PackageNode, Variant, Value, _, _),
   not propagate(PackageNode, variant_value(Variant, Value)).

%----
% Flags
%----

% A propagated flag implies:
% 1. The same flag type is not set on this node
% 2. This node has the same compiler as the propagation source

propagated_flag(node(PackageID, Package), node_flag(FlagType, Flag, FlagGroup, Source), SourceNode) :-
  propagate(node(PackageID, Package), node_flag(FlagType, Flag, FlagGroup, Source), _),
  not attr("node_flag_set", node(PackageID, Package), node_flag(FlagType, _, _, "literal")),
  % Same compiler as propagation source
  node_compiler(node(PackageID, Package), CompilerID),
  node_compiler(SourceNode, CompilerID),
  attr("propagate", SourceNode, node_flag(FlagType, Flag, FlagGroup, Source), _),
  node(PackageID, Package) != SourceNode,
  not runtime(Package).

attr("node_flag", PackageNode, NodeFlag) :- propagated_flag(PackageNode, NodeFlag, _).

% Cannot propagate the same flag from two distinct sources
error(100, "{0} and {1} cannot both propagate compiler flags '{2}' to {3}", Source1, Source2, Package, FlagType) :-
  propagated_flag(node(ID, Package), node_flag(FlagType, _, _, _), node(_, Source1)),
  propagated_flag(node(ID, Package), node_flag(FlagType, _, _, _), node(_, Source2)),
  Source1 < Source2.

%----
% Compiler constraints
%----

attr("node_compiler_version_satisfies", node(ID, Package), Compiler, Version) :-
  propagate(node(ID, Package), node_compiler_version_satisfies(Compiler, Version)),
  node_compiler(node(ID, Package), CompilerID),
  compiler_name(CompilerID, Compiler),
  not runtime(Package),
  not external(Package).

%-----------------------------------------------------------------------------
% Runtimes
%-----------------------------------------------------------------------------

% Check whether the DAG has any built package
has_built_packages() :- build(X), not external(X).

% If we build packages, the runtime nodes must use an available compiler
1 { node_compiler(PackageNode, CompilerID) : build(PackageNode), not external(PackageNode) } :-
  has_built_packages(),
  runtime(RuntimePackage),
  node_compiler(node(_, RuntimePackage), CompilerID).

%-----------------------------------------------------------------------------
% Platform semantics
%-----------------------------------------------------------------------------

% NOTE: Currently we have a single allowed platform per DAG, therefore there is no
% need to have additional optimization criteria. If we ever add cross-platform dags,
% this needs to be changed.
:- 2 { allowed_platform(Platform) }, internal_error("More than one allowed platform detected").

1 { attr("node_platform", PackageNode, Platform) : allowed_platform(Platform) } 1
  :- attr("node", PackageNode).

% setting platform on a node is a hard constraint
attr("node_platform", PackageNode, Platform)
 :- attr("node", PackageNode), attr("node_platform_set", PackageNode, Platform).

% platform is set if set to anything
attr("node_platform_set", PackageNode) :- attr("node_platform_set", PackageNode, _).

%-----------------------------------------------------------------------------
% OS semantics
%-----------------------------------------------------------------------------
% convert weighted OS declarations to simple one
os(OS) :- os(OS, _).

% one os per node
{ attr("node_os", PackageNode, OS) : os(OS) } :- attr("node", PackageNode).

% can't have a non-buildable OS on a node we need to build
error(100, "Cannot select '{0} os={1}' (operating system '{1}' is not buildable)", Package, OS)
 :- build(node(X, Package)),
    attr("node_os", node(X, Package), OS),
    not buildable_os(OS).

% give OS choice weights according to os declarations
node_os_weight(PackageNode, Weight)
 :- attr("node", PackageNode),
    attr("node_os", PackageNode, OS),
    os(OS, Weight).

% every OS is compatible with itself. We can use `os_compatible` to declare
os_compatible(OS, OS) :- os(OS).

% Transitive compatibility among operating systems
os_compatible(OS1, OS3) :- os_compatible(OS1, OS2), os_compatible(OS2, OS3).

% If an OS is set explicitly respect the value
attr("node_os", PackageNode, OS) :- attr("node_os_set", PackageNode, OS), attr("node", PackageNode).

#defined os_compatible/2.

%-----------------------------------------------------------------------------
% Target semantics
%-----------------------------------------------------------------------------

% Each node has only one target chosen among the known targets
{ attr("node_target", PackageNode, Target) : target(Target) } :- attr("node", PackageNode).

% If a node must satisfy a target constraint, enforce it
error(10, "'{0} target={1}' cannot satisfy constraint 'target={2}'", Package, Target, Constraint)
  :- attr("node_target", node(X, Package), Target),
     attr("node_target_satisfies", node(X, Package), Constraint),
     not target_satisfies(Constraint, Target).

% If a node has a target and the target satisfies a constraint, then the target
% associated with the node satisfies the same constraint
attr("node_target_satisfies", PackageNode, Constraint)
  :- attr("node_target", PackageNode, Target), target_satisfies(Constraint, Target).

% If a node has a target, all of its dependencies must be compatible with that target
error(100, "Cannot find compatible targets for {0} and {1}", Package, Dependency)
  :- depends_on(node(X, Package), node(Y, Dependency)),
     attr("node_target", node(X, Package), Target),
     not node_target_compatible(node(Y, Dependency), Target).

% Intermediate step for performance reasons
% When the integrity constraint above was formulated including this logic
% we suffered a substantial performance penalty
node_target_compatible(PackageNode, Target)
 :- attr("node_target", PackageNode, MyTarget),
    target_compatible(Target, MyTarget).

#defined target_satisfies/2.

% can't use targets on node if the compiler for the node doesn't support them
error(100, "{0} compiler '{2}@{3}' incompatible with 'target={1}'", Package, Target, Compiler, Version)
  :- attr("node_target", node(X, Package), Target),
     node_compiler(node(X, Package), CompilerID),
     not compiler_supports_target(CompilerID, Target),
     compiler_name(CompilerID, Compiler),
     compiler_version(CompilerID, Version),
     build(node(X, Package)).

#defined compiler_supports_target/2.
#defined compiler_available/1.

% if a target is set explicitly, respect it
attr("node_target", PackageNode, Target)
 :- attr("node", PackageNode), attr("node_target_set", PackageNode, Target).

% each node has the weight of its assigned target
target_weight(Target, 0)
 :- attr("node", PackageNode),
    attr("node_target", PackageNode, Target),
    attr("node_target_set", PackageNode, Target).

node_target_weight(PackageNode, MinWeight)
 :- attr("node", PackageNode),
    attr("node_target", PackageNode, Target),
    target(Target),
    MinWeight = #min { Weight : target_weight(Target, Weight) }.

:- attr("node_target", PackageNode, Target), not node_target_weight(PackageNode, _).

% compatibility rules for targets among nodes
node_target_match(ParentNode, DependencyNode)
  :- attr("depends_on", ParentNode, DependencyNode, Type), Type != "build",
     attr("node_target", ParentNode, Target),
     attr("node_target", DependencyNode, Target).

node_target_mismatch(ParentNode, DependencyNode)
  :- attr("depends_on", ParentNode, DependencyNode, Type), Type != "build",
     not node_target_match(ParentNode, DependencyNode).

% disallow reusing concrete specs that don't have a compatible target
error(100, "'{0} target={1}' is not compatible with this machine", Package, Target)
  :- attr("node", node(X, Package)),
     attr("node_target", node(X, Package), Target),
     not target(Target).

%-----------------------------------------------------------------------------
% Compiler semantics
%-----------------------------------------------------------------------------
% There must be only one compiler set per built node.
{ node_compiler(PackageNode, CompilerID) : compiler_id(CompilerID), compiler_available(CompilerID) } :-
    attr("node", PackageNode),
    build(PackageNode).

% Infer the compiler that matches a reused node
node_compiler(PackageNode, CompilerID)
  :- attr("node_compiler_version", PackageNode, CompilerName, CompilerVersion),
     attr("node", PackageNode),
     compiler_name(CompilerID, CompilerName),
     compiler_version(CompilerID, CompilerVersion),
     concrete(PackageNode).

% Expand the internal attribute into "attr("node_compiler_version")
attr("node_compiler_version", PackageNode, CompilerName, CompilerVersion)
  :- node_compiler(PackageNode, CompilerID),
     compiler_name(CompilerID, CompilerName),
     compiler_version(CompilerID, CompilerVersion),
     compiler_available(CompilerID),
     build(PackageNode).

attr("node_compiler", PackageNode, CompilerName)
  :- attr("node_compiler_version", PackageNode, CompilerName, CompilerVersion).

error(100, "No valid compiler version found for '{0}'", Package)
  :- attr("node", node(X, Package)),
     not node_compiler(node(X, Package), _).

% We can't have a compiler be enforced and select the version from another compiler
error(100, "Cannot select a single compiler for package {0}", Package)
 :- attr("node", node(X, Package)),
    2 { attr("node_compiler_version", node(X, Package), C, V) }.

% If the compiler of a node cannot be satisfied, raise
error(10, "No valid compiler for {0} satisfies '%{1}'", Package, Compiler)
  :- attr("node", node(X, Package)),
     attr("node_compiler_version_satisfies", node(X, Package), Compiler, ":"),
     not compiler_version_satisfies(Compiler, ":", _).

% If the compiler of a node must satisfy a constraint, then its version
% must be chosen among the ones that satisfy said constraint
error(100, "Package {0} cannot satisfy '%{1}@{2}'", Package, Compiler, Constraint)
  :- attr("node", node(X, Package)),
     attr("node_compiler_version_satisfies", node(X, Package), Compiler, Constraint),
	 not compiler_version_satisfies(Compiler, Constraint, _).

error(100, "Package {0} cannot satisfy '%{1}@{2}'", Package, Compiler, Constraint)
  :- attr("node", node(X, Package)),
     attr("node_compiler_version_satisfies", node(X, Package), Compiler, Constraint),
     not compiler_version_satisfies(Compiler, Constraint, ID),
     node_compiler(node(X, Package), ID).

% If the node is associated with a compiler and the compiler satisfy a constraint, then
% the compiler associated with the node satisfy the same constraint
attr("node_compiler_version_satisfies", PackageNode, Compiler, Constraint)
  :- node_compiler(PackageNode, CompilerID),
     compiler_name(CompilerID, Compiler),
     compiler_version_satisfies(Compiler, Constraint, CompilerID).

#defined compiler_version_satisfies/3.

% If the compiler version was set from the command line,
% respect it verbatim
error(100, "Cannot set the required compiler: {2}%{0}@{1}", Compiler, Version, Package)
  :- attr("node_compiler_version_set", node(X, Package), Compiler, Version),
     not attr("node_compiler_version", node(X, Package), Compiler, Version).

error(100, "Cannot set the required compiler: {1}%{0}", Compiler, Package)
  :- attr("node_compiler_set", node(X, Package), Compiler),
     not attr("node_compiler_version", node(X, Package), Compiler, _).

% Cannot select a compiler if it is not supported on the OS
% Compilers that are explicitly marked as allowed
% are excluded from this check
error(100, "{0} compiler '%{1}@{2}' incompatible with 'os={3}'", Package, Compiler, Version, OS)
  :- attr("node_os", node(X, Package), OS),
     node_compiler(node(X, Package), CompilerID),
     compiler_name(CompilerID, Compiler),
     compiler_version(CompilerID, Version),
     compiler_os(CompilerID, CompilerOS),
     not os_compatible(CompilerOS, OS),
     build(node(X, Package)).

% If a package and one of its dependencies don't have the
% same compiler there's a mismatch.
compiler_match(PackageNode, DependencyNode)
  :- depends_on(PackageNode, DependencyNode),
     node_compiler(PackageNode, CompilerID),
     node_compiler(DependencyNode, CompilerID).

compiler_mismatch(PackageNode, DependencyNode)
  :- depends_on(PackageNode, DependencyNode),
     not attr("node_compiler_set", DependencyNode, _),
     not compiler_match(PackageNode, DependencyNode).

compiler_mismatch_required(PackageNode, DependencyNode)
  :- depends_on(PackageNode, DependencyNode),
     attr("node_compiler_set", DependencyNode, _),
     not compiler_match(PackageNode, DependencyNode).

#defined compiler_os/3.

% compilers weighted by preference according to packages.yaml
node_compiler_weight(node(ID, Package), Weight)
 :- node_compiler(node(ID, Package), CompilerID),
    compiler_name(CompilerID, Compiler),
    compiler_version(CompilerID, V),
    compiler_weight(CompilerID, Weight).

node_compiler_weight(node(ID, Package), 100)
 :- node_compiler(node(ID, Package), CompilerID),
    compiler_name(CompilerID, Compiler),
    compiler_version(CompilerID, V),
    not compiler_weight(CompilerID, _).

% For the time being, be strict and reuse only if the compiler match one we have on the system
error(100, "Compiler {1}@{2} requested for {0} cannot be found.", Package, Compiler, Version)
 :- attr("node_compiler_version", node(ID, Package), Compiler, Version),
    not node_compiler(node(ID, Package), _).

#defined node_compiler_preference/4.
#defined compiler_weight/3.

%-----------------------------------------------------------------------------
% Compiler flags
%-----------------------------------------------------------------------------

% compiler flags from compilers.yaml are put on nodes if compiler matches
attr("node_flag", PackageNode, node_flag(FlagType, Flag, FlagGroup, CompilerID))
  :- compiler_flag(CompilerID, FlagType, Flag, FlagGroup),
     node_compiler(PackageNode, CompilerID),
     flag_type(FlagType),
     compiler_id(CompilerID),
     compiler_name(CompilerID, CompilerName),
     compiler_version(CompilerID, Version).

attr("node_flag", PackageNode, NodeFlag) :- attr("node_flag_set", PackageNode, NodeFlag).

#defined compiler_flag/4.


%-----------------------------------------------------------------------------
% Installed packages
%-----------------------------------------------------------------------------
% the solver is free to choose at most one installed hash for each package
{ attr("hash", node(ID, Package), Hash) : installed_hash(Package, Hash) } 1
 :- attr("node", node(ID, Package)), internal_error("Package must resolve to at most one hash").

% you can't choose an installed hash for a dev spec
:- attr("hash", PackageNode, Hash), attr("variant_value", PackageNode, "dev_path", _).

% You can't install a hash, if it is not installed
:- attr("hash", node(ID, Package), Hash), not installed_hash(Package, Hash).
% This should be redundant given the constraint above
:- attr("node", PackageNode), 2 { attr("hash", PackageNode, Hash) }.

% if a hash is selected, we impose all the constraints that implies
impose(Hash, PackageNode) :- attr("hash", PackageNode, Hash).

% if we haven't selected a hash for a package, we'll be building it
build(PackageNode) :- not attr("hash", PackageNode, _), attr("node", PackageNode).

% Minimizing builds is tricky. We want a minimizing criterion

% because we want to reuse what is avaialble, but
% we also want things that are built to stick to *default preferences* from
% the package and from the user. We therefore treat built specs differently and apply
% a different set of optimization criteria to them. Spack's *first* priority is to
% reuse what it *can*, but if it builds something, the built specs will respect
% defaults and preferences.  This is implemented by bumping the priority of optimization
% criteria for built specs -- so that they take precedence over the otherwise
% topmost-priority criterion to reuse what is installed.
%
% The priority ranges are:
%   1000+       Optimizations for concretization errors
%   300 - 1000  Highest priority optimizations for valid solutions
%   200 - 299   Shifted priorities for build nodes; correspond to priorities 0 - 99.
%   100 - 199   Unshifted priorities. Currently only includes minimizing #builds and minimizing dupes.
%   0   -  99   Priorities for non-built nodes.
build_priority(PackageNode, 200) :- build(PackageNode), attr("node", PackageNode).
build_priority(PackageNode, 0)   :- not build(PackageNode), attr("node", PackageNode).

% don't assign versions from installed packages unless reuse is enabled
% NOTE: that "installed" means the declared version was only included because
% that package happens to be installed, NOT because it was asked for on the
% command line.  If the user specifies a hash, the origin will be "spec".
%
% TODO: There's a slight inconsistency with this: if the user concretizes
% and installs `foo ^bar`, for some build dependency `bar`, and then later
% does a `spack install --fresh foo ^bar/abcde` (i.e.,the hash of `bar`, it
% currently *won't* force versions for `bar`'s build dependencies -- `--fresh`
% will instead build the latest bar. When we actually include transitive
% build deps in the solve, consider using them as a preference to resolve this.
:- attr("version", node(ID, Package), Version),
   version_weight(node(ID, Package), Weight),
   pkg_fact(Package, version_declared(Version, Weight, "installed")),
   not optimize_for_reuse().

#defined installed_hash/2.

% This statement, which is a hidden feature of clingo, let us avoid cycles in the DAG
#edge (A, B) : depends_on(A, B).


%-----------------------------------------------------------------
% Optimization to avoid errors
%-----------------------------------------------------------------
% Some errors are handled as rules instead of constraints because
% it allows us to explain why something failed.
#minimize{ 0@1000: #true}.

#minimize{ Weight@1000,Msg: error(Weight, Msg) }.
#minimize{ Weight@1000,Msg,Arg1: error(Weight, Msg, Arg1) }.
#minimize{ Weight@1000,Msg,Arg1,Arg2: error(Weight, Msg, Arg1, Arg2) }.
#minimize{ Weight@1000,Msg,Arg1,Arg2,Arg3: error(Weight, Msg, Arg1, Arg2, Arg3) }.
#minimize{ Weight@1000,Msg,Arg1,Arg2,Arg3,Arg4: error(Weight, Msg, Arg1, Arg2, Arg3, Arg4) }.

%-----------------------------------------------------------------------------
% How to optimize the spec (high to low priority)
%-----------------------------------------------------------------------------
% Each criterion below has:
%   1. an opt_criterion(ID, Name) fact that describes the criterion, and
%   2. a `#minimize{ 0@2 : #true }.` statement that ensures the criterion
%      is displayed (clingo doesn't display sums over empty sets by default)

% A condition group specifies one or more specs that must be satisfied.
% Specs declared first are preferred, so we assign increasing weights and
% minimize the weights.
opt_criterion(310, "requirement weight").
#minimize{ 0@310: #true }.
#minimize {
    Weight@310,PackageNode,Group
    : requirement_weight(PackageNode, Group, Weight)
}.

% Try hard to reuse installed packages (i.e., minimize the number built)
opt_criterion(110, "number of packages to build (vs. reuse)").
#minimize { 0@110: #true }.
#minimize { 1@110,PackageNode : build(PackageNode), optimize_for_reuse() }.

opt_criterion(100, "number of nodes from the same package").
#minimize { 0@100: #true }.
#minimize { ID@100,Package : attr("node", node(ID, Package)) }.
#minimize { ID@100,Package : attr("virtual_node", node(ID, Package)) }.
#defined optimize_for_reuse/0.

% Minimize the number of deprecated versions being used
opt_criterion(73, "deprecated versions used").
#minimize{ 0@273: #true }.
#minimize{ 0@73: #true }.
#minimize{
    1@73+Priority,PackageNode
    : attr("deprecated", PackageNode, _),
      not external(PackageNode),
      build_priority(PackageNode, Priority)
}.

% Minimize the:
% 1. Version weight
% 2. Number of variants with a non default value, if not set
% for the root package.
opt_criterion(70, "version badness (roots)").
#minimize{ 0@270: #true }.
#minimize{ 0@70: #true }.
#minimize {
    Weight@70+Priority,PackageNode
    : attr("root", PackageNode),
      version_weight(PackageNode, Weight),
      build_priority(PackageNode, Priority)
}.

opt_criterion(65, "number of non-default variants (roots)").
#minimize{ 0@265: #true }.
#minimize{ 0@65: #true }.
#minimize {
    1@65+Priority,PackageNode,Variant,Value
    : variant_not_default(PackageNode, Variant, Value),
      attr("root", PackageNode),
      build_priority(PackageNode, Priority)
}.

opt_criterion(60, "preferred providers for roots").
#minimize{ 0@260: #true }.
#minimize{ 0@60: #true }.
#minimize{
    Weight@60+Priority,ProviderNode,Virtual
    : provider_weight(ProviderNode, Virtual, Weight),
      attr("root", ProviderNode),
      build_priority(ProviderNode, Priority)
}.

opt_criterion(55, "default values of variants not being used (roots)").
#minimize{ 0@255: #true }.
#minimize{ 0@55: #true }.
#minimize{
    1@55+Priority,PackageNode,Variant,Value
    : variant_default_not_used(PackageNode, Variant, Value),
      attr("root", PackageNode),
      build_priority(PackageNode, Priority)
}.

% Try to use default variants or variants that have been set
opt_criterion(50, "number of non-default variants (non-roots)").
#minimize{ 0@250: #true }.
#minimize{ 0@50: #true }.
#minimize {
    1@50+Priority,PackageNode,Variant,Value
    : variant_not_default(PackageNode, Variant, Value),
      not attr("root", PackageNode),
      build_priority(PackageNode, Priority)
}.

% Minimize the weights of the providers, i.e. use as much as
% possible the most preferred providers
opt_criterion(45, "preferred providers (non-roots)").
#minimize{ 0@245: #true }.
#minimize{ 0@45: #true }.
#minimize{
    Weight@45+Priority,ProviderNode,Virtual
    : provider_weight(ProviderNode, Virtual, Weight),
      not attr("root", ProviderNode),
      build_priority(ProviderNode, Priority)
}.

% Try to minimize the number of compiler mismatches in the DAG.
opt_criterion(40, "compiler mismatches that are not required").
#minimize{ 0@240: #true }.
#minimize{ 0@40: #true }.
#minimize{
    1@40+Priority,PackageNode,node(ID, Dependency)
    : compiler_mismatch(PackageNode, node(ID, Dependency)),
      build_priority(node(ID, Dependency), Priority),
      not runtime(Dependency)
}.

opt_criterion(39, "compiler mismatches that are required").
#minimize{ 0@239: #true }.
#minimize{ 0@39: #true }.
#minimize{
    1@39+Priority,PackageNode,node(ID, Dependency)
    : compiler_mismatch_required(PackageNode, node(ID, Dependency)),
      build_priority(node(ID, Dependency), Priority),
      not runtime(Dependency)
}.

opt_criterion(30, "non-preferred OS's").
#minimize{ 0@230: #true }.
#minimize{ 0@30: #true }.
#minimize{
    Weight@30+Priority,PackageNode
    : node_os_weight(PackageNode, Weight),
      build_priority(PackageNode, Priority)
}.

% Choose more recent versions for nodes
opt_criterion(25, "version badness (non roots)").
#minimize{ 0@225: #true }.
#minimize{ 0@25: #true }.
#minimize{
    Weight@25+Priority,node(X, Package)
    : version_weight(node(X, Package), Weight),
      build_priority(node(X, Package), Priority),
      not attr("root", node(X, Package)),
      not runtime(Package)
}.

% Try to use all the default values of variants
opt_criterion(20, "default values of variants not being used (non-roots)").
#minimize{ 0@220: #true }.
#minimize{ 0@20: #true }.
#minimize{
    1@20+Priority,PackageNode,Variant,Value
    : variant_default_not_used(PackageNode, Variant, Value),
      not attr("root", PackageNode),
      build_priority(PackageNode, Priority)
}.

% Try to use preferred compilers
opt_criterion(15, "non-preferred compilers").
#minimize{ 0@215: #true }.
#minimize{ 0@15: #true }.
#minimize{
    Weight@15+Priority,node(X, Package)
    : node_compiler_weight(node(X, Package), Weight),
      build_priority(node(X, Package), Priority),
      not runtime(Package)
}.

% Minimize the number of mismatches for targets in the DAG, try
% to select the preferred target.
opt_criterion(10, "target mismatches").
#minimize{ 0@210: #true }.
#minimize{ 0@10: #true }.
#minimize{
    1@10+Priority,PackageNode,node(ID, Dependency)
    : node_target_mismatch(PackageNode, node(ID, Dependency)),
      build_priority(node(ID, Dependency), Priority),
      not runtime(Dependency)
}.

opt_criterion(5, "non-preferred targets").
#minimize{ 0@205: #true }.
#minimize{ 0@5: #true }.
#minimize{
    Weight@5+Priority,node(X, Package)
    : node_target_weight(node(X, Package), Weight),
      build_priority(node(X, Package), Priority),
      not runtime(Package)
}.


% Minimize the number of compiler mismatches for runtimes
opt_criterion(4, "compiler mismatches (runtimes)").
#minimize{ 0@204: #true }.
#minimize{ 0@4: #true }.
#minimize{
    1@4,PackageNode,node(ID, Dependency)
    : compiler_mismatch(PackageNode, node(ID, Dependency)), runtime(Dependency)
}.
#minimize{
    1@4,PackageNode,node(ID, Dependency)
    : compiler_mismatch_required(PackageNode, node(ID, Dependency)), runtime(Dependency)
}.


% Choose more recent versions for runtimes
opt_criterion(3, "version badness (runtimes)").
#minimize{ 0@203: #true }.
#minimize{ 0@3: #true }.
#minimize{
    Weight@3,node(X, Package)
    : version_weight(node(X, Package), Weight),
      runtime(Package)
}.

% Choose best target for runtimes
opt_criterion(2, "non-preferred targets (runtimes)").
#minimize{ 0@202: #true }.
#minimize{ 0@2: #true }.
#minimize{
    Weight@2,node(X, Package)
    : node_target_weight(node(X, Package), Weight),
      runtime(Package)
}.

% Choose more recent versions for nodes
opt_criterion(1, "edge wiring").
#minimize{ 0@201: #true }.
#minimize{ 0@1: #true }.
#minimize{
    Weight@1,ParentNode,PackageNode
    : version_weight(PackageNode, Weight),
      not attr("root", PackageNode),
      depends_on(ParentNode, PackageNode)
}.

%-----------
% Notes
%-----------

% [1] Clingo ensures a total ordering among all atoms. We rely on that total ordering
%     to reduce symmetry in the solution by checking `<` instead of `!=` in symmetric
%     cases. These choices are made without loss of generality.
