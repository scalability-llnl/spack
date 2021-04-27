# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from __future__ import print_function

import collections
import copy
import itertools
import os
import pprint
import sys
import time
import types
import warnings
from six import string_types

import archspec.cpu

try:
    import clingo
    # There may be a better way to detect this
    clingo_cffi = hasattr(clingo.Symbol, '_rep')
except ImportError:
    clingo = None  # type: ignore
    clingo_cffi = False

import llnl.util.lang
import llnl.util.tty as tty

import spack
import spack.architecture
import spack.cmd
import spack.compilers
import spack.config
import spack.dependency
import spack.directives
import spack.error
import spack.spec
import spack.package
import spack.package_prefs
import spack.repo
import spack.bootstrap
import spack.variant
import spack.version


if sys.version_info >= (3, 3):
    from collections.abc import Sequence  # novm
else:
    from collections import Sequence


class Timer(object):
    """Simple timer for timing phases of a solve"""
    def __init__(self):
        self.start = time.time()
        self.last = self.start
        self.phases = {}

    def phase(self, name):
        last = self.last
        now = time.time()
        self.phases[name] = now - last
        self.last = now

    def write(self, out=sys.stdout):
        now = time.time()
        out.write("Time:\n")
        for phase, t in self.phases.items():
            out.write("    %-15s%.4f\n" % (phase + ":", t))
        out.write("Total: %.4f\n" % (now - self.start))


def issequence(obj):
    if isinstance(obj, string_types):
        return False
    return isinstance(obj, (Sequence, types.GeneratorType))


def listify(args):
    if len(args) == 1 and issequence(args[0]):
        return list(args[0])
    return list(args)


def packagize(pkg):
    if isinstance(pkg, string_types):
        return spack.repo.path.get_pkg_class(pkg)
    else:
        return pkg


def specify(spec):
    if isinstance(spec, spack.spec.Spec):
        return spec
    return spack.spec.Spec(spec)


class AspObject(object):
    """Object representing a piece of ASP code."""


def _id(thing):
    """Quote string if needed for it to be a valid identifier."""
    if isinstance(thing, AspObject):
        return thing
    elif isinstance(thing, bool):
        return '"%s"' % str(thing)
    elif isinstance(thing, int):
        return str(thing)
    else:
        return '"%s"' % str(thing)


class AspFunction(AspObject):
    def __init__(self, name, args=None):
        self.name = name
        self.args = [] if args is None else args

    def __call__(self, *args):
        return AspFunction(self.name, args)

    def symbol(self, positive=True):
        def argify(arg):
            if isinstance(arg, bool):
                return clingo.String(str(arg))
            elif isinstance(arg, int):
                return clingo.Number(arg)
            else:
                return clingo.String(str(arg))
        return clingo.Function(
            self.name, [argify(arg) for arg in self.args], positive=positive)

    def __getitem___(self, *args):
        self.args[:] = args
        return self

    def __str__(self):
        return "%s(%s)" % (
            self.name, ', '.join(str(_id(arg)) for arg in self.args))

    def __repr__(self):
        return str(self)


class AspFunctionBuilder(object):
    def __getattr__(self, name):
        return AspFunction(name)


fn = AspFunctionBuilder()


def all_compilers_in_config():
    return spack.compilers.all_compilers()


def extend_flag_list(flag_list, new_flags):
    """Extend a list of flags, preserving order and precedence.

    Add new_flags at the end of flag_list.  If any flags in new_flags are
    already in flag_list, they are moved to the end so that they take
    higher precedence on the compile line.

    """
    for flag in new_flags:
        if flag in flag_list:
            flag_list.remove(flag)
        flag_list.append(flag)


def check_same_flags(flag_dict_1, flag_dict_2):
    """Return True if flag dicts contain the same flags regardless of order."""
    types = set(flag_dict_1.keys()).union(set(flag_dict_2.keys()))
    for t in types:
        values1 = set(flag_dict_1.get(t, []))
        values2 = set(flag_dict_2.get(t, []))
        assert values1 == values2


def check_packages_exist(specs):
    """Ensure all packages mentioned in specs exist."""
    repo = spack.repo.path
    for spec in specs:
        for s in spec.traverse():
            try:
                check_passed = repo.exists(s.name) or repo.is_virtual(s.name)
            except Exception as e:
                msg = 'Cannot find package: {0}'.format(str(e))
                check_passed = False
                tty.debug(msg)

            if not check_passed:
                raise spack.repo.UnknownPackageError(str(s.fullname))


class Result(object):
    """Result of an ASP solve."""
    def __init__(self, asp=None):
        self.asp = asp
        self.satisfiable = None
        self.optimal = None
        self.warnings = None
        self.nmodels = 0

        # specs ordered by optimization level
        self.answers = []
        self.cores = []

        # names of optimization criteria
        self.criteria = []

    def print_cores(self):
        for core in self.cores:
            tty.msg(
                "The following constraints are unsatisfiable:",
                *sorted(str(symbol) for symbol in core))


def _normalize_packages_yaml(packages_yaml):
    normalized_yaml = copy.copy(packages_yaml)
    for pkg_name in packages_yaml:
        is_virtual = spack.repo.path.is_virtual(pkg_name)
        if pkg_name == 'all' or not is_virtual:
            continue

        # Remove the virtual entry from the normalized configuration
        data = normalized_yaml.pop(pkg_name)
        is_buildable = data.get('buildable', True)
        if not is_buildable:
            for provider in spack.repo.path.providers_for(pkg_name):
                entry = normalized_yaml.setdefault(provider.name, {})
                entry['buildable'] = False

        externals = data.get('externals', [])
        keyfn = lambda x: spack.spec.Spec(x['spec']).name
        for provider, specs in itertools.groupby(externals, key=keyfn):
            entry = normalized_yaml.setdefault(provider, {})
            entry.setdefault('externals', []).extend(specs)

    return normalized_yaml


