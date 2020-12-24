from __future__ import absolute_import, print_function

import abc
import code
import collections
import functools
import itertools
import re
from contextlib import contextmanager
# from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple, Union

import six
from z3 import *

import llnl.util.lang
from spack.version import Version, VersionRange, VersionList, ver
from spack.solver.asp import Timer as _Timer


class Timer(_Timer):
    def __init__(self):
        _Timer.__init__(self)
        self.superphase = ''

    def phase(self, name, sep='/'):
        return _Timer.phase(self, self.superphase + sep + name)

    @contextmanager
    def nested_phase(self, subname, sep='/'):
        orig = self.superphase
        self.superphase += sep
        self.superphase += subname
        try:
            self.phase('', sep=sep)
            yield self
        finally:
            self.superphase = orig
            self.phase('')

### Generate the model.

# From ExprRef.__doc__ in z3.py:
"""Constraints, formulas and terms are expressions in Z3.

Expressions are ASTs. Every expression has a sort.
There are three main kinds of expressions:
function applications, quantifiers and bounded variables.
A constant is a function application with 0 arguments.
For quantifier free problems, all expressions are
function applications.
"""
# Z3Expr = Any
# Z3Sort = Any

# _Z = TypeVar('_Z', bound=Z3Sort)
# class IntoZ3(Generic[_Z]):
@six.add_metaclass(abc.ABCMeta)
class IntoZ3(object):
    SORT = None  # type: ClassVar[Type[_Z]]

    def into_z3(self):
        # type: () -> _Z
        return self.extract_z3_expr(self)

    @abc.abstractmethod
    def convert_to_z3(self):
        # type: () -> _Z
        pass

    @classmethod
    @llnl.util.lang.memoized
    def extract_z3_expr(cls, instance):
        # type: (IntoZ3[T]) -> T
        if not is_sort(cls.SORT):
            raise TypeError('{}.SORT was not a z3 sort: {}'.format(cls.__name__, cls.SORT))
        z3_instance = instance.convert_to_z3()
        if not is_expr(z3_instance):
            raise TypeError('Not a z3 instance: {}'.format(z3_instance))
        if not z3_instance.sort() == cls.SORT:
            raise TypeError('Returned z3 object of unexpected sort: {} (sort {}). Expected was {}, from {}.SORT. Instance was: {}.'
                            .format(z3_instance, z3_instance.sort(), cls.SORT, cls.__name__, instance))
        return z3_instance


def assert_no_duplicates(all_values):
    # type: (Iterable[Z3Expr]) -> List[Z3Expr]
    all_values = list(all_values)
    assert len(frozenset(all_values)) == len(all_values), all_values
    return all_values


def ordered_dict(pairs):
    # type: (Iterable[T]) -> collections.OrderedDict[K, T]
    return collections.OrderedDict(pairs)


def wraps(inner_cls):
    def receive_class(outer_cls):
        outer_cls.__doc__ = inner_cls.__doc__
        outer_cls.__name__ = inner_cls.__name__
        return outer_cls
    return receive_class

def enum_type(all_values):
    # type: (Iterable[Z3Expr]) -> Callablee[[Type], Type[IntoZ3]]
    all_values = assert_no_duplicates(all_values)
    def receive_class(cls):
        @delegate_eq_hash(['inner'])
        @wraps(cls)
        class Generated(cls, IntoZ3):
            def __init__(self, inner):
                assert inner in all_values, (inner, all_values)
                self.inner = inner
            def convert_to_z3(self):
                return self.inner
            def __str__(self):
                return str(self.inner)
            def __repr__(self):
                return '{}({!r})'.format(type(self).__name__,
                                         self.inner)
        return Generated
    return receive_class


