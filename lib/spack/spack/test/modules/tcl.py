# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.modules.common
import spack.modules.tcl
import spack.spec

mpich_spec_string = 'mpich@3.0.4'
mpileaks_spec_string = 'mpileaks'
libdwarf_spec_string = 'libdwarf target=x86_64'

#: Class of the writer tested in this module
writer_cls = spack.modules.tcl.TclModulefileWriter


@pytest.mark.usefixtures('config', 'mock_packages')
class TestTcl(object):

    def test_simple_case(self, modulefile_content, module_configuration):
        """Tests the generation of a simple TCL module file."""

        module_configuration('autoload_direct')
        content = modulefile_content(mpich_spec_string)

        assert 'module-whatis "mpich @3.0.4"' in content

    def test_autoload_direct(self, modulefile_content, module_configuration):
        """Tests the automatic loading of direct dependencies."""

        module_configuration('autoload_direct')
        content = modulefile_content(mpileaks_spec_string)

        assert len([x for x in content if 'is-loaded' in x]) == 2
        assert len([x for x in content if 'module load ' in x]) == 2

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        content = modulefile_content('dtbuild1')

        assert len([x for x in content if 'is-loaded' in x]) == 2
        assert len([x for x in content if 'module load ' in x]) == 2

        # The configuration file sets the verbose keyword to False
        messages = [x for x in content if 'puts stderr "Autoloading' in x]
        assert len(messages) == 0

    def test_autoload_all(self, modulefile_content, module_configuration):
        """Tests the automatic loading of all dependencies."""

        module_configuration('autoload_all')
        content = modulefile_content(mpileaks_spec_string)

        assert len([x for x in content if 'is-loaded' in x]) == 5
        assert len([x for x in content if 'module load ' in x]) == 5

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        content = modulefile_content('dtbuild1')

        assert len([x for x in content if 'is-loaded' in x]) == 2
        assert len([x for x in content if 'module load ' in x]) == 2

        # The configuration file sets the verbose keyword to True
        messages = [x for x in content if 'puts stderr "Autoloading' in x]
        assert len(messages) == 2

    def test_prerequisites_direct(
            self, modulefile_content, module_configuration
    ):
        """Tests asking direct dependencies as prerequisites."""

        module_configuration('prerequisites_direct')
        content = modulefile_content('mpileaks target=x86_64')

        assert len([x for x in content if 'prereq' in x]) == 2

    def test_prerequisites_all(self, modulefile_content, module_configuration):
        """Tests asking all dependencies as prerequisites."""

        module_configuration('prerequisites_all')
        content = modulefile_content('mpileaks target=x86_64')

        assert len([x for x in content if 'prereq' in x]) == 5

    def test_alter_environment(self, modulefile_content, module_configuration):
        """Tests modifications to run-time environment."""

        module_configuration('alter_environment')
        content = modulefile_content('mpileaks platform=test target=x86_64')

        assert len([x for x in content
                    if x.startswith('prepend-path CMAKE_PREFIX_PATH')
                    ]) == 0
        assert len([x for x in content if 'setenv FOO "foo"' in x]) == 1
        assert len([
            x for x in content if 'setenv OMPI_MCA_mpi_leave_pinned "1"' in x
        ]) == 1
        assert len([
            x for x in content if 'setenv OMPI_MCA_MPI_LEAVE_PINNED "1"' in x
        ]) == 0
        assert len([x for x in content if 'unsetenv BAR' in x]) == 1
        assert len([x for x in content if 'setenv MPILEAKS_ROOT' in x]) == 1

        content = modulefile_content(
            'libdwarf platform=test target=core2'
        )

        assert len([x for x in content
                    if x.startswith('prepend-path CMAKE_PREFIX_PATH')
                    ]) == 0
        assert len([x for x in content if 'setenv FOO "foo"' in x]) == 0
        assert len([x for x in content if 'unsetenv BAR' in x]) == 0
        assert len([x for x in content if 'is-loaded foo/bar' in x]) == 1
        assert len([x for x in content if 'module load foo/bar' in x]) == 1
        assert len([x for x in content if 'setenv LIBDWARF_ROOT' in x]) == 1

    def test_blacklist(self, modulefile_content, module_configuration):
        """Tests blacklisting the generation of selected modules."""

        module_configuration('blacklist')
        content = modulefile_content('mpileaks ^zmpi')

        assert len([x for x in content if 'is-loaded' in x]) == 1
        assert len([x for x in content if 'module load ' in x]) == 1

        # Catch "Exception" to avoid using FileNotFoundError on Python 3
        # and IOError on Python 2 or common bases like EnvironmentError
        # which are not officially documented
        with pytest.raises(Exception):
            modulefile_content('callpath target=x86_64')

        content = modulefile_content('zmpi target=x86_64')

        assert len([x for x in content if 'is-loaded' in x]) == 1
        assert len([x for x in content if 'module load ' in x]) == 1

    def test_naming_scheme_compat(self, factory, module_configuration):
        """Tests backwards compatibility for naming_scheme key"""
        module_configuration('naming_scheme')

        # Test we read the expected configuration for the naming scheme
        writer, _ = factory('mpileaks')
        expected = {
            'all': '{name}/{version}-{compiler.name}'
        }

        assert writer.conf.projections == expected
        projection = writer.spec.format(writer.conf.projections['all'])
        assert projection in writer.layout.use_name

    def test_projections_specific(self, factory, module_configuration):
        """Tests reading the correct naming scheme."""

        # This configuration has no error, so check the conflicts directives
        # are there
        module_configuration('projections')

        # Test we read the expected configuration for the naming scheme
        writer, _ = factory('mpileaks')
        expected = {
            'all': '{name}/{version}-{compiler.name}',
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
            'all': '{name}/{version}-{compiler.name}',
            'mpileaks': '{name}-mpiprojection'
        }

        assert writer.conf.projections == expected
        projection = writer.spec.format(writer.conf.projections['all'])
        assert projection in writer.layout.use_name

    def test_invalid_naming_scheme(self, factory, module_configuration):
        """Tests the evaluation of an invalid naming scheme."""

        module_configuration('invalid_naming_scheme')

        # Test that having invalid tokens in the naming scheme raises
        # a RuntimeError
        writer, _ = factory('mpileaks')
        with pytest.raises(RuntimeError):
            writer.layout.use_name

    def test_invalid_token_in_env_name(self, factory, module_configuration):
        """Tests setting environment variables with an invalid name."""

        module_configuration('invalid_token_in_env_var_name')

        writer, _ = factory('mpileaks')
        with pytest.raises(RuntimeError):
            writer.write()

    def test_conflicts(self, modulefile_content, module_configuration):
        """Tests adding conflicts to the module."""

        # This configuration has no error, so check the conflicts directives
        # are there
        module_configuration('conflicts')
        content = modulefile_content('mpileaks')

        assert len([x for x in content if x.startswith('conflict')]) == 2
        assert len([x for x in content if x == 'conflict mpileaks']) == 1
        assert len([x for x in content if x == 'conflict intel/14.0.1']) == 1

        # This configuration is inconsistent, check an error is raised
        module_configuration('wrong_conflicts')
        with pytest.raises(SystemExit):
            modulefile_content('mpileaks')

    def test_module_index(
            self, module_configuration, factory, tmpdir_factory):

        module_configuration('suffix')

        w1, s1 = factory('mpileaks')
        w2, s2 = factory('callpath')
        w3, s3 = factory('openblas')

        test_root = str(tmpdir_factory.mktemp('module-root'))

        spack.modules.common.generate_module_index(test_root, [w1, w2])

        index = spack.modules.common.read_module_index(test_root)

        assert index[s1.dag_hash()].use_name == w1.layout.use_name
        assert index[s2.dag_hash()].path == w2.layout.filename

        spack.modules.common.generate_module_index(test_root, [w3])

        index = spack.modules.common.read_module_index(test_root)

        assert len(index) == 3
        assert index[s1.dag_hash()].use_name == w1.layout.use_name
        assert index[s2.dag_hash()].path == w2.layout.filename

        spack.modules.common.generate_module_index(
            test_root, [w3], overwrite=True)

        index = spack.modules.common.read_module_index(test_root)

        assert len(index) == 1
        assert index[s3.dag_hash()].use_name == w3.layout.use_name

    def test_suffixes(self, module_configuration, factory):
        """Tests adding suffixes to module file name."""
        module_configuration('suffix')

        writer, spec = factory('mpileaks+debug target=x86_64')
        assert 'foo' in writer.layout.use_name
        assert 'foo-foo' not in writer.layout.use_name

        writer, spec = factory('mpileaks~debug target=x86_64')
        assert 'foo-bar' in writer.layout.use_name
        assert 'baz' not in writer.layout.use_name

        writer, spec = factory('mpileaks~debug+opt target=x86_64')
        assert 'baz-foo-bar' in writer.layout.use_name

    def test_setup_environment(self, modulefile_content, module_configuration):
        """Tests the internal set-up of run-time environment."""

        module_configuration('suffix')
        content = modulefile_content('mpileaks')

        assert len([x for x in content if 'setenv FOOBAR' in x]) == 1
        assert len(
            [x for x in content if 'setenv FOOBAR "mpileaks"' in x]
        ) == 1

        spec = spack.spec.Spec('mpileaks')
        spec.concretize()
        content = modulefile_content(str(spec['callpath']))

        assert len([x for x in content if 'setenv FOOBAR' in x]) == 1
        assert len(
            [x for x in content if 'setenv FOOBAR "callpath"' in x]
        ) == 1

    def test_override_config(self, module_configuration, factory):
        """Tests overriding some sections of the configuration file."""
        module_configuration('override_config')

        writer, spec = factory('mpileaks~opt target=x86_64')
        assert 'mpich-static' in writer.layout.use_name
        assert 'over' not in writer.layout.use_name
        assert 'ridden' not in writer.layout.use_name

        writer, spec = factory('mpileaks+opt target=x86_64')
        assert 'over-ridden' in writer.layout.use_name
        assert 'mpich' not in writer.layout.use_name
        assert 'static' not in writer.layout.use_name

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

    def test_extend_context(
            self, modulefile_content, module_configuration
    ):
        """Tests using a package defined context"""
        module_configuration('autoload_direct')
        content = modulefile_content('override-context-templates')

        assert 'puts stderr "sentence from package"' in content

        short_description = 'module-whatis "This package updates the context for TCL modulefiles."'  # NOQA: ignore=E501
        assert short_description in content

    @pytest.mark.regression('4400')
    @pytest.mark.db
    def test_blacklist_implicits(
            self, modulefile_content, module_configuration, database
    ):
        module_configuration('blacklist_implicits')

        # mpileaks has been installed explicitly when setting up
        # the tests database
        mpileaks_specs = database.query('mpileaks')
        for item in mpileaks_specs:
            writer = writer_cls(item, 'default')
            assert not writer.conf.blacklisted

        # callpath is a dependency of mpileaks, and has been pulled
        # in implicitly
        callpath_specs = database.query('callpath')
        for item in callpath_specs:
            writer = writer_cls(item, 'default')
            assert writer.conf.blacklisted

    @pytest.mark.regression('9624')
    @pytest.mark.db
    def test_autoload_with_constraints(
            self, modulefile_content, module_configuration, database
    ):
        """Tests the automatic loading of direct dependencies."""

        module_configuration('autoload_with_constraints')

        # Test the mpileaks that should have the autoloaded dependencies
        content = modulefile_content('mpileaks ^mpich2')
        assert len([x for x in content if 'is-loaded' in x]) == 2

        # Test the mpileaks that should NOT have the autoloaded dependencies
        content = modulefile_content('mpileaks ^mpich')
        assert len([x for x in content if 'is-loaded' in x]) == 0

    def test_config_backwards_compat(self, mutable_config):
        settings = {
            'enable': ['tcl'],
            'tcl': {
                'all': {
                    'conflict': ['{name}']
                }
            }
        }

        spack.config.set('modules:default', settings)
        new_format = spack.modules.tcl.configuration('default')

        spack.config.set('modules', settings)
        old_format = spack.modules.tcl.configuration('default')

        assert old_format == new_format
        assert old_format == settings['tcl']
