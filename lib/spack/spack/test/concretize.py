# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

import pytest
import jinja2

import archspec.cpu

import llnl.util.lang

import spack.architecture
import spack.concretize
import spack.error
import spack.repo

from spack.concretize import find_spec
from spack.spec import Spec
from spack.version import ver
from spack.util.mock_package import MockPackageMultiRepo
import spack.compilers
import spack.platforms.test


def check_spec(abstract, concrete):
    if abstract.versions.concrete:
        assert abstract.versions == concrete.versions

    if abstract.variants:
        for name in abstract.variants:
            avariant = abstract.variants[name]
            cvariant = concrete.variants[name]
            assert avariant.value == cvariant.value

    if abstract.compiler_flags:
        for flag in abstract.compiler_flags:
            aflag = abstract.compiler_flags[flag]
            cflag = concrete.compiler_flags[flag]
            assert set(aflag) <= set(cflag)

    for name in abstract.package.variants:
        assert name in concrete.variants

    for flag in concrete.compiler_flags.valid_compiler_flags():
        assert flag in concrete.compiler_flags

    if abstract.compiler and abstract.compiler.concrete:
        assert abstract.compiler == concrete.compiler

    if abstract.architecture and abstract.architecture.concrete:
        assert abstract.architecture == concrete.architecture


def check_concretize(abstract_spec):
    abstract = Spec(abstract_spec)
    concrete = abstract.concretized()
    assert not abstract.concrete
    assert concrete.concrete
    check_spec(abstract, concrete)
    return concrete


@pytest.fixture(
    params=[
        # no_deps
        'libelf', 'libelf@0.8.13',
        # dag
        'callpath', 'mpileaks', 'libelf',
        # variant
        'mpich+debug', 'mpich~debug', 'mpich debug=True', 'mpich',
        # compiler flags
        'mpich cppflags="-O3"',
        # with virtual
        'mpileaks ^mpi', 'mpileaks ^mpi@:1.1', 'mpileaks ^mpi@2:',
        'mpileaks ^mpi@2.1', 'mpileaks ^mpi@2.2', 'mpileaks ^mpi@2.2',
        'mpileaks ^mpi@:1', 'mpileaks ^mpi@1.2:2',
        # conflict not triggered
        'conflict',
        'conflict%clang~foo',
        'conflict-parent%gcc'
    ]
)
def spec(request):
    """Spec to be concretized"""
    return request.param


@pytest.fixture(params=[
    # Mocking the host detection
    'haswell', 'broadwell', 'skylake', 'icelake',
    # Using preferred targets from packages.yaml
    'icelake-preference', 'cannonlake-preference'
])
def current_host(request, monkeypatch):
    # is_preference is not empty if we want to supply the
    # preferred target via packages.yaml
    cpu, _, is_preference = request.param.partition('-')
    target = archspec.cpu.TARGETS[cpu]

    # this function is memoized, so clear its state for testing
    spack.architecture.get_platform.cache.clear()

    monkeypatch.setattr(spack.platforms.test.Test, 'default', cpu)
    monkeypatch.setattr(spack.platforms.test.Test, 'front_end', cpu)
    if not is_preference:
        monkeypatch.setattr(archspec.cpu, 'host', lambda: target)
        yield target
    else:
        with spack.config.override('packages:all', {'target': [cpu]}):
            yield target

    # clear any test values fetched
    spack.architecture.get_platform.cache.clear()


@pytest.fixture()
def repo_with_changing_recipe(tmpdir_factory, mutable_mock_repo):
    repo_namespace = 'changing'
    repo_dir = tmpdir_factory.mktemp(repo_namespace)

    repo_dir.join('repo.yaml').write("""
repo:
  namespace: changing
""", ensure=True)

    packages_dir = repo_dir.ensure('packages', dir=True)
    root_pkg_str = """
class Root(Package):
    homepage = "http://www.example.com"
    url      = "http://www.example.com/root-1.0.tar.gz"

    version(1.0, sha256='abcde')
    depends_on('changing')
"""
    packages_dir.join('root', 'package.py').write(
        root_pkg_str, ensure=True
    )

    changing_template = """
class Changing(Package):
    homepage = "http://www.example.com"
    url      = "http://www.example.com/changing-1.0.tar.gz"

    version(1.0, sha256='abcde')
{% if not delete_variant %}
    variant('fee', default=True, description='nope')
{% endif %}
    variant('foo', default=True, description='nope')
{% if add_variant %}
    variant('fum', default=True, description='nope')
{% endif %}
"""
    repo = spack.repo.Repo(str(repo_dir))
    mutable_mock_repo.put_first(repo)

    class _ChangingPackage(object):
        def change(self, context):
            # To ensure we get the changed package we need to
            # invalidate the cache
            repo._modules = {}

            t = jinja2.Template(changing_template)
            changing_pkg_str = t.render(**context)
            packages_dir.join('changing', 'package.py').write(
                changing_pkg_str, ensure=True
            )

    _changing_pkg = _ChangingPackage()
    _changing_pkg.change({'delete_variant': False, 'add_variant': False})

    return _changing_pkg