def tuple_type(fields):
    # type: (collections.OrderedDict[K, IntoZ3]) -> Callable[[Type], Type[IntoZ3[_Z]]]

    def receive_class(cls):
        # type: (Type) -> Type[NamedTuple]
        field_names = list(fields.keys())

        tup = collections.namedtuple(cls.__name__, field_names)

        @wraps(cls)
        class Generated(
            tup,
            cls,
            IntoZ3,
        ):
            # constructor: ClassVar[Callable[[...], _Z]] = None
            def __new__(cls, *args, **kwargs):
                ret = tup.__new__(cls, *args, **kwargs)
                for f_name in field_names:
                    f_cls = fields[f_name]
                    assert hasattr(f_cls, 'convert_to_z3'), f_cls
                    f_val = getattr(ret, f_name)
                    assert isinstance(f_val, f_cls), (f_val, f_cls, cls)
                return ret

            def convert_to_z3(self):
                fields_as_args = tuple(getattr(self, f_name).into_z3() for f_name in field_names)
                return self.constructor(*fields_as_args)

            def __repr__(self):
                return ('{}({})'
                        .format(type(self).__name__,
                                ', '.join(
                                    '{}={!r}'.format(k, getattr(self, k))
                                    for k in field_names
                                )))

        return Generated

    return receive_class


def delegate_eq_hash(field_names):
    # type: (Iterable[str]) -> Callable[[Type], Type]
    field_names = assert_no_duplicates(field_names)
    def receive_class(cls):
        @wraps(cls)
        class Generated(cls):
            def __eq__(self, other):
                return isinstance(other, type(self)) and all(
                    getattr(self, f_name) == getattr(other, f_name)
                    for f_name in field_names
                )
            def __hash__(self):
                return hash(tuple(hash(getattr(self, f_name))
                                  for f_name in field_names))
        return Generated
    return receive_class


def delegate_iter(field):
    # type: (str) -> Callable[[Type], Type]
    def receive_class(cls):
        @wraps(cls)
        class Generated(cls):
            def __iter__(self):
                return iter(getattr(self, field))
        return Generated
    return receive_class


RepoSort, repos = EnumSort('RepoSort', ['spack', 'pypi', 'sonatype'])
(spack, pypi, sonatype) = repos

@enum_type(repos)
class Repo(object):
    SORT = RepoSort

PackageNameSort = StringSort()

@delegate_eq_hash(['name'])
class PackageName(IntoZ3):
    SORT = PackageNameSort

    def __init__(self, name):
        # type: (str) -> None
        self.name = name

    def convert_to_z3(self):
        return StringVal(self.name)

    def version_pin_spec(self, version):
        # type: (SpackVersion) -> str
        return '{}@{}'.format(self, version)

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'PackageName({!r})'.format(self.name)

name_try_repo_map = {
    Repo(spack): ['a', 'b'],
    Repo(pypi): ['c'],
    Repo(sonatype): [],
}

# T = TypeVar('T')

def assume_unique(along, condition_expr_fn, gen_expr_fn,
                  implies_for_expr_fn=None,
                  fmt=(lambda x: "\existsuniq! x \in {} s.t. {}. Case of: x = {}."
                       .format(list(along), gen_expr_fn(x), x))):
    # type: (Iterable[T], Callable[[], Z3Expr], Callable[[T], Z3Expr], str) -> List[Z3Expr]
    along = list(along)

    # See https://stackoverflow.com/questions/43081929/k-out-of-n-constraint-in-z3py/43081930#43081930.
    assumptions = []  # type: List[T]
    bvars = [Bool(six.binary_type(fmt(x))) for x in along]
    assumptions.extend(
        gen_expr_fn(x) == bv
        for x, bv in zip(along, bvars)
    )
    if implies_for_expr_fn is not None:
        assumptions.extend(
            Implies(gen_expr_fn(x), implies_for_expr_fn(x))
            for x in along
        )
    assumptions.append(
        condition_expr_fn() == PbEq([(bv,1) for bv in bvars],
                                    k=1)
    )
    return (assumptions, bvars)