class PyclingoDriver(object):
    def __init__(self, cores=True, asp=None):
        """Driver for the Python clingo interface.

        Arguments:
            cores (bool): whether to generate unsatisfiable cores for better
                error reporting.
            asp (file-like): optional stream to write a text-based ASP program
                for debugging or verification.
        """
        global clingo
        if not clingo:
            # TODO: Find a way to vendor the concrete spec
            # in a cross-platform way
            with spack.bootstrap.ensure_bootstrap_configuration():
                clingo_spec = spack.bootstrap.clingo_root_spec()
                clingo_spec._old_concretize()
                spack.bootstrap.make_module_available(
                    'clingo', spec=clingo_spec, install=True
                )
                import clingo
        self.out = asp or llnl.util.lang.Devnull()
        self.cores = cores

    def title(self, name, char):
        self.out.write('\n')
        self.out.write("%" + (char * 76))
        self.out.write('\n')
        self.out.write("%% %s\n" % name)
        self.out.write("%" + (char * 76))
        self.out.write('\n')

    def h1(self, name):
        self.title(name, "=")

    def h2(self, name):
        self.title(name, "-")

    def newline(self):
        self.out.write('\n')

    def fact(self, head):
        """ASP fact (a rule without a body)."""
        symbol = head.symbol() if hasattr(head, 'symbol') else head

        self.out.write("%s.\n" % str(symbol))

        atom = self.backend.add_atom(symbol)
        self.backend.add_rule([atom], [], choice=self.cores)
        if self.cores:
            self.assumptions.append(atom)

    def solve(
            self, solver_setup, specs, dump=None, nmodels=0,
            timers=False, stats=False, tests=False
    ):
        timer = Timer()

        # Initialize the control object for the solver
        self.control = clingo.Control()
        self.control.configuration.solve.models = nmodels
        self.control.configuration.asp.trans_ext = 'all'
        self.control.configuration.asp.eq = '5'
        self.control.configuration.configuration = 'tweety'
        self.control.configuration.solve.parallel_mode = '2'
        self.control.configuration.solver.opt_strategy = "usc,one"

        # set up the problem -- this generates facts and rules
        self.assumptions = []
        with self.control.backend() as backend:
            self.backend = backend
            solver_setup.setup(self, specs, tests=tests)
        timer.phase("setup")

        # read in the main ASP program and display logic -- these are
        # handwritten, not generated, so we load them as resources
        parent_dir = os.path.dirname(__file__)
        self.control.load(os.path.join(parent_dir, 'concretize.lp'))
        self.control.load(os.path.join(parent_dir, "display.lp"))
        timer.phase("load")

        # Grounding is the first step in the solve -- it turns our facts
        # and first-order logic rules into propositional logic.
        self.control.ground([("base", [])])
        timer.phase("ground")

        # With a grounded program, we can run the solve.
        result = Result()
        models = []  # stable models if things go well
        cores = []   # unsatisfiable cores if they do not

        def on_model(model):
            models.append((model.cost, model.symbols(shown=True, terms=True)))

        solve_kwargs = {"assumptions": self.assumptions,
                        "on_model": on_model,
                        "on_core": cores.append}
        if clingo_cffi:
            solve_kwargs["on_unsat"] = cores.append
        solve_result = self.control.solve(**solve_kwargs)
        timer.phase("solve")

        # once done, construct the solve result
        result.satisfiable = solve_result.satisfiable

        def stringify(x):
            if clingo_cffi:
                # Clingo w/ CFFI will throw an exception on failure
                try:
                    return x.string
                except RuntimeError:
                    return str(x)
            else:
                return x.string or str(x)

        if result.satisfiable:
            # build spec from the best model
            builder = SpecBuilder(specs)
            min_cost, best_model = min(models)
            tuples = [
                (sym.name, [stringify(a) for a in sym.arguments])
                for sym in best_model
            ]
            answers = builder.build_specs(tuples)

            # add best spec to the results
            result.answers.append((list(min_cost), 0, answers))

            # pull optimization criteria names out of the solution
            criteria = [
                (int(args[0]), args[1]) for name, args in tuples
                if name == "opt_criterion"
            ]
            result.criteria = [t[1] for t in sorted(criteria, reverse=True)]

            # record the number of models the solver considered
            result.nmodels = len(models)

        elif cores:
            symbols = dict(
                (a.literal, a.symbol)
                for a in self.control.symbolic_atoms
            )
            for core in cores:
                core_symbols = []
                for atom in core:
                    sym = symbols[atom]
                    if sym.name == "rule":
                        sym = sym.arguments[0].string
                    core_symbols.append(sym)
                result.cores.append(core_symbols)

        if timers:
            timer.write()
            print()
        if stats:
            print("Statistics:")
            pprint.pprint(self.control.statistics)

        return result


