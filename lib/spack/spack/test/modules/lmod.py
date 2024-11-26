# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import archspec.cpu

import spack.config
import spack.environment as ev
import spack.main
import spack.modules.common
import spack.modules.lmod
import spack.spec
import spack.util.environment

mpich_spec_string = "mpich@3.0.4"
mpileaks_spec_string = "mpileaks"
libdwarf_spec_string = "libdwarf arch=x64-linux"

install = spack.main.SpackCommand("install")

#: Class of the writer tested in this module
writer_cls = spack.modules.lmod.LmodModulefileWriter

pytestmark = [
    pytest.mark.not_on_windows("does not run on windows"),
    pytest.mark.usefixtures("mock_modules_root"),
]


@pytest.fixture(params=["clang@=15.0.0", "gcc@=10.2.1"])
def compiler(request):
    return request.param


@pytest.fixture(
    params=[
        ("mpich@3.0.4", ("mpi",)),
        ("mpich@3.0.1", []),
        ("openblas@0.2.15", ("blas",)),
        ("openblas-with-lapack@0.2.15", ("blas", "lapack")),
        ("mpileaks@2.3", ("mpi",)),
        ("mpileaks@2.1", []),
    ]
)
def provider(request):
    return request.param


@pytest.mark.usefixtures("mutable_config", "mock_packages")
class TestLmod:
    @pytest.mark.regression("37788")
    @pytest.mark.parametrize("modules_config", ["core_compilers", "core_compilers_at_equal"])
    def test_layout_for_specs_compiled_with_core_compilers(
        self, modules_config, module_configuration, factory
    ):
        """Tests that specs compiled with core compilers are in the 'Core' folder. Also tests that
        we can use both ``compiler@version`` and ``compiler@=version`` to specify a core compiler.
        """
        module_configuration(modules_config)
        module, spec = factory("libelf%clang@15.0.0")
        assert "Core" in module.layout.available_path_parts

    def test_file_layout(self, compiler, provider, factory, module_configuration):
        """Tests the layout of files in the hierarchy is the one expected."""
        module_configuration("complex_hierarchy")
        spec_string, services = provider
        module, spec = factory(spec_string + "%" + compiler)

        layout = module.layout

        # Check that the services provided are in the hierarchy
        for s in services:
            assert s in layout.conf.hierarchy_tokens

        # Check that the compiler part of the path has no hash and that it
        # is transformed to r"Core" if the compiler is listed among core
        # compilers
        # Check that specs listed as core_specs are transformed to "Core"
        if compiler == "clang@=15.0.0" or spec_string == "mpich@3.0.1":
            assert "Core" in layout.available_path_parts
        else:
            assert compiler.replace("@=", "/") in layout.available_path_parts

        # Check that the provider part instead has always an hash even if
        # hash has been disallowed in the configuration file
        path_parts = layout.available_path_parts
        service_part = spec_string.replace("@", "/")
        service_part = "-".join([service_part, layout.spec.dag_hash(length=7)])

        if "mpileaks" in spec_string:
            # It's a user, not a provider, so create the provider string
            service_part = layout.spec["mpi"].format("{name}/{version}-{hash:7}")
        else:
            # Only relevant for providers, not users, of virtuals
            assert service_part in path_parts

        # Check that multi-providers have repetitions in path parts
        repetitions = len([x for x in path_parts if service_part == x])
        if spec_string == "openblas-with-lapack@0.2.15":
            assert repetitions == 2
        elif spec_string == "mpileaks@2.1":
            assert repetitions == 0
        else:
            assert repetitions == 1

    def test_compilers_provided_different_name(
        self, factory, module_configuration, compiler_factory
    ):
        with spack.config.override(
            "compilers", [compiler_factory(spec="clang@3.3", operating_system="debian6")]
        ):
            module_configuration("complex_hierarchy")
            module, spec = factory("intel-oneapi-compilers%clang@3.3")

            provides = module.conf.provides

            assert "compiler" in provides
            assert provides["compiler"] == spack.spec.CompilerSpec("oneapi@=3.0")

    def test_simple_case(self, modulefile_content, module_configuration):
        """Tests the generation of a simple Lua module file."""

        module_configuration("autoload_direct")
        content = modulefile_content(mpich_spec_string)

        assert "-- -*- lua -*-" in content
        assert "whatis([[Name : mpich]])" in content
        assert "whatis([[Version : 3.0.4]])" in content
        assert 'family("mpi")' in content

    def test_autoload_direct(self, modulefile_content, module_configuration):
        """Tests the automatic loading of direct dependencies."""

        module_configuration("autoload_direct")
        content = modulefile_content(mpileaks_spec_string)

        assert len([x for x in content if "depends_on(" in x]) == 2

    def test_autoload_all(self, modulefile_content, module_configuration):
        """Tests the automatic loading of all dependencies."""

        module_configuration("autoload_all")
        content = modulefile_content(mpileaks_spec_string)

        assert len([x for x in content if "depends_on(" in x]) == 5

    def test_alter_environment(self, modulefile_content, module_configuration):
        """Tests modifications to run-time environment."""

        module_configuration("alter_environment")
        content = modulefile_content("mpileaks platform=test target=x86_64")

        assert len([x for x in content if x.startswith('prepend_path("CMAKE_PREFIX_PATH"')]) == 0
        assert len([x for x in content if 'setenv("FOO", "foo")' in x]) == 1
        assert len([x for x in content if 'unsetenv("BAR")' in x]) == 1

        content = modulefile_content("libdwarf platform=test target=core2")

        assert len([x for x in content if x.startswith('prepend_path("CMAKE_PREFIX_PATH"')]) == 0
        assert len([x for x in content if 'setenv("FOO", "foo")' in x]) == 0
        assert len([x for x in content if 'unsetenv("BAR")' in x]) == 0

    def test_prepend_path_separator(self, modulefile_content, module_configuration):
        """Tests that we can use custom delimiters to manipulate path lists."""

        module_configuration("module_path_separator")
        content = modulefile_content("module-path-separator")

        assert len([x for x in content if 'append_path("COLON", "foo", ":")' in x]) == 1
        assert len([x for x in content if 'prepend_path("COLON", "foo", ":")' in x]) == 1
        assert len([x for x in content if 'remove_path("COLON", "foo", ":")' in x]) == 1
        assert len([x for x in content if 'append_path("SEMICOLON", "bar", ";")' in x]) == 1
        assert len([x for x in content if 'prepend_path("SEMICOLON", "bar", ";")' in x]) == 1
        assert len([x for x in content if 'remove_path("SEMICOLON", "bar", ";")' in x]) == 1
        assert len([x for x in content if 'append_path("SPACE", "qux", " ")' in x]) == 1
        assert len([x for x in content if 'remove_path("SPACE", "qux", " ")' in x]) == 1

    @pytest.mark.regression("11355")
    def test_manpath_setup(self, modulefile_content, module_configuration):
        """Tests specific setup of MANPATH environment variable."""

        module_configuration("autoload_direct")

        # no manpath set by module
        content = modulefile_content("mpileaks")
        assert len([x for x in content if 'append_path("MANPATH", "", ":")' in x]) == 0

        # manpath set by module with prepend_path
        content = modulefile_content("module-manpath-prepend")
        assert (
            len([x for x in content if 'prepend_path("MANPATH", "/path/to/man", ":")' in x]) == 1
        )
        assert (
            len([x for x in content if 'prepend_path("MANPATH", "/path/to/share/man", ":")' in x])
            == 1
        )
        assert len([x for x in content if 'append_path("MANPATH", "", ":")' in x]) == 1

        # manpath set by module with append_path
        content = modulefile_content("module-manpath-append")
        assert len([x for x in content if 'append_path("MANPATH", "/path/to/man", ":")' in x]) == 1
        assert len([x for x in content if 'append_path("MANPATH", "", ":")' in x]) == 1

        # manpath set by module with setenv
        content = modulefile_content("module-manpath-setenv")
        assert len([x for x in content if 'setenv("MANPATH", "/path/to/man")' in x]) == 1
        assert len([x for x in content if 'append_path("MANPATH", "", ":")' in x]) == 0

    @pytest.mark.regression("29578")
    def test_setenv_raw_value(self, modulefile_content, module_configuration):
        """Tests that we can set environment variable value without formatting it."""

        module_configuration("autoload_direct")
        content = modulefile_content("module-setenv-raw")

        assert len([x for x in content if 'setenv("FOO", "{{name}}, {name}, {{}}, {}")' in x]) == 1

    @pytest.mark.skipif(
        str(archspec.cpu.host().family) != "x86_64", reason="test data is specific for x86_64"
    )
    def test_help_message(self, modulefile_content, module_configuration):
        """Tests the generation of module help message."""

        module_configuration("autoload_direct")
        content = modulefile_content("mpileaks target=core2")

        help_msg = (
            "help([[Name   : mpileaks]])"
            "help([[Version: 2.3]])"
            "help([[Target : core2]])"
            "help()"
            "help([[Mpileaks is a mock package that passes audits]])"
        )
        assert help_msg in "".join(content)

        content = modulefile_content("libdwarf target=core2")

        help_msg = (
            "help([[Name   : libdwarf]])"
            "help([[Version: 20130729]])"
            "help([[Target : core2]])"
            "depends_on("
        )
        assert help_msg in "".join(content)

        content = modulefile_content("module-long-help target=core2")

        help_msg = (
            "help([[Name   : module-long-help]])"
            "help([[Version: 1.0]])"
            "help([[Target : core2]])"
            "help()"
            "help([[Package to test long description message generated in modulefile."
            "Message too long is wrapped over multiple lines.]])"
        )
        assert help_msg in "".join(content)

    def test_exclude(self, modulefile_content, module_configuration):
        """Tests excluding the generation of selected modules."""
        module_configuration("exclude")
        content = modulefile_content(mpileaks_spec_string)

        assert len([x for x in content if "depends_on(" in x]) == 1

    def test_no_hash(self, factory, module_configuration):
        """Makes sure that virtual providers (in the hierarchy) always
        include a hash. Make sure that the module file for the spec
        does not include a hash if hash_length is 0.
        """

        module_configuration("no_hash")
        module, spec = factory(mpileaks_spec_string)
        path = module.layout.filename
        mpi_spec = spec["mpi"]

        mpi_element = "{0}/{1}-{2}/".format(
            mpi_spec.name, mpi_spec.version, mpi_spec.dag_hash(length=7)
        )

        assert mpi_element in path

        mpileaks_spec = spec
        mpileaks_element = "{0}/{1}.lua".format(mpileaks_spec.name, mpileaks_spec.version)

        assert path.endswith(mpileaks_element)

    def test_no_core_compilers(self, factory, module_configuration):
        """Ensures that missing 'core_compilers' in the configuration file
        raises the right exception.
        """

        # In this case we miss the entry completely
        module_configuration("missing_core_compilers")

        module, spec = factory(mpileaks_spec_string)
        with pytest.raises(spack.modules.lmod.CoreCompilersNotFoundError):
            module.write()

        # Here we have an empty list
        module_configuration("core_compilers_empty")

        module, spec = factory(mpileaks_spec_string)
        with pytest.raises(spack.modules.lmod.CoreCompilersNotFoundError):
            module.write()

    def test_non_virtual_in_hierarchy(self, factory, module_configuration):
        """Ensures that if a non-virtual is in hierarchy, an exception will
        be raised.
        """
        module_configuration("non_virtual_in_hierarchy")

        module, spec = factory(mpileaks_spec_string)
        with pytest.raises(spack.modules.lmod.NonVirtualInHierarchyError):
            module.write()

    def test_conflicts(self, modulefile_content, module_configuration):
        """Tests adding conflicts to the module."""

        # This configuration has no error, so check the conflicts directives
        # are there
        module_configuration("conflicts")
        content = modulefile_content("mpileaks")

        assert len([x for x in content if x.startswith("conflict")]) == 2
        assert len([x for x in content if x == 'conflict("mpileaks")']) == 1
        assert len([x for x in content if x == 'conflict("intel/14.0.1")']) == 1

    def test_inconsistent_conflict_in_modules_yaml(self, modulefile_content, module_configuration):
        """Tests inconsistent conflict definition in `modules.yaml`."""

        # This configuration is inconsistent, check an error is raised
        module_configuration("wrong_conflicts")
        with pytest.raises(spack.modules.common.ModulesError):
            modulefile_content("mpileaks")

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

    def test_external_configure_args(self, factory):
        # If this package is detected as an external, its configure option line
        # in the module file starts with 'unknown'
        writer, spec = factory("externaltool")

        assert "unknown" in writer.context.configure_options

    def test_guess_core_compilers(self, factory, module_configuration, monkeypatch):
        """Check that we can guess core compilers."""

        # In this case we miss the entry completely
        module_configuration("missing_core_compilers")

        # Our mock paths must be detected as system paths
        monkeypatch.setattr(spack.util.environment, "SYSTEM_DIRS", ["/path/to"])

        # We don't want to really write into user configuration
        # when running tests
        def no_op_set(*args, **kwargs):
            pass

        monkeypatch.setattr(spack.config, "set", no_op_set)

        # Assert we have core compilers now
        writer, _ = factory(mpileaks_spec_string)
        assert writer.conf.core_compilers

    @pytest.mark.parametrize(
        "spec_str", ["mpileaks target=nocona", "mpileaks target=core2", "mpileaks target=x86_64"]
    )
    @pytest.mark.regression("13005")
    def test_only_generic_microarchitectures_in_root(
        self, spec_str, factory, module_configuration
    ):
        module_configuration("complex_hierarchy")
        writer, spec = factory(spec_str)

        assert str(spec.target.family) in writer.layout.arch_dirname
        if spec.target.family != spec.target:
            assert str(spec.target) not in writer.layout.arch_dirname

    def test_projections_specific(self, factory, module_configuration):
        """Tests reading the correct naming scheme."""

        # This configuration has no error, so check the conflicts directives
        # are there
        module_configuration("projections")

        # Test we read the expected configuration for the naming scheme
        writer, _ = factory("mpileaks")
        expected = {"all": "{name}/v{version}", "mpileaks": "{name}-mpiprojection"}

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
        expected = {"all": "{name}/v{version}", "mpileaks": "{name}-mpiprojection"}

        assert writer.conf.projections == expected
        projection = writer.spec.format(writer.conf.projections["all"])
        assert projection in writer.layout.use_name

    def test_modules_relative_to_view(
        self, tmpdir, modulefile_content, module_configuration, install_mockery, mock_fetch
    ):
        with ev.create_in_dir(str(tmpdir), with_view=True) as e:
            module_configuration("with_view")
            install("--add", "cmake")

            spec = spack.spec.Spec("cmake").concretized()

            content = modulefile_content("cmake")
            expected = e.default_view.get_projection_for_spec(spec)
            # Rather than parse all lines, ensure all prefixes in the content
            # point to the right one
            assert any(expected in line for line in content)
            assert not any(spec.prefix in line for line in content)

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
        hide_implicit_mpileaks = f'hide_version("{writer.layout.use_name}")'
        assert len([x for x in content if hide_implicit_mpileaks == x]) == 1

        # The direct dependencies are all implicitly installed, and they should all be hidden,
        # except for mpich, which is provider for mpi, which is in the hierarchy, and therefore
        # can't be hidden. All other hidden modules should have a 7 character hash (the config
        # hash_length = 0 only applies to exposed modules).
        with open(writer.layout.filename) as f:
            depends_statements = [line.strip() for line in f.readlines() if "depends_on" in line]
            for dep in spec.dependencies(deptype=("link", "run")):
                if dep.satisfies("mpi"):
                    assert not any(dep.dag_hash(7) in line for line in depends_statements)
                else:
                    assert any(dep.dag_hash(7) in line for line in depends_statements)

        # when mpileaks becomes explicit, its file name changes (hash_length = 0), meaning an
        # extra module file is created; the old one still exists and remains hidden.
        writer = writer_cls(spec, "default", True)
        writer.write()
        assert os.path.exists(writer.layout.modulerc)
        with open(writer.layout.modulerc) as f:
            content = [line.strip() for line in f.readlines()]
        assert hide_implicit_mpileaks in content  # old, implicit mpileaks is still hidden
        assert f'hide_version("{writer.layout.use_name}")' not in content

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
        hide_cmd = f'hide_version("{writer.layout.use_name}")'
        hide_cmd_alt1 = f'hide_version("{writer_alt1.layout.use_name}")'
        hide_cmd_alt2 = f'hide_version("{writer_alt2.layout.use_name}")'
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