def parse_single_version(version_string):
    # type: (str) -> Version
    ret = ver(version_string)
    if isinstance(ret, Version):
        return ret
    assert isinstance(ret, (VersionRange, VersionList)), ret
    raise TypeError('received version range or list where a *precise* string was expected: {}'
                    .format(version_string))

SpackVersionSort, mk_version, (ver_string) = TupleSort('SpackVersionSort', [StringSort()])

@delegate_eq_hash(['version'])
class SpackVersion(IntoZ3):
    SORT = SpackVersionSort

    def __init__(self, version):
        assert isinstance(version, Version), version
        self.version = version

    def convert_to_z3(self):
        return mk_version(StringVal(self.version.string))

    def into_spack_version(self):
        # type: () -> Version
        return self.version

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self.version)

    def __str__(self):
        return self.version.string


DepSpecStrategySort, strategies = EnumSort('DepSpecStrategySort', ['low', 'high', 'neither'])
(low, high, neither) = strategies

@enum_type(strategies)
class DepSpecStrategy(object):
    SORT = DepSpecStrategySort

DepSpecSort, mk_dep_spec, (get_name, get_low, get_high, get_strategy) = TupleSort(
    'DepSpecSort',
    [PackageNameSort, SpackVersionSort, SpackVersionSort, DepSpecStrategySort],
)

@tuple_type(ordered_dict([('dep_name', PackageName),
                          ('low', SpackVersion),
                          ('high', SpackVersion),
                          ('strategy', DepSpecStrategy)]))
class DepSpec(object):
    SORT = DepSpecSort
    constructor = mk_dep_spec

    def __str__(self):
        # type: () -> str
        if self.strategy.into_z3() == low:
            return '{}@: {} <= x < {}'.format(self.dep_name, self.low.into_spack_version(), self.high.into_spack_version())
        if self.strategy.into_z3() == high:
            return '{}@: {} < x <= {}'.format(self.dep_name, self.low.into_spack_version(), self.high.into_spack_version())
        assert self.strategy.into_z3() == neither, self
        return '{}@: {} == x == {}'.format(self.dep_name, self.low.into_spack_version(), self.high.into_spack_version())


@delegate_iter('dep_specs')
class DepSet(IntoZ3):
    SORT = SeqSort(DepSpecSort)

    def __init__(self, dep_specs):
        # type: (Iterable[DepSpec]) -> None
        self.dep_specs = list(dep_specs)

    def convert_to_z3(self):
        seq_expr = Empty(SeqSort(DepSpecSort))
        for dep_spec in self.dep_specs:
            dep_expr = self.extract_z3_expr(dep_spec)
            seq_expr += Unit(dep_expr)
        return seq_expr


version_dependency_try_map = {
    'a': {
        '0.0.1': {
            'dependencies': {
                'b': {
                    'low': '1.0.0',
                    'high': '2.0.0',
                    'prefer': low,
                },
            },
        },
        '1.0.0': {
            'dependencies': {
                'b': {
                    'low': '1.0.0',
                    'high': '2.0.0',
                    'prefer': low,
                },
            },
        },
        '1.5.2': {
            'dependencies': {
                'b': {
                    'low': '2.1.3',
                    'high': '2.1.3',
                    'prefer': neither,
                },
            },
        },
    },
    'b': {
        '1.0.0': {
            'dependencies': {
                'c': {
                    'low': '1.0.0',
                    'high': '2.0.0',
                    'prefer': low,
                },
            },
        },
        '1.0.1': {
            'dependencies': {
                'c': {
                    'low': '2.0.0',
                    'high': '2.0.0',
                    'prefer': neither,
                },
            },
        },
        '2.0.0': {
            'dependencies': {
                'c': {
                    'low': '3.1.2',
                    'high': '3.1.2',
                    'prefer': neither,
                },
            },
        },
        '2.1.3': {
            'dependencies': {
                'c': {
                    'low': '3.1.3',
                    'high': '3.1.3',
                    'prefer': neither,
                },
            },
        },
    },
    'c': {
        '2.3.5': {
            'dependencies': {},
        },
        '3.0.0': {
            'dependencies': {},
        },
        '3.1.3': {
            'dependencies': {},
        },
    },
}