# This must use the mutable_config fixture because the test
# adjusting_default_target_based_on_compiler uses the current_host fixture,
# which changes the config.
@pytest.mark.usefixtures('mutable_config', 'mock_packages')
class TestConcretize(object):
    def test_concretize(self, spec):
        check_concretize(spec)

    def test_concretize_mention_build_dep(self):
        spec = check_concretize('cmake-client ^cmake@3.4.3')
        # Check parent's perspective of child
        dependency = spec.dependencies_dict()['cmake']
        assert set(dependency.deptypes) == set(['build'])
        # Check child's perspective of parent
        cmake = spec['cmake']
        dependent = cmake.dependents_dict()['cmake-client']
        assert set(dependent.deptypes) == set(['build'])

    def test_concretize_preferred_version(self):
        spec = check_concretize('python')
        assert spec.versions == ver('2.7.11')
        spec = check_concretize('python@3.5.1')
        assert spec.versions == ver('3.5.1')

    def test_concretize_with_restricted_virtual(self):
        check_concretize('mpileaks ^mpich2')

        concrete = check_concretize('mpileaks   ^mpich2@1.1')
        assert concrete['mpich2'].satisfies('mpich2@1.1')

        concrete = check_concretize('mpileaks   ^mpich2@1.2')
        assert concrete['mpich2'].satisfies('mpich2@1.2')

        concrete = check_concretize('mpileaks   ^mpich2@:1.5')
        assert concrete['mpich2'].satisfies('mpich2@:1.5')

        concrete = check_concretize('mpileaks   ^mpich2@:1.3')
        assert concrete['mpich2'].satisfies('mpich2@:1.3')

        concrete = check_concretize('mpileaks   ^mpich2@:1.2')
        assert concrete['mpich2'].satisfies('mpich2@:1.2')

        concrete = check_concretize('mpileaks   ^mpich2@:1.1')
        assert concrete['mpich2'].satisfies('mpich2@:1.1')

        concrete = check_concretize('mpileaks   ^mpich2@1.1:')
        assert concrete['mpich2'].satisfies('mpich2@1.1:')

        concrete = check_concretize('mpileaks   ^mpich2@1.5:')
        assert concrete['mpich2'].satisfies('mpich2@1.5:')

        concrete = check_concretize('mpileaks   ^mpich2@1.3.1:1.4')
        assert concrete['mpich2'].satisfies('mpich2@1.3.1:1.4')

    def test_concretize_enable_disable_compiler_existence_check(self):
        with spack.concretize.enable_compiler_existence_check():
            with pytest.raises(
                    spack.concretize.UnavailableCompilerVersionError):
                check_concretize('dttop %gcc@100.100')

        with spack.concretize.disable_compiler_existence_check():
            spec = check_concretize('dttop %gcc@100.100')
            assert spec.satisfies('%gcc@100.100')
            assert spec['dtlink3'].satisfies('%gcc@100.100')

    def test_concretize_with_provides_when(self):
        """Make sure insufficient versions of MPI are not in providers list when
        we ask for some advanced version.
        """
        repo = spack.repo.path
        assert not any(
            s.satisfies('mpich2@:1.0') for s in repo.providers_for('mpi@2.1')
        )
        assert not any(
            s.satisfies('mpich2@:1.1') for s in repo.providers_for('mpi@2.2')
        )
        assert not any(
            s.satisfies('mpich@:1') for s in repo.providers_for('mpi@2')
        )
        assert not any(
            s.satisfies('mpich@:1') for s in repo.providers_for('mpi@3')
        )
        assert not any(
            s.satisfies('mpich2') for s in repo.providers_for('mpi@3')
        )

    def test_provides_handles_multiple_providers_of_same_version(self):
        """
        """
        providers = spack.repo.path.providers_for('mpi@3.0')

        # Note that providers are repo-specific, so we don't misinterpret
        # providers, but vdeps are not namespace-specific, so we can
        # associate vdeps across repos.
        assert Spec('builtin.mock.multi-provider-mpi@1.10.3') in providers
        assert Spec('builtin.mock.multi-provider-mpi@1.10.2') in providers
        assert Spec('builtin.mock.multi-provider-mpi@1.10.1') in providers
        assert Spec('builtin.mock.multi-provider-mpi@1.10.0') in providers
        assert Spec('builtin.mock.multi-provider-mpi@1.8.8') in providers

    def test_different_compilers_get_different_flags(self):
        client = Spec('cmake-client %gcc@4.7.2 platform=test os=fe target=fe' +
                      ' ^cmake %clang@3.5 platform=test os=fe target=fe')
        client.concretize()
        cmake = client['cmake']
        assert set(client.compiler_flags['cflags']) == set(['-O0', '-g'])
        assert set(cmake.compiler_flags['cflags']) == set(['-O3'])
        assert set(client.compiler_flags['fflags']) == set(['-O0', '-g'])
        assert not set(cmake.compiler_flags['fflags'])

    def test_architecture_inheritance(self):
        """test_architecture_inheritance is likely to fail with an
        UnavailableCompilerVersionError if the architecture is concretized
        incorrectly.
        """
        spec = Spec('cmake-client %gcc@4.7.2 os=fe ^ cmake')
        spec.concretize()
        assert spec['cmake'].architecture == spec.architecture

    def test_architecture_deep_inheritance(self, mock_targets):
        """Make sure that indirect dependencies receive architecture
        information from the root even when partial architecture information
        is provided by an intermediate dependency.
        """
        default_dep = ('link', 'build')

        mock_repo = MockPackageMultiRepo()
        bazpkg = mock_repo.add_package('bazpkg', [], [])
        barpkg = mock_repo.add_package('barpkg', [bazpkg], [default_dep])
        mock_repo.add_package('foopkg', [barpkg], [default_dep])

        with spack.repo.use_repositories(mock_repo):
            spec = Spec('foopkg %gcc@4.5.0 os=CNL target=nocona' +
                        ' ^barpkg os=SuSE11 ^bazpkg os=be')
            spec.concretize()

            for s in spec.traverse(root=False):
                assert s.architecture.target == spec.architecture.target

    def test_compiler_flags_from_user_are_grouped(self):
        spec = Spec('a%gcc cflags="-O -foo-flag foo-val" platform=test')
        spec.concretize()
        cflags = spec.compiler_flags['cflags']
        assert any(x == '-foo-flag foo-val' for x in cflags)

    def concretize_multi_provider(self):
        s = Spec('mpileaks ^multi-provider-mpi@3.0')
        s.concretize()
        assert s['mpi'].version == ver('1.10.3')

    def test_concretize_dependent_with_singlevalued_variant_type(self):
        s = Spec('singlevalue-variant-dependent-type')
        s.concretize()

    @pytest.mark.parametrize("spec,version", [
        ('dealii', 'develop'),
        ('xsdk', '0.4.0'),
    ])
    def concretize_difficult_packages(self, a, b):
        """Test a couple of large packages that are often broken due
        to current limitations in the concretizer"""
        s = Spec(a + '@' + b)
        s.concretize()
        assert s[a].version == ver(b)

    def test_concretize_two_virtuals(self):

        """Test a package with multiple virtual dependencies."""
        Spec('hypre').concretize()

    def test_concretize_two_virtuals_with_one_bound(
            self, mutable_mock_repo
    ):
        """Test a package with multiple virtual dependencies and one preset."""
        Spec('hypre ^openblas').concretize()

    def test_concretize_two_virtuals_with_two_bound(self):
        """Test a package with multiple virtual deps and two of them preset."""
        Spec('hypre ^openblas ^netlib-lapack').concretize()

    def test_concretize_two_virtuals_with_dual_provider(self):
        """Test a package with multiple virtual dependencies and force a provider
        that provides both.
        """
        Spec('hypre ^openblas-with-lapack').concretize()

    def test_concretize_two_virtuals_with_dual_provider_and_a_conflict(
            self
    ):
        """Test a package with multiple virtual dependencies and force a
        provider that provides both, and another conflicting package that
        provides one.
        """
        s = Spec('hypre ^openblas-with-lapack ^netlib-lapack')
        with pytest.raises(spack.error.SpackError):
            s.concretize()

    def test_no_matching_compiler_specs(self, mock_low_high_config):
        # only relevant when not building compilers as needed
        with spack.concretize.enable_compiler_existence_check():
            s = Spec('a %gcc@0.0.0')
            with pytest.raises(
                    spack.concretize.UnavailableCompilerVersionError):
                s.concretize()

    def test_no_compilers_for_arch(self):
        s = Spec('a arch=linux-rhel0-x86_64')
        with pytest.raises(spack.error.SpackError):
            s.concretize()

    def test_virtual_is_fully_expanded_for_callpath(self):
        # force dependence on fake "zmpi" by asking for MPI 10.0
        spec = Spec('callpath ^mpi@10.0')
        assert 'mpi' in spec._dependencies
        assert 'fake' not in spec
        spec.concretize()
        assert 'zmpi' in spec._dependencies
        assert all('mpi' not in d._dependencies for d in spec.traverse())
        assert 'zmpi' in spec
        assert 'mpi' in spec
        assert 'fake' in spec._dependencies['zmpi'].spec

    def test_virtual_is_fully_expanded_for_mpileaks(
            self
    ):
        spec = Spec('mpileaks ^mpi@10.0')
        assert 'mpi' in spec._dependencies
        assert 'fake' not in spec
        spec.concretize()
        assert 'zmpi' in spec._dependencies
        assert 'callpath' in spec._dependencies
        assert 'zmpi' in spec._dependencies['callpath'].spec._dependencies
        assert 'fake' in spec._dependencies['callpath'].spec._dependencies[
            'zmpi'].spec._dependencies  # NOQA: ignore=E501
        assert all('mpi' not in d._dependencies for d in spec.traverse())
        assert 'zmpi' in spec
        assert 'mpi' in spec

    def test_my_dep_depends_on_provider_of_my_virtual_dep(self):
        spec = Spec('indirect-mpich')
        spec.normalize()
        spec.concretize()

    @pytest.mark.parametrize('compiler_str', [
        'clang', 'gcc', 'gcc@4.5.0', 'clang@:3.3.0'
    ])
    def test_compiler_inheritance(self, compiler_str):
        spec_str = 'mpileaks %{0}'.format(compiler_str)
        spec = Spec(spec_str).concretized()
        assert spec['libdwarf'].compiler.satisfies(compiler_str)
        assert spec['libelf'].compiler.satisfies(compiler_str)

    def test_external_package(self):
        spec = Spec('externaltool%gcc')
        spec.concretize()
        assert spec['externaltool'].external_path == '/path/to/external_tool'
        assert 'externalprereq' not in spec
        assert spec['externaltool'].compiler.satisfies('gcc')

    def test_external_package_module(self):
        # No tcl modules on darwin/linux machines
        # TODO: improved way to check for this.
        platform = spack.architecture.real_platform().name
        if platform == 'darwin' or platform == 'linux':
            return

        spec = Spec('externalmodule')
        spec.concretize()
        assert spec['externalmodule'].external_modules == ['external-module']
        assert 'externalprereq' not in spec
        assert spec['externalmodule'].compiler.satisfies('gcc')

    def test_nobuild_package(self):
        """Test that a non-buildable package raise an error if no specs
        in packages.yaml are compatible with the request.
        """
        spec = Spec('externaltool%clang')
        with pytest.raises(spack.error.SpecError):
            spec.concretize()

    def test_external_and_virtual(self):
        spec = Spec('externaltest')
        spec.concretize()
        assert spec['externaltool'].external_path == '/path/to/external_tool'
        assert spec['stuff'].external_path == '/path/to/external_virtual_gcc'
        assert spec['externaltool'].compiler.satisfies('gcc')
        assert spec['stuff'].compiler.satisfies('gcc')

    def test_find_spec_parents(self):
        """Tests the spec finding logic used by concretization. """
        s = Spec.from_literal({
            'a +foo': {
                'b +foo': {
                    'c': None,
                    'd+foo': None
                },
                'e +foo': None
            }
        })

        assert 'a' == find_spec(s['b'], lambda s: '+foo' in s).name

    def test_find_spec_children(self):
        s = Spec.from_literal({
            'a': {
                'b +foo': {
                    'c': None,
                    'd+foo': None
                },
                'e +foo': None
            }
        })

        assert 'd' == find_spec(s['b'], lambda s: '+foo' in s).name

        s = Spec.from_literal({
            'a': {
                'b +foo': {
                    'c+foo': None,
                    'd': None
                },
                'e +foo': None
            }
        })

        assert 'c' == find_spec(s['b'], lambda s: '+foo' in s).name

    def test_find_spec_sibling(self):

        s = Spec.from_literal({
            'a': {
                'b +foo': {
                    'c': None,
                    'd': None
                },
                'e +foo': None
            }
        })

        assert 'e' == find_spec(s['b'], lambda s: '+foo' in s).name
        assert 'b' == find_spec(s['e'], lambda s: '+foo' in s).name

        s = Spec.from_literal({
            'a': {
                'b +foo': {
                    'c': None,
                    'd': None
                },
                'e': {
                    'f +foo': None
                }
            }
        })

        assert 'f' == find_spec(s['b'], lambda s: '+foo' in s).name

    def test_find_spec_self(self):
        s = Spec.from_literal({
            'a': {
                'b +foo': {
                    'c': None,
                    'd': None
                },
                'e': None
            }
        })
        assert 'b' == find_spec(s['b'], lambda s: '+foo' in s).name

    def test_find_spec_none(self):
        s = Spec.from_literal({
            'a': {
                'b': {
                    'c': None,
                    'd': None
                },
                'e': None
            }
        })
        assert find_spec(s['b'], lambda s: '+foo' in s) is None

    def test_compiler_child(self):
        s = Spec('mpileaks%clang target=x86_64 ^dyninst%gcc')
        s.concretize()
        assert s['mpileaks'].satisfies('%clang')
        assert s['dyninst'].satisfies('%gcc')

    def test_conflicts_in_spec(self, conflict_spec):
        s = Spec(conflict_spec)
        with pytest.raises(spack.error.SpackError):
            s.concretize()

    def test_conflict_in_all_directives_true(self):
        s = Spec('when-directives-true')
        with pytest.raises(spack.error.SpackError):
            s.concretize()

    @pytest.mark.parametrize('spec_str', [
        'conflict@10.0%clang+foo'
    ])
    def test_no_conflict_in_external_specs(self, spec_str):
        # Modify the configuration to have the spec with conflict
        # registered as an external
        ext = Spec(spec_str)
        data = {
            'externals': [
                {'spec': spec_str,
                 'prefix': '/fake/path'}
            ]
        }
        spack.config.set("packages::{0}".format(ext.name), data)
        ext.concretize()  # failure raises exception

    def test_regression_issue_4492(self):
        # Constructing a spec which has no dependencies, but is otherwise
        # concrete is kind of difficult. What we will do is to concretize
        # a spec, and then modify it to have no dependency and reset the
        # cache values.

        s = Spec('mpileaks')
        s.concretize()

        # Check that now the Spec is concrete, store the hash
        assert s.concrete

        # Remove the dependencies and reset caches
        s._dependencies.clear()
        s._concrete = False

        assert not s.concrete

    @pytest.mark.regression('7239')
    def test_regression_issue_7239(self):
        # Constructing a SpecBuildInterface from another SpecBuildInterface
        # results in an inconsistent MRO

        # Normal Spec
        s = Spec('mpileaks')
        s.concretize()

        assert llnl.util.lang.ObjectWrapper not in type(s).__mro__

        # Spec wrapped in a build interface
        build_interface = s['mpileaks']
        assert llnl.util.lang.ObjectWrapper in type(build_interface).__mro__

        # Mimics asking the build interface from a build interface
        build_interface = s['mpileaks']['mpileaks']
        assert llnl.util.lang.ObjectWrapper in type(build_interface).__mro__

    @pytest.mark.regression('7705')
    def test_regression_issue_7705(self):
        # spec.package.provides(name) doesn't account for conditional
        # constraints in the concretized spec
        s = Spec('simple-inheritance~openblas')
        s.concretize()

        assert not s.package.provides('lapack')

    @pytest.mark.regression('7941')
    def test_regression_issue_7941(self):
        # The string representation of a spec containing
        # an explicit multi-valued variant and a dependency
        # might be parsed differently than the originating spec
        s = Spec('a foobar=bar ^b')
        t = Spec(str(s))

        s.concretize()
        t.concretize()

        assert s.dag_hash() == t.dag_hash()

    @pytest.mark.parametrize('abstract_specs', [
        # Establish a baseline - concretize a single spec
        ('mpileaks',),
        # When concretized together with older version of callpath
        # and dyninst it uses those older versions
        ('mpileaks', 'callpath@0.9', 'dyninst@8.1.1'),
        # Handle recursive syntax within specs
        ('mpileaks', 'callpath@0.9 ^dyninst@8.1.1', 'dyninst'),
        # Test specs that have overlapping dependencies but are not
        # one a dependency of the other
        ('mpileaks', 'direct-mpich')
    ])
    def test_simultaneous_concretization_of_specs(self, abstract_specs):

        abstract_specs = [Spec(x) for x in abstract_specs]
        concrete_specs = spack.concretize.concretize_specs_together(
            *abstract_specs)

        # Check there's only one configuration of each package in the DAG
        names = set(
            dep.name for spec in concrete_specs for dep in spec.traverse()
        )
        for name in names:
            name_specs = set(
                spec[name] for spec in concrete_specs if name in spec
            )
            assert len(name_specs) == 1

        # Check that there's at least one Spec that satisfies the
        # initial abstract request
        for aspec in abstract_specs:
            assert any(cspec.satisfies(aspec) for cspec in concrete_specs)

        # Make sure the concrete spec are top-level specs with no dependents
        for spec in concrete_specs:
            assert not spec.dependents()

    @pytest.mark.parametrize('spec', ['noversion', 'noversion-bundle'])
    def test_noversion_pkg(self, spec):
        """Test concretization failures for no-version packages."""
        with pytest.raises(spack.error.SpackError):
            Spec(spec).concretized()

    # Include targets to prevent regression on 20537
    @pytest.mark.parametrize('spec, best_achievable', [
        ('mpileaks%gcc@4.4.7 target=x86_64:', 'core2'),
        ('mpileaks%gcc@4.8 target=x86_64:', 'haswell'),
        ('mpileaks%gcc@5.3.0 target=x86_64:', 'broadwell'),
        ('mpileaks%apple-clang@5.1.0 target=x86_64:', 'x86_64')
    ])
    @pytest.mark.regression('13361', '20537')
    def test_adjusting_default_target_based_on_compiler(
            self, spec, best_achievable, current_host, mock_targets
    ):
        best_achievable = archspec.cpu.TARGETS[best_achievable]
        expected = best_achievable if best_achievable < current_host \
            else current_host
        with spack.concretize.disable_compiler_existence_check():
            s = Spec(spec).concretized()
            assert str(s.architecture.target) == str(expected)

    @pytest.mark.regression('8735,14730')
    def test_compiler_version_matches_any_entry_in_compilers_yaml(self):
        # Ensure that a concrete compiler with different compiler version
        # doesn't match (here it's 4.5 vs. 4.5.0)
        with pytest.raises(spack.concretize.UnavailableCompilerVersionError):
            s = Spec('mpileaks %gcc@4.5')
            s.concretize()

        # An abstract compiler with a version list could resolve to 4.5.0
        s = Spec('mpileaks %gcc@4.5:')
        s.concretize()
        assert str(s.compiler.version) == '4.5.0'

    def test_concretize_anonymous(self):
        with pytest.raises(spack.error.SpackError):
            s = Spec('+variant')
            s.concretize()

    @pytest.mark.parametrize('spec_str', [
        'mpileaks ^%gcc', 'mpileaks ^cflags=-g'
    ])
    def test_concretize_anonymous_dep(self, spec_str):
        with pytest.raises(spack.error.SpackError):
            s = Spec(spec_str)
            s.concretize()

    @pytest.mark.parametrize('spec_str,expected_str', [
        # Unconstrained versions select default compiler (gcc@4.5.0)
        ('bowtie@1.3.0', '%gcc@4.5.0'),
        # Version with conflicts and no valid gcc select another compiler
        ('bowtie@1.2.2', '%clang@3.3'),
        # If a higher gcc is available still prefer that
        ('bowtie@1.2.2 os=redhat6', '%gcc@4.7.2'),
    ])
    def test_compiler_conflicts_in_package_py(self, spec_str, expected_str):
        if spack.config.get('config:concretizer') == 'original':
            pytest.skip('Original concretizer cannot work around conflicts')

        s = Spec(spec_str).concretized()
        assert s.satisfies(expected_str)

    @pytest.mark.parametrize('spec_str,expected,unexpected', [
        ('py-extension3 ^python@3.5.1', [], ['py-extension1']),
        ('py-extension3 ^python@2.7.11', ['py-extension1'], []),
        ('py-extension3@1.0 ^python@2.7.11', ['patchelf@0.9'], []),
        ('py-extension3@1.1 ^python@2.7.11', ['patchelf@0.9'], []),
        ('py-extension3@1.0 ^python@3.5.1', ['patchelf@0.10'], []),
    ])
    @pytest.mark.skipif(
        sys.version_info[:2] == (3, 5), reason='Known failure with Python3.5'
    )
    def test_conditional_dependencies(self, spec_str, expected, unexpected):
        s = Spec(spec_str).concretized()

        for dep in expected:
            msg = '"{0}" is not in "{1}" and was expected'
            assert dep in s, msg.format(dep, spec_str)

        for dep in unexpected:
            msg = '"{0}" is in "{1}" but was unexpected'
            assert dep not in s, msg.format(dep, spec_str)

    @pytest.mark.parametrize('spec_str,patched_deps', [
        ('patch-several-dependencies', [('libelf', 1), ('fake', 2)]),
        ('patch-several-dependencies@1.0',
         [('libelf', 1), ('fake', 2), ('libdwarf', 1)]),
        ('patch-several-dependencies@1.0 ^libdwarf@20111030',
         [('libelf', 1), ('fake', 2), ('libdwarf', 2)]),
        ('patch-several-dependencies ^libelf@0.8.10',
         [('libelf', 2), ('fake', 2)]),
        ('patch-several-dependencies +foo', [('libelf', 2), ('fake', 2)])
    ])
    def test_patching_dependencies(self, spec_str, patched_deps):
        s = Spec(spec_str).concretized()

        for dep, num_patches in patched_deps:
            assert s[dep].satisfies('patches=*')
            assert len(s[dep].variants['patches'].value) == num_patches

    @pytest.mark.regression(
        '267,303,1781,2310,2632,3628'
    )
    @pytest.mark.parametrize('spec_str, expected', [
        # Need to understand that this configuration is possible
        # only if we use the +mpi variant, which is not the default
        ('fftw ^mpich', ['+mpi']),
        # This spec imposes two orthogonal constraints on a dependency,
        # one of which is conditional. The original concretizer fail since
        # when it applies the first constraint, it sets the unknown variants
        # of the dependency to their default values
        ('quantum-espresso', ['^fftw@1.0+mpi']),
        # This triggers a conditional dependency on ^fftw@1.0
        ('quantum-espresso', ['^openblas']),
        # This constructs a constraint for a dependency og the type
        # @x.y:x.z where the lower bound is unconditional, the upper bound
        # is conditional to having a variant set
        ('quantum-espresso', ['^libelf@0.8.12']),
        ('quantum-espresso~veritas', ['^libelf@0.8.13'])
    ])
    def test_working_around_conflicting_defaults(self, spec_str, expected):
        if spack.config.get('config:concretizer') == 'original':
            pytest.xfail('Known failure of the original concretizer')

        s = Spec(spec_str).concretized()

        assert s.concrete
        for constraint in expected:
            assert s.satisfies(constraint)

    @pytest.mark.regression('4635')
    @pytest.mark.parametrize('spec_str,expected', [
        ('cmake', ['%clang']),
        ('cmake %gcc', ['%gcc']),
        ('cmake %clang', ['%clang'])
    ])
    def test_external_package_and_compiler_preferences(
            self, spec_str, expected
    ):
        if spack.config.get('config:concretizer') == 'original':
            pytest.xfail('Known failure of the original concretizer')

        packages_yaml = {
            'all': {
                'compiler': ['clang', 'gcc'],
            },
            'cmake': {
                'externals': [
                    {'spec': 'cmake@3.4.3', 'prefix': '/usr'}
                ],
                'buildable': False
            }
        }
        spack.config.set('packages', packages_yaml)
        s = Spec(spec_str).concretized()

        assert s.external
        for condition in expected:
            assert s.satisfies(condition)

    @pytest.mark.regression('5651')
    def test_package_with_constraint_not_met_by_external(
            self
    ):
        """Check that if we have an external package A at version X.Y in
        packages.yaml, but our spec doesn't allow X.Y as a version, then
        a new version of A is built that meets the requirements.
        """
        if spack.config.get('config:concretizer') == 'original':
            pytest.xfail('Known failure of the original concretizer')

        packages_yaml = {
            'libelf': {
                'externals': [
                    {'spec': 'libelf@0.8.13', 'prefix': '/usr'}
                ]
            }
        }
        spack.config.set('packages', packages_yaml)

        # quantum-espresso+veritas requires libelf@:0.8.12
        s = Spec('quantum-espresso+veritas').concretized()
        assert s.satisfies('^libelf@0.8.12')
        assert not s['libelf'].external

    @pytest.mark.regression('9744')
    def test_cumulative_version_ranges_with_different_length(self):
        if spack.config.get('config:concretizer') == 'original':
            pytest.xfail('Known failure of the original concretizer')

        s = Spec('cumulative-vrange-root').concretized()
        assert s.concrete
        assert s.satisfies('^cumulative-vrange-bottom@2.2')

    @pytest.mark.regression('9937')
    @pytest.mark.skipif(
        sys.version_info[:2] == (3, 5), reason='Known failure with Python3.5'
    )
    def test_dependency_conditional_on_another_dependency_state(self):
        root_str = 'variant-on-dependency-condition-root'
        dep_str = 'variant-on-dependency-condition-a'
        spec_str = '{0} ^{1}'.format(root_str, dep_str)

        s = Spec(spec_str).concretized()
        assert s.concrete
        assert s.satisfies('^variant-on-dependency-condition-b')

        s = Spec(spec_str + '+x').concretized()
        assert s.concrete
        assert s.satisfies('^variant-on-dependency-condition-b')

        s = Spec(spec_str + '~x').concretized()
        assert s.concrete
        assert not s.satisfies('^variant-on-dependency-condition-b')

    @pytest.mark.regression('8082')
    @pytest.mark.parametrize('spec_str,expected', [
        ('cmake %gcc', '%gcc'),
        ('cmake %clang', '%clang')
    ])
    def test_compiler_constraint_with_external_package(
            self, spec_str, expected
    ):
        if spack.config.get('config:concretizer') == 'original':
            pytest.xfail('Known failure of the original concretizer')

        packages_yaml = {
            'cmake': {
                'externals': [
                    {'spec': 'cmake@3.4.3', 'prefix': '/usr'}
                ],
                'buildable': False
            }
        }
        spack.config.set('packages', packages_yaml)

        s = Spec(spec_str).concretized()
        assert s.external
        assert s.satisfies(expected)

    @pytest.mark.regression('20976')
    @pytest.mark.parametrize('compiler,spec_str,expected,xfailold', [
        ('gcc', 'external-common-python %clang',
         '%clang ^external-common-openssl%gcc ^external-common-gdbm%clang', False),
        ('clang', 'external-common-python',
         '%clang ^external-common-openssl%clang ^external-common-gdbm%clang', True)
    ])
    def test_compiler_in_nonbuildable_external_package(
            self, compiler, spec_str, expected, xfailold
    ):
        """Check that the compiler of a non-buildable external package does not
           spread to other dependencies, unless no other commpiler is specified."""
        packages_yaml = {
            'external-common-openssl': {
                'externals': [
                    {'spec': 'external-common-openssl@1.1.1i%' + compiler,
                     'prefix': '/usr'}
                ],
                'buildable': False
            }
        }
        spack.config.set('packages', packages_yaml)

        s = Spec(spec_str).concretized()
        if xfailold and spack.config.get('config:concretizer') == 'original':
            pytest.xfail('This only works on the ASP-based concretizer')
        assert s.satisfies(expected)
        assert 'external-common-perl' not in [d.name for d in s.dependencies()]

    def test_external_packages_have_consistent_hash(self):
        if spack.config.get('config:concretizer') == 'original':
            pytest.skip('This tests needs the ASP-based concretizer')

        s, t = Spec('externaltool'), Spec('externaltool')
        s._old_concretize(), t._new_concretize()

        assert s.dag_hash() == t.dag_hash()
        assert s.build_hash() == t.build_hash()
        assert s.full_hash() == t.full_hash()

    def test_external_that_would_require_a_virtual_dependency(self):
        s = Spec('requires-virtual').concretized()

        assert s.external
        assert 'stuff' not in s

    def test_transitive_conditional_virtual_dependency(self):
        s = Spec('transitive-conditional-virtual-dependency').concretized()

        # The default for conditional-virtual-dependency is to have
        # +stuff~mpi, so check that these defaults are respected
        assert '+stuff' in s['conditional-virtual-dependency']
        assert '~mpi' in s['conditional-virtual-dependency']

        # 'stuff' is provided by an external package, so check it's present
        assert 'externalvirtual' in s

    @pytest.mark.regression('20040')
    def test_conditional_provides_or_depends_on(self):
        if spack.config.get('config:concretizer') == 'original':
            pytest.xfail('Known failure of the original concretizer')

        # Check that we can concretize correctly a spec that can either
        # provide a virtual or depend on it based on the value of a variant
        s = Spec('conditional-provider +disable-v1').concretized()
        assert 'v1-provider' in s
        assert s['v1'].name == 'v1-provider'
        assert s['v2'].name == 'conditional-provider'

    @pytest.mark.regression('20079')
    @pytest.mark.parametrize('spec_str,tests_arg,with_dep,without_dep', [
        # Check that True is treated correctly and attaches test deps
        # to all nodes in the DAG
        ('a', True, ['a'], []),
        ('a foobar=bar', True, ['a', 'b'], []),
        # Check that a list of names activates the dependency only for
        # packages in that list
        ('a foobar=bar', ['a'], ['a'], ['b']),
        ('a foobar=bar', ['b'], ['b'], ['a']),
        # Check that False disregard test dependencies
        ('a foobar=bar', False, [], ['a', 'b']),
    ])
    def test_activating_test_dependencies(
            self, spec_str, tests_arg, with_dep, without_dep
    ):
        s = Spec(spec_str).concretized(tests=tests_arg)

        for pkg_name in with_dep:
            msg = "Cannot find test dependency in package '{0}'"
            node = s[pkg_name]
            assert node.dependencies(deptype='test'), msg.format(pkg_name)

        for pkg_name in without_dep:
            msg = "Test dependency in package '{0}' is unexpected"
            node = s[pkg_name]
            assert not node.dependencies(deptype='test'), msg.format(pkg_name)

    @pytest.mark.regression('20019')
    def test_compiler_match_is_preferred_to_newer_version(self):
        if spack.config.get('config:concretizer') == 'original':
            pytest.xfail('Known failure of the original concretizer')

        # This spec depends on openblas. Openblas has a conflict
        # that doesn't allow newer versions with gcc@4.4.0. Check
        # that an old version of openblas is selected, rather than
        # a different compiler for just that node.
        spec_str = 'simple-inheritance+openblas %gcc@4.4.0 os=redhat6'
        s = Spec(spec_str).concretized()

        assert 'openblas@0.2.13' in s
        assert s['openblas'].satisfies('%gcc@4.4.0')

    @pytest.mark.regression('19981')
    def test_target_ranges_in_conflicts(self):
        with pytest.raises(spack.error.SpackError):
            Spec('impossible-concretization').concretized()

    @pytest.mark.regression('20040')
    def test_variant_not_default(self):
        s = Spec('ecp-viz-sdk').concretized()

        # Check default variant value for the package
        assert '+dep' in s['conditional-constrained-dependencies']

        # Check that non-default variant values are forced on the dependency
        d = s['dep-with-variants']
        assert '+foo+bar+baz' in d

    @pytest.mark.regression('20055')
    def test_custom_compiler_version(self):
        if spack.config.get('config:concretizer') == 'original':
            pytest.xfail('Known failure of the original concretizer')

        s = Spec('a %gcc@foo os=redhat6').concretized()
        assert '%gcc@foo' in s

    def test_all_patches_applied(self):
        uuidpatch = 'a60a42b73e03f207433c5579de207c6ed61d58e4d12dd3b5142eb525728d89ea'
        localpatch = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
        spec = spack.spec.Spec('conditionally-patch-dependency+jasper')
        spec.concretize()
        assert ((uuidpatch, localpatch) ==
                spec['libelf'].variants['patches'].value)

    def test_dont_select_version_that_brings_more_variants_in(self):
        s = Spec('dep-with-variants-if-develop-root').concretized()
        assert s['dep-with-variants-if-develop'].satisfies('@1.0')

    @pytest.mark.regression('20244,20736')
    @pytest.mark.parametrize('spec_str,is_external,expected', [
        # These are all externals, and 0_8 is a version not in package.py
        ('externaltool@1.0', True, '@1.0'),
        ('externaltool@0.9', True, '@0.9'),
        ('externaltool@0_8', True, '@0_8'),
        # This external package is buildable, has a custom version
        # in packages.yaml that is greater than the ones in package.py
        # and specifies a variant
        ('external-buildable-with-variant +baz', True, '@1.1.special +baz'),
        ('external-buildable-with-variant ~baz', False, '@1.0 ~baz'),
        ('external-buildable-with-variant@1.0: ~baz', False, '@1.0 ~baz'),
        # This uses an external version that meets the condition for
        # having an additional dependency, but the dependency shouldn't
        # appear in the answer set
        ('external-buildable-with-variant@0.9 +baz', True, '@0.9'),
    ])
    def test_external_package_versions(self, spec_str, is_external, expected):
        s = Spec(spec_str).concretized()
        assert s.external == is_external
        assert s.satisfies(expected)

    @pytest.mark.regression('20292')
    @pytest.mark.parametrize('context', [
        {'add_variant': True, 'delete_variant': False},
        {'add_variant': False, 'delete_variant': True},
        {'add_variant': True, 'delete_variant': True}
    ])
    @pytest.mark.xfail()
    def test_reuse_installed_packages(
            self, context, mutable_database, repo_with_changing_recipe
    ):
        # Install a spec
        root = Spec('root').concretized()
        dependency = root['changing'].copy()
        root.package.do_install(fake=True, explicit=True)

        # Modify package.py
        repo_with_changing_recipe.change(context)

        # Try to concretize with the spec installed previously
        new_root = Spec('root ^/{0}'.format(
            dependency.dag_hash())
        ).concretized()

        assert root.dag_hash() == new_root.dag_hash()

    @pytest.mark.regression('20784')
    def test_concretization_of_test_dependencies(self):
        # With clingo we emit dependency_conditions regardless of the type
        # of the dependency. We need to ensure that there's at least one
        # dependency type declared to infer that the dependency holds.
        s = Spec('test-dep-with-imposed-conditions').concretized()
        assert 'c' not in s

    @pytest.mark.parametrize('spec_str', [
        'wrong-variant-in-conflicts',
        'wrong-variant-in-depends-on'
    ])
    def test_error_message_for_inconsistent_variants(self, spec_str):
        if spack.config.get('config:concretizer') == 'original':
            pytest.xfail('Known failure of the original concretizer')

        s = Spec(spec_str)
        with pytest.raises(RuntimeError, match='not found in package'):
            s.concretize()