class SpackSolverSetup(object):
    """Class to set up and run a Spack concretization solve."""

    def __init__(self):
        self.gen = None  # set by setup()
        self.possible_versions = {}
        self.versions_in_package_py = {}
        self.versions_from_externals = {}
        self.possible_virtuals = None
        self.possible_compilers = []
        self.variant_values_from_specs = set()
        self.version_constraints = set()
        self.target_constraints = set()
        self.compiler_version_constraints = set()
        self.post_facts = []

        # id for dummy variables
        self._condition_id_counter = itertools.count()

        # Caches to optimize the setup phase of the solver
        self.target_specs_cache = None

    def pkg_version_rules(self, pkg):
        """Output declared versions of a package.

        This uses self.possible_versions so that we include any versions
        that arise from a spec.
        """
        pkg = packagize(pkg)

        config = spack.config.get("packages")
        version_prefs = config.get(pkg.name, {}).get("version", {})
        priority = dict((v, i) for i, v in enumerate(version_prefs))

        # The keys below show the order of precedence of factors used
        # to select a version when concretizing.  The item with
        # the "largest" key will be selected.
        #
        # NOTE: When COMPARING VERSIONS, the '@develop' version is always
        #       larger than other versions.  BUT when CONCRETIZING,
        #       the largest NON-develop version is selected by default.
        keyfn = lambda v: (
            # ------- Special direction from the user
            # Respect order listed in packages.yaml
            -priority.get(v, 0),

            # The preferred=True flag (packages or packages.yaml or both?)
            pkg.versions.get(v, {}).get('preferred', False),

            # ------- Regular case: use latest non-develop version by default.
            # Avoid @develop version, which would otherwise be the "largest"
            # in straight version comparisons
            not v.isdevelop(),

            # Compare the version itself
            # This includes the logic:
            #    a) develop > everything (disabled by "not v.isdevelop() above)
            #    b) numeric > non-numeric
            #    c) Numeric or string comparison
            v)

        # Compute which versions appear only in packages.yaml
        from_externals = self.versions_from_externals[pkg.name]
        from_package_py = self.versions_in_package_py[pkg.name]
        only_from_externals = from_externals - from_package_py

        # These versions don't need a default weight, as they are
        # already weighted in a more favorable way when accounting
        # for externals. Assigning them a default weight would be
        # equivalent to state that they are also declared in
        # the package.py file
        considered = self.possible_versions[pkg.name] - only_from_externals
        most_to_least_preferred = sorted(considered, key=keyfn, reverse=True)

        for i, v in enumerate(most_to_least_preferred):
            self.gen.fact(fn.version_declared(pkg.name, v, i))

    def spec_versions(self, spec):
        """Return list of clauses expressing spec's version constraints."""
        spec = specify(spec)
        assert spec.name

        if spec.concrete:
            return [fn.version(spec.name, spec.version)]

        if spec.versions == spack.version.ver(":"):
            return []

        # record all version constraints for later
        self.version_constraints.add((spec.name, spec.versions))
        return [fn.version_satisfies(spec.name, spec.versions)]

    def target_ranges(self, spec, single_target_fn):
        target = spec.architecture.target

        # Check if the target is a concrete target
        if str(target) in archspec.cpu.TARGETS:
            return [single_target_fn(spec.name, target)]

        self.target_constraints.add((spec.name, target))
        return [fn.node_target_satisfies(spec.name, target)]

    def conflict_rules(self, pkg):
        for trigger, constraints in pkg.conflicts.items():
            trigger_id = self.condition(spack.spec.Spec(trigger), name=pkg.name)
            self.gen.fact(fn.conflict_trigger(trigger_id))

            for constraint, _ in constraints:
                constraint_id = self.condition(constraint, name=pkg.name)
                self.gen.fact(fn.conflict(pkg.name, trigger_id, constraint_id))
                self.gen.newline()

    def available_compilers(self):
        """Facts about available compilers."""

        self.gen.h2("Available compilers")
        compilers = self.possible_compilers

        compiler_versions = collections.defaultdict(lambda: set())
        for compiler in compilers:
            compiler_versions[compiler.name].add(compiler.version)

        for compiler in sorted(compiler_versions):
            for v in sorted(compiler_versions[compiler]):
                self.gen.fact(fn.compiler_version(compiler, v))

            self.gen.newline()

    def compiler_defaults(self):
        """Set compiler defaults, given a list of possible compilers."""
        self.gen.h2("Default compiler preferences")

        compiler_list = self.possible_compilers.copy()
        compiler_list = sorted(
            compiler_list, key=lambda x: (x.name, x.version), reverse=True)
        ppk = spack.package_prefs.PackagePrefs("all", 'compiler', all=False)
        matches = sorted(compiler_list, key=ppk)

        for i, cspec in enumerate(matches):
            f = fn.default_compiler_preference(cspec.name, cspec.version, i)
            self.gen.fact(f)

        # Enumerate target families. This may be redundant, but compilers with
        # custom versions will be able to concretize properly.
        for entry in spack.compilers.all_compilers_config():
            compiler_entry = entry['compiler']
            cspec = spack.spec.CompilerSpec(compiler_entry['spec'])
            if not compiler_entry.get('target', None):
                continue

            self.gen.fact(fn.compiler_supports_target(
                cspec.name, cspec.version, compiler_entry['target']
            ))

    def compiler_supports_os(self):
        compilers_yaml = spack.compilers.all_compilers_config()
        for entry in compilers_yaml:
            c = spack.spec.CompilerSpec(entry['compiler']['spec'])
            operating_system = entry['compiler']['operating_system']
            self.gen.fact(fn.compiler_supports_os(
                c.name, c.version, operating_system
            ))

    def package_compiler_defaults(self, pkg):
        """Facts about packages' compiler prefs."""

        packages = spack.config.get("packages")
        pkg_prefs = packages.get(pkg.name)
        if not pkg_prefs or "compiler" not in pkg_prefs:
            return

        compiler_list = self.possible_compilers.copy()
        compiler_list = sorted(
            compiler_list, key=lambda x: (x.name, x.version), reverse=True)
        ppk = spack.package_prefs.PackagePrefs(pkg.name, 'compiler', all=False)
        matches = sorted(compiler_list, key=ppk)

        for i, cspec in enumerate(reversed(matches)):
            self.gen.fact(fn.node_compiler_preference(
                pkg.name, cspec.name, cspec.version, -i * 100
            ))

    def pkg_rules(self, pkg, tests):
        pkg = packagize(pkg)

        # versions
        self.pkg_version_rules(pkg)
        self.gen.newline()

        # variants
        for name, variant in sorted(pkg.variants.items()):
            self.gen.fact(fn.variant(pkg.name, name))

            single_value = not variant.multi
            if single_value:
                self.gen.fact(fn.variant_single_value(pkg.name, name))
                self.gen.fact(
                    fn.variant_default_value_from_package_py(
                        pkg.name, name, variant.default)
                )
            else:
                spec_variant = variant.make_default()
                defaults = spec_variant.value
                for val in sorted(defaults):
                    self.gen.fact(
                        fn.variant_default_value_from_package_py(
                            pkg.name, name, val)
                    )

            values = variant.values
            if values is None:
                values = []
            elif isinstance(values, spack.variant.DisjointSetsOfValues):
                union = set()
                # Encode the disjoint sets in the logic program
                for sid, s in enumerate(values.sets):
                    for value in s:
                        self.gen.fact(fn.variant_value_from_disjoint_sets(
                            pkg.name, name, value, sid
                        ))
                    union.update(s)
                values = union

            # make sure that every variant has at least one possible value
            if not values:
                values = [variant.default]

            for value in sorted(values):
                self.gen.fact(fn.variant_possible_value(pkg.name, name, value))

            self.gen.newline()

        # conflicts
        self.conflict_rules(pkg)

        # default compilers for this package
        self.package_compiler_defaults(pkg)

        # virtuals
        self.package_provider_rules(pkg)

        # dependencies
        self.package_dependencies_rules(pkg, tests)

        # virtual preferences
        self.virtual_preferences(
            pkg.name,
            lambda v, p, i: self.gen.fact(
                fn.pkg_provider_preference(pkg.name, v, p, i)
            )
        )

    def condition(self, required_spec, imposed_spec=None, name=None):
        """Generate facts for a dependency or virtual provider condition.

        Arguments:
            required_spec (Spec): the spec that triggers this condition
            imposed_spec (optional, Spec): the sepc with constraints that
                are imposed when this condition is triggered
            name (optional, str): name for `required_spec` (required if
                required_spec is anonymous, ignored if not)

        Returns:
            (int): id of the condition created by this function
        """
        named_cond = required_spec.copy()
        named_cond.name = named_cond.name or name
        assert named_cond.name, "must provide name for anonymous condtions!"

        condition_id = next(self._condition_id_counter)
        self.gen.fact(fn.condition(condition_id))

        # requirements trigger the condition
        requirements = self.checked_spec_clauses(
            named_cond, body=True, required_from=name)
        for pred in requirements:
            self.gen.fact(
                fn.condition_requirement(condition_id, pred.name, *pred.args)
            )

        if imposed_spec:
            imposed_constraints = self.checked_spec_clauses(
                imposed_spec, body=False, required_from=name)
            for pred in imposed_constraints:
                # imposed "node"-like conditions are no-ops
                if pred.name in ("node", "virtual_node"):
                    continue
                self.gen.fact(
                    fn.imposed_constraint(condition_id, pred.name, *pred.args)
                )

        return condition_id

    def package_provider_rules(self, pkg):
        for provider_name in sorted(set(s.name for s in pkg.provided.keys())):
            self.gen.fact(fn.possible_provider(pkg.name, provider_name))

        for provided, whens in pkg.provided.items():
            for when in whens:
                condition_id = self.condition(when, provided, pkg.name)
                self.gen.fact(fn.provider_condition(
                    condition_id, when.name, provided.name
                ))
            self.gen.newline()

    def package_dependencies_rules(self, pkg, tests):
        """Translate 'depends_on' directives into ASP logic."""
        for _, conditions in sorted(pkg.dependencies.items()):
            for cond, dep in sorted(conditions.items()):
                deptypes = dep.type.copy()
                # Skip test dependencies if they're not requested
                if not tests:
                    deptypes.discard("test")

                # ... or if they are requested only for certain packages
                if not isinstance(tests, bool) and pkg.name not in tests:
                    deptypes.discard("test")

                # if there are no dependency types to be considered
                # anymore, don't generate the dependency
                if not deptypes:
                    continue

                condition_id = self.condition(cond, dep.spec, pkg.name)
                self.gen.fact(fn.dependency_condition(
                    condition_id, pkg.name, dep.spec.name
                ))

                for t in sorted(deptypes):
                    # there is a declared dependency of type t
                    self.gen.fact(fn.dependency_type(condition_id, t))

                self.gen.newline()

    def virtual_preferences(self, pkg_name, func):
        """Call func(vspec, provider, i) for each of pkg's provider prefs."""
        config = spack.config.get("packages")
        pkg_prefs = config.get(pkg_name, {}).get("providers", {})
        for vspec, providers in pkg_prefs.items():
            if vspec not in self.possible_virtuals:
                continue

            for i, provider in enumerate(providers):
                func(vspec, provider, i + 10)

    def provider_defaults(self):
        self.gen.h2("Default virtual providers")
        assert self.possible_virtuals is not None
        self.virtual_preferences(
            "all",
            lambda v, p, i: self.gen.fact(
                fn.default_provider_preference(v, p, i))
        )

    def external_packages(self):
        """Facts on external packages, as read from packages.yaml"""
        # Read packages.yaml and normalize it, so that it
        # will not contain entries referring to virtual
        # packages.
        packages_yaml = spack.config.get("packages")
        packages_yaml = _normalize_packages_yaml(packages_yaml)

        self.gen.h1('External packages')
        for pkg_name, data in packages_yaml.items():
            if pkg_name == 'all':
                continue

            # This package does not appear in any repository
            if pkg_name not in spack.repo.path:
                continue

            self.gen.h2('External package: {0}'.format(pkg_name))
            # Check if the external package is buildable. If it is
            # not then "external(<pkg>)" is a fact.
            external_buildable = data.get('buildable', True)
            if not external_buildable:
                self.gen.fact(fn.external_only(pkg_name))

            # Read a list of all the specs for this package
            externals = data.get('externals', [])
            external_specs = [spack.spec.Spec(x['spec']) for x in externals]

            # Compute versions with appropriate weights. This accounts for the
            # fact that we should prefer more recent versions, but specs in
            # packages.yaml may not be ordered in that sense.
            external_versions = [
                (x.version, local_idx)
                for local_idx, x in enumerate(external_specs)
            ]
            external_versions = [
                (v, -(w + 1), local_idx)
                for w, (v, local_idx) in enumerate(sorted(external_versions))
            ]
            for version, weight, id in external_versions:
                self.gen.fact(fn.external_version_declared(
                    pkg_name, str(version), weight, id
                ))

            # Declare external conditions with a local index into packages.yaml
            for local_idx, spec in enumerate(external_specs):
                condition_id = self.condition(spec)
                self.gen.fact(
                    fn.possible_external(condition_id, pkg_name, local_idx)
                )
                self.versions_from_externals[spec.name].add(spec.version)
                self.possible_versions[spec.name].add(spec.version)
                self.gen.newline()

    def preferred_variants(self, pkg_name):
        """Facts on concretization preferences, as read from packages.yaml"""
        preferences = spack.package_prefs.PackagePrefs
        preferred_variants = preferences.preferred_variants(pkg_name)
        if not preferred_variants:
            return

        for variant_name in sorted(preferred_variants):
            variant = preferred_variants[variant_name]
            values = variant.value

            if not isinstance(values, tuple):
                values = (values,)

            # perform validation of the variant and values
            spec = spack.spec.Spec(pkg_name)
            spec.update_variant_validate(variant_name, values)

            for value in values:
                self.variant_values_from_specs.add(
                    (pkg_name, variant.name, value)
                )
                self.gen.fact(fn.variant_default_value_from_packages_yaml(
                    pkg_name, variant.name, value
                ))

    def preferred_targets(self, pkg_name):
        key_fn = spack.package_prefs.PackagePrefs(pkg_name, 'target')

        if not self.target_specs_cache:
            self.target_specs_cache = [
                spack.spec.Spec('target={0}'.format(target_name))
                for target_name in archspec.cpu.TARGETS
            ]

        target_specs = self.target_specs_cache
        preferred_targets = [x for x in target_specs if key_fn(x) < 0]
        if not preferred_targets:
            return

        preferred = preferred_targets[0]
        self.gen.fact(fn.package_target_weight(
            str(preferred.architecture.target), pkg_name, -30
        ))

    def preferred_versions(self, pkg_name):
        packages_yaml = spack.config.get('packages')
        versions = packages_yaml.get(pkg_name, {}).get('version', [])
        if not versions:
            return

        for idx, version in enumerate(reversed(versions)):
            self.gen.fact(
                fn.preferred_version_declared(pkg_name, version, -(idx + 1))
            )

    def flag_defaults(self):
        self.gen.h2("Compiler flag defaults")

        # types of flags that can be on specs
        for flag in spack.spec.FlagMap.valid_compiler_flags():
            self.gen.fact(fn.flag_type(flag))
        self.gen.newline()

        # flags from compilers.yaml
        compilers = all_compilers_in_config()
        for compiler in compilers:
            for name, flags in compiler.flags.items():
                for flag in flags:
                    self.gen.fact(fn.compiler_version_flag(
                        compiler.name, compiler.version, name, flag))

    def checked_spec_clauses(self, *args, **kwargs):
        """Wrap a call to spec clauses into a try/except block that raise
        a comprehensible error message in case of failure.
        """
        requestor = kwargs.pop('required_from', None)
        try:
            clauses = self.spec_clauses(*args, **kwargs)
        except RuntimeError as exc:
            msg = str(exc)
            if requestor:
                msg += ' [required from package "{0}"]'.format(requestor)
            raise RuntimeError(msg)
        return clauses

    def spec_clauses(self, spec, body=False, transitive=True):
        """Return a list of clauses for a spec mandates are true.

        Arguments:
            spec (Spec): the spec to analyze
            body (bool): if True, generate clauses to be used in rule bodies
                (final values) instead of rule heads (setters).
            transitive (bool): if False, don't generate clauses from
                 dependencies (default True)
        """
        clauses = []

        # TODO: do this with consistent suffixes.
        class Head(object):
            node = fn.node
            virtual_node = fn.virtual_node
            node_platform = fn.node_platform_set
            node_os = fn.node_os_set
            node_target = fn.node_target_set
            variant_value = fn.variant_set
            node_compiler = fn.node_compiler_set
            node_compiler_version = fn.node_compiler_version_set
            node_flag = fn.node_flag_set

        class Body(object):
            node = fn.node
            virtual_node = fn.virtual_node
            node_platform = fn.node_platform
            node_os = fn.node_os
            node_target = fn.node_target
            variant_value = fn.variant_value
            node_compiler = fn.node_compiler
            node_compiler_version = fn.node_compiler_version
            node_flag = fn.node_flag

        f = Body if body else Head

        if spec.name:
            clauses.append(
                f.node(spec.name) if not spec.virtual
                else f.virtual_node(spec.name))

        clauses.extend(self.spec_versions(spec))

        # seed architecture at the root (we'll propagate later)
        # TODO: use better semantics.
        arch = spec.architecture
        if arch:
            if arch.platform:
                clauses.append(f.node_platform(spec.name, arch.platform))
            if arch.os:
                clauses.append(f.node_os(spec.name, arch.os))
            if arch.target:
                clauses.extend(self.target_ranges(spec, f.node_target))

        # variants
        for vname, variant in sorted(spec.variants.items()):
            values = variant.value
            if not isinstance(values, (list, tuple)):
                values = [values]

            for value in values:
                # * is meaningless for concretization -- just for matching
                if value == '*':
                    continue

                # validate variant value only if spec not concrete
                if not spec.concrete:
                    reserved_names = spack.directives.reserved_names
                    if not spec.virtual and vname not in reserved_names:
                        try:
                            variant_def = spec.package.variants[vname]
                        except KeyError:
                            msg = 'variant "{0}" not found in package "{1}"'
                            raise RuntimeError(msg.format(vname, spec.name))
                        else:
                            variant_def.validate_or_raise(variant, spec.package)

                clauses.append(f.variant_value(spec.name, vname, value))

                # Tell the concretizer that this is a possible value for the
                # variant, to account for things like int/str values where we
                # can't enumerate the valid values
                self.variant_values_from_specs.add((spec.name, vname, value))

        # compiler and compiler version
        if spec.compiler:
            clauses.append(f.node_compiler(spec.name, spec.compiler.name))

            if spec.compiler.concrete:
                clauses.append(f.node_compiler_version(
                    spec.name, spec.compiler.name, spec.compiler.version))

            elif spec.compiler.versions:
                clauses.append(
                    fn.node_compiler_version_satisfies(
                        spec.name, spec.compiler.name, spec.compiler.versions))
                self.compiler_version_constraints.add(
                    (spec.name, spec.compiler))

        # compiler flags
        for flag_type, flags in spec.compiler_flags.items():
            for flag in flags:
                clauses.append(f.node_flag(spec.name, flag_type, flag))

        # dependencies
        if spec.concrete:
            clauses.append(fn.concrete(spec.name))
            # TODO: add concrete depends_on() facts for concrete dependencies

        # add all clauses from dependencies
        if transitive:
            for dep in spec.traverse(root=False):
                clauses.extend(self.spec_clauses(dep, body, transitive=False))

        return clauses

    def build_version_dict(self, possible_pkgs, specs):
        """Declare any versions in specs not declared in packages."""
        self.possible_versions = collections.defaultdict(set)
        self.versions_in_package_py = collections.defaultdict(set)
        self.versions_from_externals = collections.defaultdict(set)

        for pkg_name in possible_pkgs:
            pkg = spack.repo.get(pkg_name)
            for v in pkg.versions:
                self.versions_in_package_py[pkg_name].add(v)
                self.possible_versions[pkg_name].add(v)

        for spec in specs:
            for dep in spec.traverse():
                if dep.versions.concrete:
                    self.possible_versions[dep.name].add(dep.version)

    def _supported_targets(self, compiler_name, compiler_version, targets):
        """Get a list of which targets are supported by the compiler.

        Results are ordered most to least recent.
        """
        supported = []

        for target in targets:
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")
                    target.optimization_flags(compiler_name, compiler_version)
                supported.append(target)
            except archspec.cpu.UnsupportedMicroarchitecture:
                continue
            except ValueError:
                continue

        return sorted(supported, reverse=True)

    def platform_defaults(self):
        self.gen.h2('Default platform')
        platform = spack.architecture.platform()
        self.gen.fact(fn.node_platform_default(platform))

    def os_defaults(self, specs):
        self.gen.h2('Possible operating systems')
        platform = spack.architecture.platform()

        # create set of OS's to consider
        possible = set([
            platform.front_os, platform.back_os, platform.default_os])
        for spec in specs:
            if spec.architecture and spec.architecture.os:
                possible.add(spec.architecture.os)

        # make directives for possible OS's
        for possible_os in sorted(possible):
            self.gen.fact(fn.os(possible_os))

        # mark this one as default
        self.gen.fact(fn.node_os_default(platform.default_os))

    def target_defaults(self, specs):
        """Add facts about targets and target compatibility."""
        self.gen.h2('Default target')

        platform = spack.architecture.platform()
        uarch = archspec.cpu.TARGETS.get(platform.default)

        self.gen.h2('Target compatibility')

        compatible_targets = [uarch] + uarch.ancestors
        additional_targets_in_family = sorted([
            t for t in archspec.cpu.TARGETS.values()
            if (t.family.name == uarch.family.name and
                t not in compatible_targets)
        ], key=lambda x: len(x.ancestors), reverse=True)
        compatible_targets += additional_targets_in_family
        compilers = self.possible_compilers

        # this loop can be used to limit the number of targets
        # considered. Right now we consider them all, but it seems that
        # many targets can make things slow.
        # TODO: investigate this.
        best_targets = set([uarch.family.name])
        for compiler in sorted(compilers):
            supported = self._supported_targets(
                compiler.name, compiler.version, compatible_targets
            )

            # If we can't find supported targets it may be due to custom
            # versions in the spec, e.g. gcc@foo. Try to match the
            # real_version from the compiler object to get more accurate
            # results.
            if not supported:
                compiler_obj = spack.compilers.compilers_for_spec(compiler)
                compiler_obj = compiler_obj[0]
                supported = self._supported_targets(
                    compiler.name,
                    compiler_obj.real_version,
                    compatible_targets
                )

            if not supported:
                continue

            for target in supported:
                best_targets.add(target.name)
                self.gen.fact(fn.compiler_supports_target(
                    compiler.name, compiler.version, target.name))
                self.gen.fact(fn.compiler_supports_target(
                    compiler.name, compiler.version, uarch.family.name))

        # add any targets explicitly mentioned in specs
        for spec in specs:
            if not spec.architecture or not spec.architecture.target:
                continue

            target = archspec.cpu.TARGETS.get(spec.target.name)
            if not target:
                self.target_ranges(spec, None)
                continue

            if target not in compatible_targets:
                compatible_targets.append(target)

        i = 0
        for target in compatible_targets:
            self.gen.fact(fn.target(target.name))
            self.gen.fact(fn.target_family(target.name, target.family.name))
            for parent in sorted(target.parents):
                self.gen.fact(fn.target_parent(target.name, parent.name))

            # prefer best possible targets; weight others poorly so
            # they're not used unless set explicitly
            if target.name in best_targets:
                self.gen.fact(fn.default_target_weight(target.name, i))
                i += 1
            else:
                self.gen.fact(fn.default_target_weight(target.name, 100))

            self.gen.newline()

    def virtual_providers(self):
        self.gen.h2("Virtual providers")
        assert self.possible_virtuals is not None

        # what provides what
        for vspec in sorted(self.possible_virtuals):
            self.gen.fact(fn.virtual(vspec))
        self.gen.newline()

    def generate_possible_compilers(self, specs):
        compilers = all_compilers_in_config()
        cspecs = set([c.spec for c in compilers])

        # add compiler specs from the input line to possibilities if we
        # don't require compilers to exist.
        strict = spack.concretize.Concretizer().check_for_compiler_existence
        for spec in specs:
            for s in spec.traverse():
                if not s.compiler or not s.compiler.concrete:
                    continue

                if strict and s.compiler not in cspecs:
                    raise spack.concretize.UnavailableCompilerVersionError(
                        s.compiler
                    )
                else:
                    cspecs.add(s.compiler)
                    self.gen.fact(fn.allow_compiler(
                        s.compiler.name, s.compiler.version
                    ))

        return cspecs

    def define_version_constraints(self):
        """Define what version_satisfies(...) means in ASP logic."""
        for pkg_name, versions in sorted(self.version_constraints):
            # version must be *one* of the ones the spec allows.
            allowed_versions = [
                v for v in sorted(self.possible_versions[pkg_name])
                if v.satisfies(versions)
            ]

            # This is needed to account for a variable number of
            # numbers e.g. if both 1.0 and 1.0.2 are possible versions
            exact_match = [v for v in allowed_versions if v == versions]
            if exact_match:
                allowed_versions = exact_match

            # generate facts for each package constraint and the version
            # that satisfies it
            for v in allowed_versions:
                self.gen.fact(fn.version_satisfies(pkg_name, versions, v))

            self.gen.newline()

    def define_virtual_constraints(self):
        """Define versions for constraints on virtuals.

        Must be called before define_version_constraints().
        """
        # aggregate constraints into per-virtual sets
        constraint_map = collections.defaultdict(lambda: set())
        for pkg_name, versions in self.version_constraints:
            if not spack.repo.path.is_virtual(pkg_name):
                continue
            constraint_map[pkg_name].add(versions)

        # extract all the real versions mentioned in version ranges
        def versions_for(v):
            if isinstance(v, spack.version.Version):
                return [v]
            elif isinstance(v, spack.version.VersionRange):
                result = [v.start] if v.start else []
                result += [v.end] if v.end else []
                return result
            elif isinstance(v, spack.version.VersionList):
                return sum((versions_for(e) for e in v), [])
            else:
                raise TypeError("expected version type, found: %s" % type(v))

        # define a set of synthetic possible versions for virtuals, so
        # that `version_satisfies(Package, Constraint, Version)` has the
        # same semantics for virtuals as for regular packages.
        for pkg_name, versions in sorted(constraint_map.items()):
            possible_versions = set(
                sum([versions_for(v) for v in versions], [])
            )
            for version in sorted(possible_versions):
                self.possible_versions[pkg_name].add(version)

    def define_compiler_version_constraints(self):
        compiler_list = spack.compilers.all_compiler_specs()
        compiler_list = list(sorted(set(compiler_list)))

        for pkg_name, cspec in self.compiler_version_constraints:
            for compiler in compiler_list:
                if compiler.satisfies(cspec):
                    self.gen.fact(
                        fn.node_compiler_version_satisfies(
                            pkg_name,
                            cspec.name,
                            cspec.versions,
                            compiler.version
                        )
                    )
        self.gen.newline()

    def define_target_constraints(self):

        def _all_targets_satisfiying(single_constraint):
            allowed_targets = []

            if ':' not in single_constraint:
                return [single_constraint]

            t_min, _, t_max = single_constraint.partition(':')
            for test_target in archspec.cpu.TARGETS.values():
                # Check lower bound
                if t_min and not t_min <= test_target:
                    continue

                # Check upper bound
                if t_max and not t_max >= test_target:
                    continue

                allowed_targets.append(test_target)
            return allowed_targets

        cache = {}
        for spec_name, target_constraint in sorted(self.target_constraints):

            # Construct the list of allowed targets for this constraint
            allowed_targets = []
            for single_constraint in str(target_constraint).split(','):
                if single_constraint not in cache:
                    cache[single_constraint] = _all_targets_satisfiying(
                        single_constraint
                    )
                allowed_targets.extend(cache[single_constraint])

            for target in allowed_targets:
                self.gen.fact(
                    fn.node_target_satisfies(
                        spec_name, target_constraint, target
                    )
                )
            self.gen.newline()

    def define_variant_values(self):
        """Validate variant values from the command line.

        Also add valid variant values from the command line to the
        possible values for a variant.

        """
        # Tell the concretizer about possible values from specs we saw in
        # spec_clauses()
        for pkg, variant, value in sorted(self.variant_values_from_specs):
            self.gen.fact(fn.variant_possible_value(pkg, variant, value))

    def setup(self, driver, specs, tests=False):
        """Generate an ASP program with relevant constraints for specs.

        This calls methods on the solve driver to set up the problem with
        facts and rules from all possible dependencies of the input
        specs, as well as constraints from the specs themselves.

        Arguments:
            specs (list): list of Specs to solve

        """
        self._condition_id_counter = itertools.count()

        # preliminary checks
        check_packages_exist(specs)

        # get list of all possible dependencies
        self.possible_virtuals = set(
            x.name for x in specs if x.virtual
        )
        possible = spack.package.possible_dependencies(
            *specs,
            virtuals=self.possible_virtuals,
            deptype=spack.dependency.all_deptypes
        )
        pkgs = set(possible)

        # driver is used by all the functions below to add facts and
        # rules to generate an ASP program.
        self.gen = driver

        # get possible compilers
        self.possible_compilers = self.generate_possible_compilers(specs)

        # traverse all specs and packages to build dict of possible versions
        self.build_version_dict(possible, specs)

        self.gen.h1('General Constraints')
        self.available_compilers()
        self.compiler_defaults()
        self.compiler_supports_os()

        # architecture defaults
        self.platform_defaults()
        self.os_defaults(specs)
        self.target_defaults(specs)

        self.virtual_providers()
        self.provider_defaults()
        self.external_packages()
        self.flag_defaults()

        self.gen.h1('Package Constraints')
        for pkg in sorted(pkgs):
            self.gen.h2('Package rules: %s' % pkg)
            self.pkg_rules(pkg, tests=tests)
            self.gen.h2('Package preferences: %s' % pkg)
            self.preferred_variants(pkg)
            self.preferred_targets(pkg)
            self.preferred_versions(pkg)

        # Inject dev_path from environment
        env = spack.environment.get_env(None, None)
        if env:
            for spec in sorted(specs):
                for dep in spec.traverse():
                    _develop_specs_from_env(dep, env)

        self.gen.h1('Spec Constraints')
        for spec in sorted(specs):
            self.gen.h2('Spec: %s' % str(spec))
            self.gen.fact(
                fn.virtual_root(spec.name) if spec.virtual
                else fn.root(spec.name)
            )
            for clause in self.spec_clauses(spec):
                self.gen.fact(clause)

        self.gen.h1("Variant Values defined in specs")
        self.define_variant_values()

        self.gen.h1("Virtual Constraints")
        self.define_virtual_constraints()

        self.gen.h1("Version Constraints")
        self.define_version_constraints()

        self.gen.h1("Compiler Version Constraints")
        self.define_compiler_version_constraints()

        self.gen.h1("Target Constraints")
        self.define_target_constraints()