package_version_try_map = dict(
    (k, [parse_single_version(v) for v in ver.keys()])
    for k, ver in version_dependency_try_map.items()
)

PackageIdentitySort, mk_pkg_identity, (get_id_string,) = TupleSort(
    'PackageIdentitySort', [StringSort()]
)

@delegate_eq_hash(['hash_string'])
@six.add_metaclass(abc.ABCMeta)
class PackageIdentity(IntoZ3):
    SORT = PackageIdentitySort

    def __init__(self, hash_string):
        assert isinstance(hash_string, str), hash_string
        self.hash_string = hash_string

    def convert_to_z3(self):
        return mk_pkg_identity(StringVal(self.hash_string))

    @classmethod
    @abc.abstractmethod
    def from_package_descriptor(cls, pkg_descriptor):
        # type: (Any) -> PackageIdentity
        raise NotImplemented

    def __str__(self):
        return self.hash_string

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self.hash_string)


package_associate_name = Function('package_associate_name',
                                  PackageIdentitySort, PackageNameSort)
package_associate_version = Function('package_associate_version',
                                     PackageIdentitySort, SpackVersionSort)

dependency_matches_version_spec = Function('dependency_matches_version_spec',
                                           DepSpecSort, SpackVersionSort, BoolSort())
use_this_dependency = Function('use_this_dependency',
                               PackageIdentitySort, PackageIdentitySort, BoolSort())

# get_dep_specs = Function('get_dep_specs', PackageIdentitySort, SetSort(DepSpecSort))

use_package = Function('use_package', PackageIdentitySort, BoolSort())

repo_has_package = Function('repo_has_package', PackageIdentitySort, RepoSort, BoolSort())
use_repo_package = Function('use_repo_package', PackageIdentitySort, RepoSort, BoolSort())


@six.add_metaclass(abc.ABCMeta)
class VersionSolverSetup(object):

    def __init__(self):
        self._name_mapping = {}  # type: Dict[PackageIdentity, PackageName]
        self._version_mapping = {}  # type: Dict[PackageIdentity, SpackVersion]
        self._owning_bool_mapping = {}  # type: Dict[PackageIdentity, Bool]
        self._dep_set_mapping = {}  # type: Dict[PackageIdentity, DepSet]

        # type: Dict[PackageName, Dict[SpackVersion, List[PackageIdentity]]]
        self._reverse_lookup = collections.defaultdict(lambda: collections.defaultdict(list))

    def register_package(self, pkg, name, version, owning_bool, dep_set):
        # type: (PackageIdentity, PackageName, SpackVersion, Bool, DepSet) -> None
        assert isinstance(name, PackageName), name
        self._name_mapping[pkg] = name
        assert isinstance(version, SpackVersion), version
        self._version_mapping[pkg] = version
        assert is_bool(owning_bool), owning_bool
        self._owning_bool_mapping[pkg] = owning_bool
        assert isinstance(dep_set, DepSet), dep_set
        self._dep_set_mapping[pkg] = dep_set

        # Add to the reverse lookup table.
        self._reverse_lookup[name][version].append(pkg)

    @abc.abstractmethod
    def all_repos(self):
        # type: () -> Iterable[Repo]
        raise NotImplemented

    @abc.abstractmethod
    def all_repo_packages(self, repo):
        # type: (RepoSort) -> Iterator[PackageIdentity]
        raise NotImplemented

    def extract_package_details(self, pkg):
        # type: (PackageIdentity) -> Tuple[PackageName, SpackVersion, Bool, DepSet]
        name = self._name_mapping[pkg]
        version = self._version_mapping[pkg]
        owning_bool = self._owning_bool_mapping[pkg]
        dep_set = self._dep_set_mapping[pkg]
        return (name, version, owning_bool, dep_set)

    def reverse_lookup_packages(self, name):
        # type: (str) -> Iterable[Tuple[SpackVersion, List[PackageIdentity]]]
        return self._reverse_lookup[name].items()

    def reverse_lookup_package_version(self, name, version):
        # type: (PackageName, SpackVersion) -> Iterable[PackageIdentity]
        return self._reverse_lookup[name][version]


