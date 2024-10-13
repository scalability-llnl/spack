# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import archspec.cpu

import spack.modules.common
import spack.modules.tcl
import spack.spec

mpich_spec_string = "mpich@3.0.4"
mpileaks_spec_string = "mpileaks"
libdwarf_spec_string = "libdwarf target=x86_64"

#: Class of the writer tested in this module
writer_cls = spack.modules.tcl.TclModulefileWriter

pytestmark = [
    pytest.mark.not_on_windows("does not run on windows"),
    pytest.mark.usefixtures("mock_modules_root"),
]


@pytest.mark.usefixtures("mutable_config", "mock_packages", "mock_module_filename")
class TestTcl:
    def test_simple_case(self, modulefile_content, module_configuration):
        """Tests the generation of a simple Tcl module file."""

        module_configuration("autoload_direct")
        content = modulefile_content(mpich_spec_string)

        assert "module-whatis {mpich @3.0.4}" in content

    def test_autoload_direct(self, modulefile_content, module_configuration):
        """Tests the automatic loading of direct dependencies."""

        module_configuration("autoload_direct")
        content = modulefile_content(mpileaks_spec_string)

        assert (
            len([x for x in content if "if {![info exists ::env(LMOD_VERSION_MAJOR)]} {" in x])
            == 1
        )
        assert len([x for x in content if "depends-on " in x]) == 2
        assert len([x for x in content if "module load " in x]) == 2

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        content = modulefile_content("dtbuild1")

        assert (
            len([x for x in content if "if {![info exists ::env(LMOD_VERSION_MAJOR)]} {" in x])
            == 1
        )
        assert len([x for x in content if "depends-on " in x]) == 2
        assert len([x for x in content if "module load " in x]) == 2

        # The configuration file sets the verbose keyword to False
        messages = [x for x in content if 'puts stderr "Autoloading' in x]
        assert len(messages) == 0

    def test_autoload_all(self, modulefile_content, module_configuration):
        """Tests the automatic loading of all dependencies."""

        module_configuration("autoload_all")
        content = modulefile_content(mpileaks_spec_string)

        assert (
            len([x for x in content if "if {![info exists ::env(LMOD_VERSION_MAJOR)]} {" in x])
            == 1
        )
        assert len([x for x in content if "depends-on " in x]) == 5
        assert len([x for x in content if "module load " in x]) == 5

        # dtbuild1 has
        # - 1 ('run',) dependency
        # - 1 ('build','link') dependency
        # - 1 ('build',) dependency
        # Just make sure the 'build' dependency is not there
        content = modulefile_content("dtbuild1")

        assert (
            len([x for x in content if "if {![info exists ::env(LMOD_VERSION_MAJOR)]} {" in x])
            == 1
        )
        assert len([x for x in content if "depends-on " in x]) == 2
        assert len([x for x in content if "module load " in x]) == 2

    def test_prerequisites_direct(
        self, modulefile_content, module_configuration, host_architecture_str
    ):
        """Tests asking direct dependencies as prerequisites."""

        module_configuration("prerequisites_direct")
        content = modulefile_content(f"mpileaks target={host_architecture_str}")

        assert len([x for x in content if "prereq" in x]) == 2

    def test_prerequisites_all(
        self, modulefile_content, module_configuration, host_architecture_str
    ):
        """Tests asking all dependencies as prerequisites."""

        module_configuration("prerequisites_all")
        content = modulefile_content(f"mpileaks target={host_architecture_str}")

        assert len([x for x in content if "prereq" in x]) == 5

    def test_alter_environment(self, modulefile_content, module_configuration):
        """Tests modifications to run-time environment."""

        module_configuration("alter_environment")
        content = modulefile_content("mpileaks platform=test target=x86_64")

        assert len([x for x in content if x.startswith("prepend-path CMAKE_PREFIX_PATH")]) == 0
        assert len([x for x in content if "setenv FOO {foo}" in x]) == 1
        assert len([x for x in content if "setenv OMPI_MCA_mpi_leave_pinned {1}" in x]) == 1
        assert len([x for x in content if "setenv OMPI_MCA_MPI_LEAVE_PINNED {1}" in x]) == 0
        assert len([x for x in content if "unsetenv BAR" in x]) == 1
        assert len([x for x in content if "setenv MPILEAKS_ROOT" in x]) == 1

        content = modulefile_content("libdwarf platform=test target=core2")

        assert len([x for x in content if x.startswith("prepend-path CMAKE_PREFIX_PATH")]) == 0
        assert len([x for x in content if "setenv FOO {foo}" in x]) == 0
        assert len([x for x in content if "unsetenv BAR" in x]) == 0
        assert len([x for x in content if "depends-on foo/bar" in x]) == 1
        assert len([x for x in content if "module load foo/bar" in x]) == 1
        assert len([x for x in content if "setenv LIBDWARF_ROOT" in x]) == 1

    def test_prepend_path_separator(self, modulefile_content, module_configuration):
        """Tests that we can use custom delimiters to manipulate path lists."""

        module_configuration("module_path_separator")
        content = modulefile_content("module-path-separator")

        assert len([x for x in content if "append-path COLON {foo}" in x]) == 1
        assert len([x for x in content if "prepend-path COLON {foo}" in x]) == 1
        assert len([x for x in content if "remove-path COLON {foo}" in x]) == 1
        assert len([x for x in content if "append-path --delim {;} SEMICOLON {bar}" in x]) == 1
        assert len([x for x in content if "prepend-path --delim {;} SEMICOLON {bar}" in x]) == 1
        assert len([x for x in content if "remove-path --delim {;} SEMICOLON {bar}" in x]) == 1
        assert len([x for x in content if "append-path --delim { } SPACE {qux}" in x]) == 1
        assert len([x for x in content if "remove-path --delim { } SPACE {qux}" in x]) == 1

    @pytest.mark.regression("11355")
    def test_manpath_setup(self, modulefile_content, module_configuration):
        """Tests specific setup of MANPATH environment variable."""

        module_configuration("autoload_direct")

        # no manpath set by module
        content = modulefile_content("mpileaks")
        assert len([x for x in content if "append-path MANPATH {}" in x]) == 0

        # manpath set by module with prepend-path
        content = modulefile_content("module-manpath-prepend")
        assert len([x for x in content if "prepend-path MANPATH {/path/to/man}" in x]) == 1
        assert len([x for x in content if "prepend-path MANPATH {/path/to/share/man}" in x]) == 1
        assert len([x for x in content if "append-path MANPATH {}" in x]) == 1

        # manpath set by module with append-path
        content = modulefile_content("module-manpath-append")
        assert len([x for x in content if "append-path MANPATH {/path/to/man}" in x]) == 1
        assert len([x for x in content if "append-path MANPATH {}" in x]) == 1

        # manpath set by module with setenv
        content = modulefile_content("module-manpath-setenv")
        assert len([x for x in content if "setenv MANPATH {/path/to/man}" in x]) == 1
        assert len([x for x in content if "append-path MANPATH {}" in x]) == 0

    @pytest.mark.regression("29578")
    def test_setenv_raw_value(self, modulefile_content, module_configuration):
        """Tests that we can set environment variable value without formatting it."""

        module_configuration("autoload_direct")
        content = modulefile_content("module-setenv-raw")

        assert len([x for x in content if "setenv FOO {{{name}}, {name}, {{}}, {}}" in x]) == 1

    @pytest.mark.skipif(
        str(archspec.cpu.host().family) != "x86_64", reason="test data is specific for x86_64"
    )
    def test_help_message(self, modulefile_content, module_configuration):
        """Tests the generation of module help message."""

        module_configuration("autoload_direct")
        content = modulefile_content("mpileaks target=core2")

        help_msg = (
            "proc ModulesHelp { } {"
            "    puts stderr {Name   : mpileaks}"
            "    puts stderr {Version: 2.3}"
            "    puts stderr {Target : core2}"
            "    puts stderr {}"
            "    puts stderr {Mpileaks is a mock package that passes audits}"
            "}"
        )
        assert help_msg in "".join(content)

        content = modulefile_content("libdwarf target=core2")

        help_msg = (
            "proc ModulesHelp { } {"
            "    puts stderr {Name   : libdwarf}"
            "    puts stderr {Version: 20130729}"
            "    puts stderr {Target : core2}"
            "}"
        )
        assert help_msg in "".join(content)

        content = modulefile_content("module-long-help target=core2")

        help_msg = (
            "proc ModulesHelp { } {"
            "    puts stderr {Name   : module-long-help}"
            "    puts stderr {Version: 1.0}"
            "    puts stderr {Target : core2}"
            "    puts stderr {}"
            "    puts stderr {Package to test long description message generated in modulefile.}"
            "    puts stderr {Message too long is wrapped over multiple lines.}"
            "}"
        )
        assert help_msg in "".join(content)

    def test_exclude(self, modulefile_content, module_configuration, host_architecture_str):
        """Tests excluding the generation of selected modules."""

        module_configuration("exclude")
        content = modulefile_content("mpileaks ^zmpi")

        assert len([x for x in content if "module load " in x]) == 1

        # Catch "Exception" to avoid using FileNotFoundError on Python 3
        # and IOError on Python 2 or common bases like EnvironmentError
        # which are not officially documented
        with pytest.raises(Exception):
            modulefile_content(f"callpath target={host_architecture_str}")

        content = modulefile_content(f"zmpi target={host_architecture_str}")

        assert len([x for x in content if "module load " in x]) == 1

    def test_naming_scheme_compat(self, factory, module_configuration):
        """Tests backwards compatibility for naming_scheme key"""
        module_configuration("naming_scheme")

        # Test we read the expected configuration for the naming scheme
        writer, _ = factory("mpileaks")
        expected = {"all": "{name}/{version}-{compiler.name}"}

        assert writer.conf.projections == expected
        projection = writer.spec.format(writer.conf.projections["all"])
        assert projection in writer.layout.use_name

    def test_projections_specific(self, factory, module_configuration):
        """Tests reading the correct naming scheme."""

        # This configuration has no error, so check the conflicts directives
        # are there
        module_configuration("projections")

        # Test we read the expected configuration for the naming scheme
        writer, _ = factory("mpileaks")
        expected = {"all": "{name}/{version}-{compiler.name}", "mpileaks": "{name}-mpiprojection"}

        assert writer.conf.projections == expected
        projection = writer.spec.format(writer.conf.projections["mpileaks"])
        assert projection in writer.layout.use_name

    def test_projections_all(self, factory, module_configuration):
        """Tests reading the correct naming scheme."""

        # This configuration has no error, so check the conflicts directives
        # are there
        module_configuration("projections")

        # Test we read the expected configuration for the naming scheme
        writer, _ = factory("libelf")
        expected = {"all": "{name}/{version}-{compiler.name}", "mpileaks": "{name}-mpiprojection"}

        assert writer.conf.projections == expected
        projection = writer.spec.format(writer.conf.projections["all"])
        assert projection in writer.layout.use_name

    def test_invalid_naming_scheme(self, factory, module_configuration):
        """Tests the evaluation of an invalid naming scheme."""

        module_configuration("invalid_naming_scheme")

        # Test that having invalid tokens in the naming scheme raises
        # a RuntimeError
        writer, _ = factory("mpileaks")
        with pytest.raises(RuntimeError):
            writer.layout.use_name

    def test_invalid_token_in_env_name(self, factory, module_configuration):
        """Tests setting environment variables with an invalid name."""

        module_configuration("invalid_token_in_env_var_name")

        writer, _ = factory("mpileaks")
        with pytest.raises(RuntimeError):
            writer.write()

    def test_conflicts(self, modulefile_content, module_configuration):
        """Tests adding conflicts to the module."""

        # This configuration has no error, so check the conflicts directives
        # are there
        module_configuration("conflicts")
        content = modulefile_content("mpileaks")

        assert len([x for x in content if x.startswith("conflict")]) == 2
        assert len([x for x in content if x == "conflict mpileaks"]) == 1
        assert len([x for x in content if x == "conflict intel/14.0.1"]) == 1

    def test_inconsistent_conflict_in_modules_yaml(self, modulefile_content, module_configuration):
        """Tests inconsistent conflict definition in `modules.yaml`."""

        # This configuration is inconsistent, check an error is raised
        module_configuration("wrong_conflicts")
        with pytest.raises(spack.modules.common.ModulesError):
            modulefile_content("mpileaks")

    def test_module_index(self, module_configuration, factory, tmpdir_factory):
        module_configuration("suffix")

        w1, s1 = factory("mpileaks")
        w2, s2 = factory("callpath")
        w3, s3 = factory("openblas")

        test_root = str(tmpdir_factory.mktemp("module-root"))

        spack.modules.common.generate_module_index(test_root, [w1, w2])

        index = spack.modules.common.read_module_index(test_root)

        assert index[s1.dag_hash()].use_name == w1.layout.use_name
        assert index[s2.dag_hash()].path == w2.layout.filename

        spack.modules.common.generate_module_index(test_root, [w3])

        index = spack.modules.common.read_module_index(test_root)

        assert len(index) == 3
        assert index[s1.dag_hash()].use_name == w1.layout.use_name
        assert index[s2.dag_hash()].path == w2.layout.filename

        spack.modules.common.generate_module_index(test_root, [w3], overwrite=True)

        index = spack.modules.common.read_module_index(test_root)

        assert len(index) == 1
        assert index[s3.dag_hash()].use_name == w3.layout.use_name

    def test_suffixes(self, module_configuration, factory):
        """Tests adding suffixes to module file name."""
        module_configuration("suffix")

        writer, spec = factory("mpileaks+debug target=x86_64")
        assert "foo" in writer.layout.use_name
        assert "foo-foo" not in writer.layout.use_name

        writer, spec = factory("mpileaks~debug target=x86_64")
        assert "foo-bar" in writer.layout.use_name
        assert "baz" not in writer.layout.use_name

        writer, spec = factory("mpileaks~debug+opt target=x86_64")
        assert "baz-foo-bar" in writer.layout.use_name

    def test_setup_environment(self, modulefile_content, module_configuration):
        """Tests the internal set-up of run-time environment."""

        module_configuration("suffix")
        content = modulefile_content("mpileaks")

        assert len([x for x in content if "setenv FOOBAR" in x]) == 1
        assert len([x for x in content if "setenv FOOBAR {mpileaks}" in x]) == 1

        spec = spack.spec.Spec("mpileaks")
        spec.concretize()
        content = modulefile_content(spec["callpath"])

        assert len([x for x in content if "setenv FOOBAR" in x]) == 1
        assert len([x for x in content if "setenv FOOBAR {callpath}" in x]) == 1

    def test_override_config(self, module_configuration, factory):
        """Tests overriding some sections of the configuration file."""
        module_configuration("override_config")

        writer, spec = factory("mpileaks~opt target=x86_64")
        assert "mpich-static" in writer.layout.use_name
        assert "over" not in writer.layout.use_name
        assert "ridden" not in writer.layout.use_name

        writer, spec = factory("mpileaks+opt target=x86_64")
        assert "over-ridden" in writer.layout.use_name
        assert "mpich" not in writer.layout.use_name
        assert "static" not in writer.layout.use_name

    def test_override_template_in_package(self, modulefile_content, module_configuration):
        """Tests overriding a template from and attribute in the package."""

        module_configuration("autoload_direct")
        content = modulefile_content("override-module-templates")

        assert "Override successful!" in content

    def test_override_template_in_modules_yaml(
        self, modulefile_content, module_configuration, host_architecture_str
    ):
        """Tests overriding a template from `modules.yaml`"""
        module_configuration("override_template")

        content = modulefile_content("override-module-templates")
        assert "Override even better!" in content

        content = modulefile_content(f"mpileaks target={host_architecture_str}")
        assert "Override even better!" in content

    def test_extend_context(self, modulefile_content, module_configuration):
        """Tests using a package defined context"""
        module_configuration("autoload_direct")
        content = modulefile_content("override-context-templates")

        assert 'puts stderr "sentence from package"' in content

        short_description = "module-whatis {This package updates the context for Tcl modulefiles.}"
        assert short_description in content

    @pytest.mark.regression("4400")
    @pytest.mark.db
    def test_hide_implicits_no_arg(self, module_configuration, mutable_database):
        module_configuration("exclude_implicits")

        # mpileaks has been installed explicitly when setting up
        # the tests database
        mpileaks_specs = mutable_database.query("mpileaks")
        for item in mpileaks_specs:
            writer = writer_cls(item, "default")
            assert not writer.conf.excluded

        # callpath is a dependency of mpileaks, and has been pulled
        # in implicitly
        callpath_specs = mutable_database.query("callpath")
        for item in callpath_specs:
            writer = writer_cls(item, "default")
            assert writer.conf.excluded

    @pytest.mark.regression("12105")
    def test_hide_implicits_with_arg(self, module_configuration):
        module_configuration("exclude_implicits")

        # mpileaks is defined as explicit with explicit argument set on writer
        mpileaks_spec = spack.spec.Spec("mpileaks")
        mpileaks_spec.concretize()
        writer = writer_cls(mpileaks_spec, "default", True)
        assert not writer.conf.excluded

        # callpath is defined as implicit with explicit argument set on writer
        callpath_spec = spack.spec.Spec("callpath")
        callpath_spec.concretize()
        writer = writer_cls(callpath_spec, "default", False)
        assert writer.conf.excluded

    @pytest.mark.regression("9624")
    def test_autoload_with_constraints(self, modulefile_content, module_configuration):
        """Tests the automatic loading of direct dependencies."""

        module_configuration("autoload_with_constraints")

        # Test the mpileaks that should have the autoloaded dependencies
        content = modulefile_content("mpileaks ^mpich2")
        assert len([x for x in content if "depends-on " in x]) == 2
        assert len([x for x in content if "module load " in x]) == 2

        # Test the mpileaks that should NOT have the autoloaded dependencies
        content = modulefile_content("mpileaks ^mpich")
        assert (
            len([x for x in content if "if {![info exists ::env(LMOD_VERSION_MAJOR)]} {" in x])
            == 0
        )
        assert len([x for x in content if "depends-on " in x]) == 0
        assert len([x for x in content if "module load " in x]) == 0

    def test_modules_no_arch(self, factory, module_configuration):
        module_configuration("no_arch")
        module, spec = factory(mpileaks_spec_string)
        path = module.layout.filename

        assert str(spec.os) not in path

    def test_hide_implicits(self, module_configuration, temporary_store):
        """Tests the addition and removal of hide command in modulerc."""
        module_configuration("hide_implicits")

        spec = spack.spec.Spec("mpileaks@2.3").concretized()

        # mpileaks is defined as implicit, thus hide command should appear in modulerc
        writer = writer_cls(spec, "default", False)
        writer.write()
        assert os.path.exists(writer.layout.modulerc)
        with open(writer.layout.modulerc) as f:
            content = [line.strip() for line in f.readlines()]
        hide_implicit_mpileaks = f"module-hide --soft --hidden-loaded {writer.layout.use_name}"
        assert len([x for x in content if hide_implicit_mpileaks == x]) == 1

        # The direct dependencies are all implicit, and they should have depends-on with fixed
        # 7 character hash, even though the config is set to hash_length = 0.
        with open(writer.layout.filename) as f:
            depends_statements = [line.strip() for line in f.readlines() if "depends-on" in line]
            for dep in spec.dependencies(deptype=("link", "run")):
                assert any(dep.dag_hash(7) in line for line in depends_statements)

        # when mpileaks becomes explicit, its file name changes (hash_length = 0), meaning an
        # extra module file is created; the old one still exists and remains hidden.
        writer = writer_cls(spec, "default", True)
        writer.write()
        assert os.path.exists(writer.layout.modulerc)
        with open(writer.layout.modulerc) as f:
            content = [line.strip() for line in f.readlines()]
        assert hide_implicit_mpileaks in content  # old, implicit mpileaks is still hidden
        assert f"module-hide --soft --hidden-loaded {writer.layout.use_name}" not in content

        # after removing both the implicit and explicit module, the modulerc file would be empty
        # and should be removed.
        writer_cls(spec, "default", False).remove()
        writer_cls(spec, "default", True).remove()
        assert not os.path.exists(writer.layout.modulerc)
        assert not os.path.exists(writer.layout.filename)

        # implicit module is removed
        writer = writer_cls(spec, "default", False)
        writer.write()
        assert os.path.exists(writer.layout.filename)
        assert os.path.exists(writer.layout.modulerc)
        writer.remove()
        assert not os.path.exists(writer.layout.modulerc)
        assert not os.path.exists(writer.layout.filename)

        # three versions of mpileaks are implicit
        writer = writer_cls(spec, "default", False)
        writer.write(overwrite=True)
        spec_alt1 = spack.spec.Spec("mpileaks@2.2").concretized()
        spec_alt2 = spack.spec.Spec("mpileaks@2.1").concretized()
        writer_alt1 = writer_cls(spec_alt1, "default", False)
        writer_alt1.write(overwrite=True)
        writer_alt2 = writer_cls(spec_alt2, "default", False)
        writer_alt2.write(overwrite=True)
        assert os.path.exists(writer.layout.modulerc)
        with open(writer.layout.modulerc) as f:
            content = [line.strip() for line in f.readlines()]
        hide_cmd = f"module-hide --soft --hidden-loaded {writer.layout.use_name}"
        hide_cmd_alt1 = f"module-hide --soft --hidden-loaded {writer_alt1.layout.use_name}"
        hide_cmd_alt2 = f"module-hide --soft --hidden-loaded {writer_alt2.layout.use_name}"
        assert len([x for x in content if hide_cmd == x]) == 1
        assert len([x for x in content if hide_cmd_alt1 == x]) == 1
        assert len([x for x in content if hide_cmd_alt2 == x]) == 1

        # one version is removed
        writer_alt1.remove()
        assert os.path.exists(writer.layout.modulerc)
        with open(writer.layout.modulerc) as f:
            content = [line.strip() for line in f.readlines()]
        assert len([x for x in content if hide_cmd == x]) == 1
        assert len([x for x in content if hide_cmd_alt1 == x]) == 0
        assert len([x for x in content if hide_cmd_alt2 == x]) == 1