class SpecBuilder(object):
    """Class with actions to rebuild a spec from ASP results."""
    def __init__(self, specs):
        self._result = None
        self._command_line_specs = specs
        self._flag_sources = collections.defaultdict(lambda: set())
        self._flag_compiler_defaults = set()

    def node(self, pkg):
        if pkg not in self._specs:
            self._specs[pkg] = spack.spec.Spec(pkg)

    def _arch(self, pkg):
        arch = self._specs[pkg].architecture
        if not arch:
            arch = spack.spec.ArchSpec()
            self._specs[pkg].architecture = arch
        return arch

    def node_platform(self, pkg, platform):
        self._arch(pkg).platform = platform

    def node_os(self, pkg, os):
        self._arch(pkg).os = os

    def node_target(self, pkg, target):
        self._arch(pkg).target = target

    def variant_value(self, pkg, name, value):
        # FIXME: is there a way not to special case 'dev_path' everywhere?
        if name == 'dev_path':
            self._specs[pkg].variants.setdefault(
                name,
                spack.variant.SingleValuedVariant(name, value)
            )
            return

        if name == 'patches':
            self._specs[pkg].variants.setdefault(
                name,
                spack.variant.MultiValuedVariant(name, value)
            )
            return

        self._specs[pkg].update_variant_validate(name, value)

    def version(self, pkg, version):
        self._specs[pkg].versions = spack.version.ver([version])

    def node_compiler(self, pkg, compiler):
        self._specs[pkg].compiler = spack.spec.CompilerSpec(compiler)

    def node_compiler_version(self, pkg, compiler, version):
        self._specs[pkg].compiler.versions = spack.version.VersionList(
            [version])

    def node_flag_compiler_default(self, pkg):
        self._flag_compiler_defaults.add(pkg)

    def node_flag(self, pkg, flag_type, flag):
        self._specs[pkg].compiler_flags.setdefault(flag_type, []).append(flag)

    def node_flag_source(self, pkg, source):
        self._flag_sources[pkg].add(source)

    def no_flags(self, pkg, flag_type):
        self._specs[pkg].compiler_flags[flag_type] = []

    def external_spec_selected(self, pkg, idx):
        """This means that the external spec and index idx
        has been selected for this package.
        """
        packages_yaml = spack.config.get('packages')
        packages_yaml = _normalize_packages_yaml(packages_yaml)
        spec_info = packages_yaml[pkg]['externals'][int(idx)]
        self._specs[pkg].external_path = spec_info.get('prefix', None)
        self._specs[pkg].external_modules = (
            spack.spec.Spec._format_module_list(spec_info.get('modules', None))
        )
        self._specs[pkg].extra_attributes = spec_info.get(
            'extra_attributes', {}
        )

    def depends_on(self, pkg, dep, type):
        dependency = self._specs[pkg]._dependencies.get(dep)
        if not dependency:
            self._specs[pkg]._add_dependency(
                self._specs[dep], (type,))
        else:
            dependency.add_type(type)

    def reorder_flags(self):
        """Order compiler flags on specs in predefined order.

        We order flags so that any node's flags will take priority over
        those of its dependents.  That is, the deepest node in the DAG's
        flags will appear last on the compile line, in the order they
        were specified.

        The solver determines wihch flags are on nodes; this routine
        imposes order afterwards.
        """
        # nodes with no flags get flag order from compiler
        compilers = dict((c.spec, c) for c in all_compilers_in_config())
        for pkg in self._flag_compiler_defaults:
            spec = self._specs[pkg]
            compiler_flags = compilers[spec.compiler].flags
            check_same_flags(spec.compiler_flags, compiler_flags)
            spec.compiler_flags.update(compiler_flags)

        # index of all specs (and deps) from the command line by name
        cmd_specs = dict(
            (s.name, s)
            for spec in self._command_line_specs
            for s in spec.traverse())

        # iterate through specs with specified flags
        for pkg, sources in self._flag_sources.items():
            spec = self._specs[pkg]

            # order is determined by the DAG.  A spec's flags come after
            # any from its ancestors on the compile line.
            order = [
                s.name
                for s in spec.traverse(order='post', direction='parents')]

            # sort the sources in our DAG order
            sorted_sources = sorted(
                sources, key=lambda s: order.index(s))

            # add flags from each source, lowest to highest precedence
            flags = collections.defaultdict(lambda: [])
            for source_name in sorted_sources:
                source = cmd_specs[source_name]
                for name, flag_list in source.compiler_flags.items():
                    extend_flag_list(flags[name], flag_list)

            check_same_flags(spec.compiler_flags, flags)
            spec.compiler_flags.update(flags)

    def build_specs(self, function_tuples):
        # Functions don't seem to be in particular order in output.  Sort
        # them here so that directives that build objects (like node and
        # node_compiler) are called in the right order.
        function_tuples.sort(key=lambda f: {
            "node": -2,
            "node_compiler": -1,
        }.get(f[0], 0))

        self._specs = {}
        for name, args in function_tuples:
            action = getattr(self, name, None)

            # print out unknown actions so we can display them for debugging
            if not action:
                msg = "%s(%s)" % (name, ", ".join(str(a) for a in args))
                tty.debug(msg)
                continue

            assert action and callable(action)

            # ignore predicates on virtual packages, as they're used for
            # solving but don't construct anything
            pkg = args[0]
            if spack.repo.path.is_virtual(pkg):
                continue

            action(*args)

        # namespace assignment is done after the fact, as it is not
        # currently part of the solve
        for spec in self._specs.values():
            repo = spack.repo.path.repo_for_pkg(spec)
            spec.namespace = repo.namespace

        # fix flags after all specs are constructed
        self.reorder_flags()

        # inject patches -- note that we' can't use set() to unique the
        # roots here, because the specs aren't complete, and the hash
        # function will loop forever.
        roots = [spec.root for spec in self._specs.values()]
        roots = dict((id(r), r) for r in roots)
        for root in roots.values():
            spack.spec.Spec.inject_patches_variant(root)

        # Add external paths to specs with just external modules
        for s in self._specs.values():
            spack.spec.Spec.ensure_external_path_if_external(s)

        env = spack.environment.get_env(None, None)
        for s in self._specs.values():
            _develop_specs_from_env(s, env)

        for s in self._specs.values():
            s._mark_concrete()

        for s in self._specs.values():
            spack.spec.Spec.ensure_no_deprecated(s)

        return self._specs


def _develop_specs_from_env(spec, env):
    dev_info = env.dev_specs.get(spec.name, {}) if env else {}
    if not dev_info:
        return

    path = os.path.normpath(os.path.join(env.path, dev_info['path']))

    if 'dev_path' in spec.variants:
        assert spec.variants['dev_path'].value == path
    else:
        spec.variants.setdefault(
            'dev_path', spack.variant.SingleValuedVariant('dev_path', path)
        )
    spec.constrain(dev_info['spec'])


#
# These are handwritten parts for the Spack ASP model.
#
def solve(specs, dump=(), models=0, timers=False, stats=False, tests=False):
    """Solve for a stable model of specs.

    Arguments:
        specs (list): list of Specs to solve.
        dump (tuple): what to dump
        models (int): number of models to search (default: 0)
    """
    driver = PyclingoDriver()
    if "asp" in dump:
        driver.out = sys.stdout

    # Check upfront that the variants are admissible
    for root in specs:
        for s in root.traverse():
            if s.virtual:
                continue
            spack.spec.Spec.ensure_valid_variants(s)

    setup = SpackSolverSetup()
    return driver.solve(setup, specs, dump, models, timers, stats, tests)