class StaticVersionSolverSetup(VersionSolverSetup):

    def all_repos(self):
        return [Repo(r) for r in repos]

    class StaticPackageIdentity(PackageIdentity):
        @classmethod
        def from_package_descriptor(cls, pkg_descriptor):
            # type: (Tuple[PackageName, SpackVersion]) -> StaticPackageIdentity
            name, version = pkg_descriptor
            s = 'FAKE::[{}]'.format(name.version_pin_spec(version))
            return cls(s)

    def all_repo_packages(self, repo):
        repo_names = frozenset(PackageName(n) for n in name_try_repo_map[repo])
        for name, version_map in version_dependency_try_map.items():
            name = PackageName(name)
            if name not in repo_names:
                continue
            for version_string, dep_var_spec in version_map.items():
                v_spack_ver = parse_single_version(version_string)
                version = SpackVersion(v_spack_ver)

                deps = dep_var_spec['dependencies']
                dep_specs = []  # type: List[DepSpec]
                for dep_name, this_dep_spec in deps.items():
                    low_spack_ver = SpackVersion(parse_single_version(this_dep_spec['low']))
                    high_spack_ver = SpackVersion(parse_single_version(this_dep_spec['high']))
                    prefer_strategy = DepSpecStrategy(this_dep_spec['prefer'])
                    single_dep_spec = DepSpec(dep_name=PackageName(dep_name),
                                              low=low_spack_ver,
                                              high=high_spack_ver,
                                              strategy=prefer_strategy)
                    print(single_dep_spec)
                    dep_specs.append(single_dep_spec)
                dep_set = DepSet(dep_specs)

                var_string = name.version_pin_spec(version)
                pkg = (
                    StaticVersionSolverSetup
                    .StaticPackageIdentity
                    .from_package_descriptor(
                        (name, version_string)))
                pkg_bool_var = Bool(var_string)

                # Registers the package so the ground variables can be set up!
                self.register_package(pkg, name, version, pkg_bool_var, dep_set)

                yield pkg


