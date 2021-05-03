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
from six import string_types

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
import spack.util.classes

# Different models for setup generate different facts
mod_path = spack.paths.models_path
setup_models = spack.util.classes.list_classes("spack.solver.models", mod_path)


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
        self.assumptions = []

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

    def load_logic_programs(self, logic_programs, needs):
        """
        Load one or more logic programs, and ensure all needed are provided.
        """
        # Ensure that all required, needed programs are included
        basenames = [os.path.basename(x) for x in logic_programs]
        missing = [x for x in needs if x not in basenames]

        if missing:
            tty.die("Missing logic programs for solver: %s" % " ".join(needs))

        # read in logic programs associated with different setups
        parent_dir = os.path.dirname(__file__)
        for logic_program in set(logic_programs):

            # If the full path was not provided, it has to be in logic
            if not os.path.exists(logic_program):
                logic_program = os.path.join(parent_dir, 'logic', logic_program)

            # If it still does not exist, we have a problem
            if not os.path.exists(logic_program):
                tty.die("%s does not exist." % logic_program)
            self.control.load(logic_program)

    def init_control(self, nmodels=0):
        """Initialize the controller for the solver.

        In the case that we don't need to run solve, this function is separate
        from solve, below. This function should be called, and then used in
        the context of creating the backend (see solve usage below).
        """
        # Initialize the control object for the solver
        self.control = clingo.Control()
        self.control.configuration.solve.models = nmodels
        self.control.configuration.asp.trans_ext = 'all'
        self.control.configuration.asp.eq = '5'
        self.control.configuration.configuration = 'tweety'
        self.control.configuration.solve.parallel_mode = '2'
        self.control.configuration.solver.opt_strategy = "usc,one"

    def solve(
            self, setups, specs, dump=None, nmodels=0, timers=False, stats=False,
            tests=False, extra_lp=None
    ):
        timer = Timer()

        self.init_control(nmodels)

        # Logic programs are matched to setups
        # Add the "empty" abi compatible rule if we don't have another model
        logic_programs = ["no-op.lp"] if len(setups) == 1 else []
        logic_programs += [extra_lp] if extra_lp else []

        # keep track of needed, required programs
        needs = [getattr(s, 'needs') for s in setups if hasattr(s, 'needs')]

        # set up the problem -- this generates facts and rules
        with self.control.backend() as backend:
            self.backend = backend
            for solver_setup in setups:
                solver_setup.setup(self, specs, tests=tests)
                logic_programs += solver_setup.lp
        timer.phase("setup")

        # Load logic programs and check for missing
        self.load_logic_programs(logic_programs, needs)
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
def solve(specs, dump=(), models=0, timers=False, stats=False, tests=False,
          extra_setup=None, extra_lp=None):
    """Solve for a stable model of specs.

    Arguments:
        specs (list): list of Specs to solve.
        dump (tuple): what to dump
        models (int): number of models to search (default: 0)
        extra_setup (str): an extra setup function and logic program to run.
        extra_lp (str): extra logic program for models.
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

    # By default, we only use one setup (base)
    extra_setups = ([extra_setup] if extra_setup else []) + ['base']
    setups = [s() for s in setup_models if s.name in extra_setups]

    return driver.solve(setups, specs, dump, models, timers, stats,
                        tests, extra_lp)
