# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re
import pytest

import spack.environment as ev
import spack.main
import spack.modules.lmod
import spack.spec

mpich_spec_string = 'mpich@3.0.4'
mpileaks_spec_string = 'mpileaks'
libdwarf_spec_string = 'libdwarf arch=x64-linux'

install = spack.main.SpackCommand('install')

#: Class of the writer tested in this module
writer_cls = spack.modules.lmod.LmodModulefileWriter


@pytest.fixture(params=[
    'clang@3.3',
    'gcc@4.5.0'
])
def compiler(request):
    return request.param


@pytest.fixture(params=[
    ('mpich@3.0.4', ('mpi',)),
    ('mpich@3.0.1', []),
    ('openblas@0.2.15', ('blas',)),
    ('openblas-with-lapack@0.2.15', ('blas', 'lapack'))
])
def provider(request):
    return request.param


@pytest.mark.usefixtures('config', 'mock_packages',)
class TestLmod(object):

    def test_file_layout(
            self, compiler, provider, factory, module_configuration
    ):
        """Tests the layout of files in the hierarchy is the one expected."""
        module_configuration('complex_hierarchy')
        spec_string, services = provider
        module, spec = factory(spec_string + '%' + compiler)

        layout = module.layout

        # Check that the services provided are in the hierarchy
        for s in services:
            assert s in layout.conf.hierarchy_tokens

        # Check that the compiler part of the path has no hash and that it
        # is transformed to r"Core" if the compiler is listed among core
        # compilers
        # Check that specs listed as core_specs are transformed to "Core"
        if compiler == 'clang@3.3' or spec_string == 'mpich@3.0.1':
            assert 'Core' in layout.available_path_parts
        else:
            assert compiler.replace('@', '/') in layout.available_path_parts

        # Check that the provider part instead has always an hash even if
        # hash has been disallowed in the configuration file
        path_parts = layout.available_path_parts
        service_part = spec_string.replace('@', '/')
        service_part = '-'.join([service_part, layout.spec.dag_hash(length=7)])
        assert service_part in path_parts

        # Check that multi-providers have repetitions in path parts
        repetitions = len([x for x in path_parts if service_part == x])
        if spec_string == 'openblas-with-lapack@0.2.15':
            assert repetitions == 2
        else:
            assert repetitions == 1

    def test_simple_case(self, modulefile_content, module_configuration):
        """Tests the generation of a simple TCL module file."""

        module_configuration('autoload_direct')
        content = modulefile_content(mpich_spec_string)

        assert '-- -*- lua -*-' in content
        assert 'whatis([[Name : mpich]])' in content
        assert 'whatis([[Version : 3.0.4]])' in content
        assert 'family("mpi")' in content

    def test_autoload_direct(self, modulefile_content, module_configuration):
        """Tests the automatic loading of direct dependencies."""

        module_configuration('autoload_direct')
        content = modulefile_content(mpileaks_spec_string)

        assert len([x for x in content if 'if not isloaded(' in x]) == 2
        assert len([x for x in content if 'load(' in x]) == 2

        # The configuration file doesn't set the verbose keyword
        # that defaults to False
        messages = [x for x in content if 'LmodMessage("Autoloading' in x]
        assert len(messages) == 0

    def test_autoload_all(self, modulefile_content, module_configuration):
        """Tests the automatic loading of all dependencies."""

        module_configuration('autoload_all')
        content = modulefile_content(mpileaks_spec_string)

        assert len([x for x in content if 'if not isloaded(' in x]) == 5
        assert len([x for x in content if 'load(' in x]) == 5

        # The configuration file sets the verbose keyword to True
        messages = [x for x in content if 'LmodMessage("Autoloading' in x]
        assert len(messages) == 5

    def test_alter_environment(self, modulefile_content, module_configuration):
        """Tests modifications to run-time environment."""

        module_configuration('alter_environment')
        content = modulefile_content('mpileaks platform=test target=x86_64')

        assert len(
            [x for x in content if x.startswith('prepend_path("CMAKE_PREFIX_PATH"')]  # NOQA: ignore=E501
        ) == 0
        assert len([x for x in content if 'setenv("FOO", "foo")' in x]) == 1
        assert len([x for x in content if 'unsetenv("BAR")' in x]) == 1

        content = modulefile_content(
            'libdwarf platform=test target=core2'
        )

        assert len(
            [x for x in content if x.startswith('prepend-path("CMAKE_PREFIX_PATH"')]  # NOQA: ignore=E501
        ) == 0
        assert len([x for x in content if 'setenv("FOO", "foo")' in x]) == 0
        assert len([x for x in content if 'unsetenv("BAR")' in x]) == 0

    def test_prepend_path_separator(self, modulefile_content,
                                    module_configuration):
        """Tests modifications to run-time environment."""

        module_configuration('module_path_separator')
        content = modulefile_content('module-path-separator')

        for line in content:
            if re.match(r'[a-z]+_path\("COLON"', line):
                assert line.endswith('"foo", ":")')
            elif re.match(r'[a-z]+_path\("SEMICOLON"', line):
                assert line.endswith('"bar", ";")')

    def test_blacklist(self, modulefile_content, module_configuration):
        """Tests blacklisting the generation of selected modules."""

        module_configuration('blacklist')
        content = modulefile_content(mpileaks_spec_string)

        assert len([x for x in content if 'if not isloaded(' in x]) == 1
        assert len([x for x in content if 'load(' in x]) == 1

    def test_no_hash(self, factory, module_configuration):
        """Makes sure that virtual providers (in the hierarchy) always
        include a hash. Make sure that the module file for the spec
        does not include a hash if hash_length is 0.
        """

        module_configuration('no_hash')
        module, spec = factory(mpileaks_spec_string)
        path = module.layout.filename
        mpi_spec = spec['mpi']

        mpi_element = "{0}/{1}-{2}/".format(
            mpi_spec.name, mpi_spec.version, mpi_spec.dag_hash(length=7)
        )

        assert mpi_element in path

        mpileaks_spec = spec
        mpileaks_element = "{0}/{1}.lua".format(
            mpileaks_spec.name, mpileaks_spec.version
        )

        assert path.endswith(mpileaks_element)

    def test_no_core_compilers(self, factory, module_configuration):
        """Ensures that missing 'core_compilers' in the configuration file
        raises the right exception.
        """

        # In this case we miss the entry completely
        module_configuration('missing_core_compilers')

        module, spec = factory(mpileaks_spec_string)
        with pytest.raises(spack.modules.lmod.CoreCompilersNotFoundError):
            module.write()

        # Here we have an empty list
        module_configuration('core_compilers_empty')

        module, spec = factory(mpileaks_spec_string)
        with pytest.raises(spack.modules.lmod.CoreCompilersNotFoundError):
            module.write()

    def test_non_virtual_in_hierarchy(self, factory, module_configuration):
        """Ensures that if a non-virtual is in hierarchy, an exception will
        be raised.
        """
        module_configuration('non_virtual_in_hierarchy')

        module, spec = factory(mpileaks_spec_string)
        with pytest.raises(spack.modules.lmod.NonVirtualInHierarchyError):
            module.write()

    def test_override_template_in_package(
            self, modulefile_content, module_configuration
    ):
        """Tests overriding a template from and attribute in the package."""

        module_configuration('autoload_direct')
        content = modulefile_content('override-module-templates')

        assert 'Override successful!' in content

    def test_override_template_in_modules_yaml(
            self, modulefile_content, module_configuration
    ):
        """Tests overriding a template from `modules.yaml`"""
        module_configuration('override_template')

        content = modulefile_content('override-module-templates')
        assert 'Override even better!' in content

        content = modulefile_content('mpileaks target=x86_64')
        assert 'Override even better!' in content

    @pytest.mark.usefixtures('config')
    def test_external_configure_args(
            self, factory
    ):
        # If this package is detected as an external, its configure option line
        # in the module file starts with 'unknown'
        writer, spec = factory('externaltool')

        assert 'unknown' in writer.context.configure_options

    def test_guess_core_compilers(
            self, factory, module_configuration, monkeypatch
    ):
        """Check that we can guess core compilers."""

        # In this case we miss the entry completely
        module_configuration('missing_core_compilers')

        # Our mock paths must be detected as system paths
        monkeypatch.setattr(
            spack.util.environment, 'system_dirs', ['/path/to']
        )

        # We don't want to really write into user configuration
        # when running tests
        def no_op_set(*args, **kwargs):
            pass
        monkeypatch.setattr(spack.config, 'set', no_op_set)

        # Assert we have core compilers now
        writer, _ = factory(mpileaks_spec_string)
        assert writer.conf.core_compilers

    @pytest.mark.parametrize('spec_str', [
        'mpileaks target=nocona',
        'mpileaks target=core2',
        'mpileaks target=x86_64',
    ])
    @pytest.mark.regression('13005')
    def test_only_generic_microarchitectures_in_root(
            self, spec_str, factory, module_configuration
    ):
        module_configuration('complex_hierarchy')
        writer, spec = factory(spec_str)

        assert str(spec.target.family) in writer.layout.arch_dirname
        if spec.target.family != spec.target:
            assert str(spec.target) not in writer.layout.arch_dirname

    def test_projections_specific(self, factory, module_configuration):
        """Tests reading the correct naming scheme."""

        # This configuration has no error, so check the conflicts directives
        # are there
        module_configuration('projections')

        # Test we read the expected configuration for the naming scheme
        writer, _ = factory('mpileaks')
        expected = {
            'all': '{name}/v{version}',
            'mpileaks': '{name}-mpiprojection'
        }

        assert writer.conf.projections == expected
        projection = writer.spec.format(writer.conf.projections['mpileaks'])
        assert projection in writer.layout.use_name

    def test_projections_all(self, factory, module_configuration):
        """Tests reading the correct naming scheme."""

        # This configuration has no error, so check the conflicts directives
        # are there
        module_configuration('projections')

        # Test we read the expected configuration for the naming scheme
        writer, _ = factory('libelf')
        expected = {
            'all': '{name}/v{version}',
            'mpileaks': '{name}-mpiprojection'
        }

        assert writer.conf.projections == expected
        projection = writer.spec.format(writer.conf.projections['all'])
        assert projection in writer.layout.use_name

    def test_config_backwards_compat(self, mutable_config):
        settings = {
            'enable': ['lmod'],
            'lmod': {
                'core_compilers': ['%gcc@0.0.0']
            }
        }

        spack.config.set('modules:default', settings)
        new_format = spack.modules.lmod.configuration('default')

        spack.config.set('modules', settings)
        old_format = spack.modules.lmod.configuration('default')

        assert old_format == new_format
        assert old_format == settings['lmod']

    def test_modules_relative_to_view(
            self, tmpdir, modulefile_content, module_configuration, install_mockery):
        with ev.Environment(str(tmpdir), with_view=True) as e:
            module_configuration('with_view')
            install('cmake')

            spec = spack.spec.Spec('cmake').concretized()

            content = modulefile_content('cmake')
            expected = e.default_view.view().get_projection_for_spec(spec)
            # Rather than parse all lines, ensure all prefixes in the content
            # point to the right one
            assert any(expected in line for line in content)
            assert not any(spec.prefix in line for line in content)