def perform_manual_grounding(
    assumptions,  # type: List[Z3Expr]
):
    # type: (...) -> VersionSolverSetup
    solver_setup = StaticVersionSolverSetup()
    repo_by_pkg = collections.defaultdict(set)  # type: Dict[Repo, Set[PackageIdentity]]
    repos = frozenset(solver_setup.all_repos())
    for repo in repos:
        for pkg in solver_setup.all_repo_packages(repo):
            repo_by_pkg[pkg].add(repo)
    all_packages = list(repo_by_pkg.keys())  # type: List[PackageIdentity]

    for pkg in all_packages:
        (name, version, owning, dep_set) = solver_setup.extract_package_details(pkg)
        # Ensure that using a package flips on or off the Bool variable previously created for
        # this package.
        assumptions.append(owning == use_package(pkg.into_z3()))

        for dep_spec in dep_set:
            dep_name = dep_spec.dep_name
            low_end = dep_spec.low
            low_version = low_end.into_spack_version()
            high_end = dep_spec.high
            high_version = high_end.into_spack_version()
            strategy = dep_spec.strategy.into_z3()

            all_matching_deps = []  # type: List[PackageIdentity]
            # Here's where we provide dependency ranges!
            for other, dep_pkgs in solver_setup.reverse_lookup_packages(dep_name):
                other_version = other.into_spack_version()
                # Determine whether `other_version` matches the `dep_spec`.
                dep_matched_version = False
                if strategy == low:
                    dep_matched_version = (other_version >= low_version) and (other_version < high_version)
                elif strategy == high:
                    dep_matched_version = (other_version <= high_version) and (other_version >  low_version)
                else:
                    assert strategy == neither, strategy
                    dep_matched_version = (other_version == low_version) and (low_version == high_version)

                if dep_matched_version:
                    print('MATCHED: version {} matches {}'.format(other_version, dep_spec))
                else:
                    print('UNMATCHED: version {} does NOT match {}'.format(other_version, dep_spec))

                # Fill in the now-known value of dependency_matches_version_spec()!
                assumptions.append(
                    dependency_matches_version_spec(dep_spec.into_z3(), other.into_z3()) == dep_matched_version
                )

                # TODO: Convert this into a Spec satisfying any result with that version!
                for dep_pkg in dep_pkgs:
                    # Require the version to have matched to satisfy the dependency!
                    if dep_matched_version:
                        all_matching_deps.append(dep_pkg)
                        assumptions.append(
                            Implies(use_this_dependency(pkg.into_z3(), dep_pkg.into_z3()),
                                    dependency_matches_version_spec(dep_spec.into_z3(), other.into_z3()))
                        )
                    else:
                        # TODO: determine if this is an optimization at all.
                        assumptions.append(
                            use_this_dependency(pkg.into_z3(), dep_pkg.into_z3()) == False
                        )

            # Assume only a single other package is chosen (for this particular package).
            unique_dependency_assumptions, _bvars = assume_unique(
                all_matching_deps,
                condition_expr_fn=(lambda: use_package(pkg.into_z3())),
                gen_expr_fn=(lambda dep_pkg: use_this_dependency(pkg.into_z3(), dep_pkg.into_z3())),
                implies_for_expr_fn=(lambda dep_pkg: use_package(dep_pkg.into_z3())),
                fmt=(lambda dep_pkg: (
                    "use_package(p = {}) => \existsuniq! d \in {{P_dependencies(p)}} s.t. "
                    "use_this_dependency(p, d). case of: d = {}."
                    .format(pkg, dep_pkg))),
            )
            assumptions.extend(unique_dependency_assumptions)

    for pkg, pkg_repos in repo_by_pkg.items():
        # The repo must contain the package in order for us to use it!
        assumptions.extend(
            Implies(
                use_repo_package(pkg.into_z3(), r.into_z3()),
                repo_has_package(pkg.into_z3(), r.into_z3()),
            ) for r in pkg_repos
        )
        for r in repos:
            assumptions.append(
                repo_has_package(pkg.into_z3(), r.into_z3()) == BoolVal(r in pkg_repos)
            )

        # Checking that any package we consume comes from exactly one repo.
        unique_repo_assumptions, _bvars = assume_unique(
            pkg_repos,
            condition_expr_fn=(lambda: use_package(pkg.into_z3())),
            gen_expr_fn=(lambda repo: use_repo_package(pkg.into_z3(), repo.into_z3())),
            fmt=(lambda repo: (
                "use_package(p = {}) => \existsuniq! r \in {{Repo}} s.t. use_repo_package(p, r). "
                "case of: r = {}."
                .format(pkg, repo))),
        )
        assumptions.extend(unique_repo_assumptions)

    return solver_setup


def build_assumptions():
    assumptions = []  # type: List[Z3Expr]

    # Iterate over every package!
    solver_setup = perform_manual_grounding(assumptions=assumptions)

    return (assumptions, solver_setup)


### Execute the model.

def install_check(problems, timer=Timer(), solver=None):
    # type: (Iterable[Z3Expr], Optional[Solver]) -> Solver
    with timer.nested_phase('solve'):
        if solver is None:
            solver = Solver()
        try:
            # NB: Providing the problems all at once is necessary to have `.unsat_core()` reflect
            # them (this seems arbitrary).
            result = solver.check(problems)
        except Z3Exception:
            # But, if one of the problems is malformed (e.g. a non-boolean expression), this will at
            # least narrow down the issue.
            for problem in problems:
                print(problem)
                solver.add(problem)
            raise
        truths = []
        unsat_core = []
        if result == sat:
            m = solver.model()
            for x in m:
                if is_true(m[x]):
                    # x is a Z3 declaration
                    # x() returns the Z3 expression
                    # x.name() returns a string
                    if x.name() == str(x()):
                        truth = x.name()
                    else:
                        truth = "name: {name} == value: {value}".format(name=x.name(), value=x())
                    truths.append(truth)
        elif result == unsat:
            unsat_core = solver.unsat_core()
        return (solver, result, truths, unsat_core)


def generate_then_solve_then_print(initial_requirements, solver=None, timer=Timer()):
    # type: (List[Z3Expr], Optional[Solver], bool) -> Tuple[BoolVarsDict, List[Bool], Solver]
    with timer.nested_phase('build assumptions'):
        (assumptions, solver_setup) = build_assumptions()
    with timer.nested_phase('install check'):
        init_requirements_maybe = list(initial_requirements(solver_setup))
        print('init_requirements: {}'.format(init_requirements_maybe))
        all_exprs = assumptions + init_requirements_maybe
        # print('\n----\n'.join(str(e).decode('utf-8').encode('utf-8') for e in all_exprs))
        (s, result, truths, unsat_core) = install_check(all_exprs, timer=timer, solver=solver)
        if result == sat:
            print('TRUTHS:\n{}'.format('\n'.join(truths)))
        elif result == unknown:
            print('UNKNOWN:\n{}'.format(s.reason_unknown()))
        elif result == unsat:
            print('UNSAT_CORE():\n{}'.format(s.unsat_core()))
        else:
            raise OSError('unrecognized result {}'.format(result))
        return (s, all_exprs, result, truths, unsat_core, init_requirements_maybe, solver_setup)


def solve(timer=Timer(), interact=False):
    # TODO: this only makes it fail to find solutions for all tactics I've tried.
    # robust_tactic = Then(
    #                      Tactic('macro-finder'),
    #                      Tactic('smt'),
    #                      Tactic('symmetry-reduce'),
    #                      Tactic('smt'),
    # )

    def make_initial_requirements_1(version_solver_setup):
        # type: (VersionSolverSetup) -> Iterable[Z3Expr]
        a_1_5_2 = list(version_solver_setup.reverse_lookup_package_version(
            PackageName('a'),
            SpackVersion(parse_single_version('1.5.2')),
        ))[0]
        return [use_package(a_1_5_2.into_z3())]

    with timer.nested_phase('solve 1'):
        s1, e1, r1, tr1, u1, g1, ss1 = generate_then_solve_then_print(
            make_initial_requirements_1,
            timer=timer,
            # solver=robust_tactic.solver()
        )
        with timer.nested_phase('check 1'):
            if r1 == sat:
                print('SUCCESS: SAT!!!!')
            else:
                if interact:
                    print('ERROR: NOT SAT! SHOULD BE!')
                    # code.interact(local=locals())
                else:
                    assert r1 == sat, r1

    def make_initial_requirements_2(version_solver_setup):
        # type: (VersionSolverSetup) -> Iterable[Z3Expr]
        a_1_0_0 = list(version_solver_setup.reverse_lookup_package_version(
            PackageName('a'),
            SpackVersion(parse_single_version('1.0.0')),
        ))[0]
        return [use_package(a_1_0_0.into_z3())]

    with timer.nested_phase('solve 2'):
        s2, e2, r2, tr2, u2, g2, ss2 = generate_then_solve_then_print(
            make_initial_requirements_2,
            timer=timer,
            # solver=robust_tactic.solver()
        )
        with timer.nested_phase('check 2'):
            # TODO: make this correct!
            if r2 == unsat:
                print('SUCCESS: UNSAT!!!!!')
            else:
                if interact:
                    print('ERROR: NOT \'unsat\'! SHOULD  BE!')
                    # code.interact(local=locals())
                else:
                    assert r2 == unsat

    timer.write()

    if interact:
        code.interact(local=locals())

if __name__ == '__main__':
    solve(interact=True)
