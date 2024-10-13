# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import platform
import posixpath
import sys

import pytest

import archspec.cpu

from llnl.path import Path, convert_to_platform_path
from llnl.util.filesystem import HeaderList, LibraryList

import spack.build_environment
import spack.config
import spack.deptypes as dt
import spack.package_base
import spack.paths
import spack.spec
import spack.util.spack_yaml as syaml
from spack.build_environment import UseMode, _static_to_shared_library, dso_suffix
from spack.context import Context
from spack.installer import PackageInstaller
from spack.paths import build_env_path
from spack.util.environment import EnvironmentModifications
from spack.util.executable import Executable


def os_pathsep_join(path, *pths):
    out_pth = path
    for pth in pths:
        out_pth = os.pathsep.join([out_pth, pth])
    return out_pth


def prep_and_join(path, *pths):
    return os.path.sep + os.path.join(path, *pths)


@pytest.fixture
def build_environment(working_env):
    cc = Executable(os.path.join(build_env_path, "cc"))
    cxx = Executable(os.path.join(build_env_path, "c++"))
    fc = Executable(os.path.join(build_env_path, "fc"))

    realcc = "/bin/mycc"
    prefix = "/spack-test-prefix"

    os.environ["SPACK_CC"] = realcc
    os.environ["SPACK_CXX"] = realcc
    os.environ["SPACK_FC"] = realcc

    os.environ["SPACK_PREFIX"] = prefix
    os.environ["SPACK_ENV_PATH"] = "test"
    os.environ["SPACK_DEBUG_LOG_DIR"] = "."
    os.environ["SPACK_DEBUG_LOG_ID"] = "foo-hashabc"
    os.environ["SPACK_COMPILER_SPEC"] = "gcc@4.4.7"
    os.environ["SPACK_SHORT_SPEC"] = "foo@1.2 arch=linux-rhel6-x86_64 /hashabc"

    os.environ["SPACK_CC_RPATH_ARG"] = "-Wl,-rpath,"
    os.environ["SPACK_CXX_RPATH_ARG"] = "-Wl,-rpath,"
    os.environ["SPACK_F77_RPATH_ARG"] = "-Wl,-rpath,"
    os.environ["SPACK_FC_RPATH_ARG"] = "-Wl,-rpath,"
    os.environ["SPACK_LINKER_ARG"] = "-Wl,"
    os.environ["SPACK_DTAGS_TO_ADD"] = "--disable-new-dtags"
    os.environ["SPACK_DTAGS_TO_STRIP"] = "--enable-new-dtags"
    os.environ["SPACK_SYSTEM_DIRS"] = "/usr/include|/usr/lib"
    os.environ["SPACK_MANAGED_DIRS"] = f"{prefix}/opt/spack"
    os.environ["SPACK_TARGET_ARGS"] = ""

    if "SPACK_DEPENDENCIES" in os.environ:
        del os.environ["SPACK_DEPENDENCIES"]

    yield {"cc": cc, "cxx": cxx, "fc": fc}

    for name in (
        "SPACK_CC",
        "SPACK_CXX",
        "SPACK_FC",
        "SPACK_PREFIX",
        "SPACK_ENV_PATH",
        "SPACK_DEBUG_LOG_DIR",
        "SPACK_COMPILER_SPEC",
        "SPACK_SHORT_SPEC",
        "SPACK_CC_RPATH_ARG",
        "SPACK_CXX_RPATH_ARG",
        "SPACK_F77_RPATH_ARG",
        "SPACK_FC_RPATH_ARG",
        "SPACK_TARGET_ARGS",
    ):
        del os.environ[name]


@pytest.fixture
def ensure_env_variables(config, mock_packages, monkeypatch, working_env):
    """Returns a function that takes a dictionary and updates os.environ
    for the test lifetime accordingly. Plugs-in mock config and repo.
    """

    def _ensure(env_mods):
        for name, value in env_mods.items():
            monkeypatch.setenv(name, value)

    return _ensure


@pytest.fixture
def mock_module_cmd(monkeypatch):
    class Logger:
        def __init__(self, fn=None):
            self.fn = fn
            self.calls = []

        def __call__(self, *args, **kwargs):
            self.calls.append((args, kwargs))
            if self.fn:
                return self.fn(*args, **kwargs)

    mock_module_cmd = Logger()
    monkeypatch.setattr(spack.build_environment, "module", mock_module_cmd)
    monkeypatch.setattr(spack.build_environment, "_on_cray", lambda: (True, None))
    return mock_module_cmd


@pytest.mark.not_on_windows("Static to Shared not supported on Win (yet)")
def test_static_to_shared_library(build_environment):
    os.environ["SPACK_TEST_COMMAND"] = "dump-args"

    expected = {
        "linux": (
            "/bin/mycc -shared"
            " -Wl,--disable-new-dtags"
            " -Wl,-soname -Wl,{2} -Wl,--whole-archive {0}"
            " -Wl,--no-whole-archive -o {1}"
        ),
        "darwin": (
            "/bin/mycc -dynamiclib"
            " -Wl,--disable-new-dtags"
            " -install_name {1} -Wl,-force_load -Wl,{0} -o {1}"
        ),
    }

    static_lib = "/spack/libfoo.a"

    for arch in ("linux", "darwin"):
        for shared_lib in (None, "/spack/libbar.so"):
            output = _static_to_shared_library(
                arch, build_environment["cc"], static_lib, shared_lib, compiler_output=str
            ).strip()

            if not shared_lib:
                shared_lib = "{0}.{1}".format(os.path.splitext(static_lib)[0], dso_suffix)

            assert set(output.split()) == set(
                expected[arch].format(static_lib, shared_lib, os.path.basename(shared_lib)).split()
            )


@pytest.mark.regression("8345")
@pytest.mark.usefixtures("config", "mock_packages")
def test_cc_not_changed_by_modules(monkeypatch, working_env):
    s = spack.spec.Spec("cmake")
    s.concretize()
    pkg = s.package

    def _set_wrong_cc(x):
        os.environ["CC"] = "NOT_THIS_PLEASE"
        os.environ["ANOTHER_VAR"] = "THIS_IS_SET"

    monkeypatch.setattr(spack.build_environment, "load_module", _set_wrong_cc)
    monkeypatch.setattr(pkg.compiler, "modules", ["some_module"])

    spack.build_environment.setup_package(pkg, False)

    assert os.environ["CC"] != "NOT_THIS_PLEASE"
    assert os.environ["ANOTHER_VAR"] == "THIS_IS_SET"


def test_setup_dependent_package_inherited_modules(
    working_env, mock_packages, install_mockery, mock_fetch
):
    # This will raise on regression
    s = spack.spec.Spec("cmake-client-inheritor").concretized()
    PackageInstaller([s.package]).install()


@pytest.mark.parametrize(
    "initial,modifications,expected",
    [
        # Set and unset variables
        (
            {"SOME_VAR_STR": "", "SOME_VAR_NUM": "0"},
            {"set": {"SOME_VAR_STR": "SOME_STR", "SOME_VAR_NUM": 1}},
            {"SOME_VAR_STR": "SOME_STR", "SOME_VAR_NUM": "1"},
        ),
        ({"SOME_VAR_STR": ""}, {"unset": ["SOME_VAR_STR"]}, {"SOME_VAR_STR": None}),
        (
            {},  # Set a variable that was not defined already
            {"set": {"SOME_VAR_STR": "SOME_STR"}},
            {"SOME_VAR_STR": "SOME_STR"},
        ),
        # Append and prepend to the same variable
        (
            {"EMPTY_PATH_LIST": prep_and_join("path", "middle")},
            {
                "prepend_path": {"EMPTY_PATH_LIST": prep_and_join("path", "first")},
                "append_path": {"EMPTY_PATH_LIST": prep_and_join("path", "last")},
            },
            {
                "EMPTY_PATH_LIST": os_pathsep_join(
                    prep_and_join("path", "first"),
                    prep_and_join("path", "middle"),
                    prep_and_join("path", "last"),
                )
            },
        ),
        # Append and prepend from empty variables
        (
            {"EMPTY_PATH_LIST": "", "SOME_VAR_STR": ""},
            {
                "prepend_path": {"EMPTY_PATH_LIST": prep_and_join("path", "first")},
                "append_path": {"SOME_VAR_STR": prep_and_join("path", "last")},
            },
            {
                "EMPTY_PATH_LIST": prep_and_join("path", "first"),
                "SOME_VAR_STR": prep_and_join("path", "last"),
            },
        ),
        (
            {},  # Same as before but on variables that were not defined
            {
                "prepend_path": {"EMPTY_PATH_LIST": prep_and_join("path", "first")},
                "append_path": {"SOME_VAR_STR": prep_and_join("path", "last")},
            },
            {
                "EMPTY_PATH_LIST": prep_and_join("path", "first"),
                "SOME_VAR_STR": prep_and_join("path", "last"),
            },
        ),
        # Remove a path from a list
        (
            {
                "EMPTY_PATH_LIST": os_pathsep_join(
                    prep_and_join("path", "first"),
                    prep_and_join("path", "middle"),
                    prep_and_join("path", "last"),
                )
            },
            {"remove_path": {"EMPTY_PATH_LIST": prep_and_join("path", "middle")}},
            {
                "EMPTY_PATH_LIST": os_pathsep_join(
                    prep_and_join("path", "first"), prep_and_join("path", "last")
                )
            },
        ),
        (
            {"EMPTY_PATH_LIST": prep_and_join("only", "path")},
            {"remove_path": {"EMPTY_PATH_LIST": prep_and_join("only", "path")}},
            {"EMPTY_PATH_LIST": ""},
        ),
    ],
)
def test_compiler_config_modifications(
    initial, modifications, expected, ensure_env_variables, monkeypatch
):
    # Set the environment as per prerequisites
    ensure_env_variables(initial)

    def platform_pathsep(pathlist):
        if Path.platform_path == Path.windows:
            pathlist = pathlist.replace(":", ";")

        return convert_to_platform_path(pathlist)

    # Monkeypatch a pkg.compiler.environment with the required modifications
    pkg = spack.spec.Spec("cmake").concretized().package
    monkeypatch.setattr(pkg.compiler, "environment", modifications)
    # Trigger the modifications
    spack.build_environment.setup_package(pkg, False)

    # Check they were applied
    for name, value in expected.items():
        if value is not None:
            value = platform_pathsep(value)
            assert os.environ[name] == value
            continue
        assert name not in os.environ


def test_compiler_custom_env(config, mock_packages, monkeypatch, working_env):
    if sys.platform == "win32":
        test_path = r"C:\test\path\element\custom-env" + "\\"
    else:
        test_path = r"/test/path/element/custom-env/"

    def custom_env(pkg, env):
        env.prepend_path("PATH", test_path)
        env.append_flags("ENV_CUSTOM_CC_FLAGS", "--custom-env-flag1")

    pkg = spack.spec.Spec("cmake").concretized().package
    monkeypatch.setattr(pkg.compiler, "setup_custom_environment", custom_env)
    spack.build_environment.setup_package(pkg, False)

    # Note: trailing slash may be stripped by internal logic
    assert test_path[:-1] in os.environ["PATH"]
    assert "--custom-env-flag1" in os.environ["ENV_CUSTOM_CC_FLAGS"]


def test_external_config_env(mock_packages, mutable_config, working_env):
    cmake_config = {
        "externals": [
            {
                "spec": "cmake@1.0",
                "prefix": "/fake/path",
                "extra_attributes": {"environment": {"set": {"TEST_ENV_VAR_SET": "yes it's set"}}},
            }
        ]
    }
    spack.config.set("packages:cmake", cmake_config)

    cmake_client = spack.spec.Spec("cmake-client").concretized()
    spack.build_environment.setup_package(cmake_client.package, False)

    assert os.environ["TEST_ENV_VAR_SET"] == "yes it's set"


@pytest.mark.regression("9107")
def test_spack_paths_before_module_paths(config, mock_packages, monkeypatch, working_env):
    s = spack.spec.Spec("cmake")
    s.concretize()
    pkg = s.package

    module_path = os.path.join("path", "to", "module")

    def _set_wrong_cc(x):
        os.environ["PATH"] = module_path + os.pathsep + os.environ["PATH"]

    monkeypatch.setattr(spack.build_environment, "load_module", _set_wrong_cc)
    monkeypatch.setattr(pkg.compiler, "modules", ["some_module"])

    spack.build_environment.setup_package(pkg, False)

    spack_path = os.path.join(spack.paths.prefix, os.path.join("lib", "spack", "env"))

    paths = os.environ["PATH"].split(os.pathsep)

    assert paths.index(spack_path) < paths.index(module_path)


def test_package_inheritance_module_setup(config, mock_packages, working_env):
    s = spack.spec.Spec("multimodule-inheritance")
    s.concretize()
    pkg = s.package

    spack.build_environment.setup_package(pkg, False)

    os.environ["TEST_MODULE_VAR"] = "failed"

    assert pkg.use_module_variable() == "test_module_variable"
    assert os.environ["TEST_MODULE_VAR"] == "test_module_variable"


def test_wrapper_variables(
    config, mock_packages, working_env, monkeypatch, installation_dir_with_headers
):
    """Check that build_environment supplies the needed library/include
    directories via the SPACK_LINK_DIRS and SPACK_INCLUDE_DIRS environment
    variables.
    """

    # https://github.com/spack/spack/issues/13969
    cuda_headers = HeaderList(
        [
            "prefix/include/cuda_runtime.h",
            "prefix/include/cuda/atomic",
            "prefix/include/cuda/std/detail/libcxx/include/ctype.h",
        ]
    )
    cuda_include_dirs = cuda_headers.directories
    assert posixpath.join("prefix", "include") in cuda_include_dirs
    assert (
        posixpath.join("prefix", "include", "cuda", "std", "detail", "libcxx", "include")
        not in cuda_include_dirs
    )

    root = spack.spec.Spec("dt-diamond")
    root.concretize()

    for s in root.traverse():
        s.prefix = "/{0}-prefix/".format(s.name)

    dep_pkg = root["dt-diamond-left"].package
    dep_lib_paths = ["/test/path/to/ex1.so", "/test/path/to/subdir/ex2.so"]
    dep_lib_dirs = ["/test/path/to", "/test/path/to/subdir"]
    dep_libs = LibraryList(dep_lib_paths)

    dep2_pkg = root["dt-diamond-right"].package
    dep2_pkg.spec.prefix = str(installation_dir_with_headers)

    setattr(dep_pkg, "libs", dep_libs)
    try:
        pkg = root.package
        env_mods = EnvironmentModifications()
        spack.build_environment.set_wrapper_variables(pkg, env_mods)

        env_mods.apply_modifications()

        def normpaths(paths):
            return list(os.path.normpath(p) for p in paths)

        link_dir_var = os.environ["SPACK_LINK_DIRS"]
        assert normpaths(link_dir_var.split(":")) == normpaths(dep_lib_dirs)

        root_libdirs = ["/dt-diamond-prefix/lib", "/dt-diamond-prefix/lib64"]
        rpath_dir_var = os.environ["SPACK_RPATH_DIRS"]
        # The 'lib' and 'lib64' subdirectories of the root package prefix
        # should always be rpathed and should be the first rpaths
        assert normpaths(rpath_dir_var.split(":")) == normpaths(root_libdirs + dep_lib_dirs)

        header_dir_var = os.environ["SPACK_INCLUDE_DIRS"]

        # The default implementation looks for header files only
        # in <prefix>/include and subdirectories
        prefix = str(installation_dir_with_headers)
        include_dirs = normpaths(header_dir_var.split(os.pathsep))

        assert os.path.join(prefix, "include") in include_dirs
        assert os.path.join(prefix, "include", "boost") not in include_dirs
        assert os.path.join(prefix, "path", "to") not in include_dirs
        assert os.path.join(prefix, "path", "to", "subdir") not in include_dirs

    finally:
        delattr(dep_pkg, "libs")


def test_external_prefixes_last(mutable_config, mock_packages, working_env, monkeypatch):
    # Sanity check: under normal circumstances paths associated with
    # dt-diamond-left would appear first. We'll mark it as external in
    # the test to check if the associated paths are placed last.
    assert "dt-diamond-left" < "dt-diamond-right"

    cfg_data = syaml.load_config(
        """\
dt-diamond-left:
  externals:
  - spec: dt-diamond-left@1.0
    prefix: /fake/path1
  buildable: false
"""
    )
    spack.config.set("packages", cfg_data)
    top = spack.spec.Spec("dt-diamond").concretized()

    def _trust_me_its_a_dir(path):
        return True

    monkeypatch.setattr(os.path, "isdir", _trust_me_its_a_dir)

    env_mods = EnvironmentModifications()
    spack.build_environment.set_wrapper_variables(top.package, env_mods)

    env_mods.apply_modifications()
    link_dir_var = os.environ["SPACK_LINK_DIRS"]
    link_dirs = link_dir_var.split(":")
    external_lib_paths = set(
        [os.path.normpath("/fake/path1/lib"), os.path.normpath("/fake/path1/lib64")]
    )
    # The external lib paths should be the last two entries of the list and
    # should not appear anywhere before the last two entries
    assert set(os.path.normpath(x) for x in link_dirs[-2:]) == external_lib_paths
    assert not (set(os.path.normpath(x) for x in link_dirs[:-2]) & external_lib_paths)


def test_parallel_false_is_not_propagating(default_mock_concretization):
    """Test that parallel=False is not propagating to dependencies"""
    # a foobar=bar (parallel = False)
    # |
    # b (parallel =True)
    s = default_mock_concretization("pkg-a foobar=bar")

    spack.build_environment.set_package_py_globals(s.package, context=Context.BUILD)
    assert s["pkg-a"].package.module.make_jobs == 1

    spack.build_environment.set_package_py_globals(s["pkg-b"].package, context=Context.BUILD)
    assert s["pkg-b"].package.module.make_jobs == spack.config.determine_number_of_jobs(
        parallel=s["pkg-b"].package.parallel
    )


@pytest.mark.parametrize(
    "config_setting,expected_flag",
    [
        ("runpath", "" if platform.system() == "Darwin" else "--enable-new-dtags"),
        ("rpath", "" if platform.system() == "Darwin" else "--disable-new-dtags"),
    ],
)
def test_setting_dtags_based_on_config(config_setting, expected_flag, config, mock_packages):
    # Pick a random package to be able to set compiler's variables
    s = spack.spec.Spec("cmake")
    s.concretize()
    pkg = s.package

    env = EnvironmentModifications()
    with spack.config.override("config:shared_linking", {"type": config_setting, "bind": False}):
        spack.build_environment.set_compiler_environment_variables(pkg, env)
        modifications = env.group_by_name()
        assert "SPACK_DTAGS_TO_STRIP" in modifications
        assert "SPACK_DTAGS_TO_ADD" in modifications
        assert len(modifications["SPACK_DTAGS_TO_ADD"]) == 1
        assert len(modifications["SPACK_DTAGS_TO_STRIP"]) == 1

        dtags_to_add = modifications["SPACK_DTAGS_TO_ADD"][0]
        assert dtags_to_add.value == expected_flag


def test_build_jobs_sequential_is_sequential():
    assert (
        spack.config.determine_number_of_jobs(
            parallel=False,
            max_cpus=8,
            config=spack.config.Configuration(
                spack.config.InternalConfigScope("command_line", {"config": {"build_jobs": 8}}),
                spack.config.InternalConfigScope("defaults", {"config": {"build_jobs": 8}}),
            ),
        )
        == 1
    )


def test_build_jobs_command_line_overrides():
    assert (
        spack.config.determine_number_of_jobs(
            parallel=True,
            max_cpus=1,
            config=spack.config.Configuration(
                spack.config.InternalConfigScope("command_line", {"config": {"build_jobs": 10}}),
                spack.config.InternalConfigScope("defaults", {"config": {"build_jobs": 1}}),
            ),
        )
        == 10
    )
    assert (
        spack.config.determine_number_of_jobs(
            parallel=True,
            max_cpus=100,
            config=spack.config.Configuration(
                spack.config.InternalConfigScope("command_line", {"config": {"build_jobs": 10}}),
                spack.config.InternalConfigScope("defaults", {"config": {"build_jobs": 100}}),
            ),
        )
        == 10
    )


def test_build_jobs_defaults():
    assert (
        spack.config.determine_number_of_jobs(
            parallel=True,
            max_cpus=10,
            config=spack.config.Configuration(
                spack.config.InternalConfigScope("defaults", {"config": {"build_jobs": 1}})
            ),
        )
        == 1
    )
    assert (
        spack.config.determine_number_of_jobs(
            parallel=True,
            max_cpus=10,
            config=spack.config.Configuration(
                spack.config.InternalConfigScope("defaults", {"config": {"build_jobs": 100}})
            ),
        )
        == 10
    )


class TestModuleMonkeyPatcher:
    def test_getting_attributes(self, default_mock_concretization):
        s = default_mock_concretization("libelf")
        module_wrapper = spack.build_environment.ModuleChangePropagator(s.package)
        assert module_wrapper.Libelf == s.package.module.Libelf

    def test_setting_attributes(self, default_mock_concretization):
        s = default_mock_concretization("libelf")
        module = s.package.module
        module_wrapper = spack.build_environment.ModuleChangePropagator(s.package)

        # Setting an attribute has an immediate effect
        module_wrapper.SOME_ATTRIBUTE = 1
        assert module.SOME_ATTRIBUTE == 1

        # We can also propagate the settings to classes in the MRO
        module_wrapper.propagate_changes_to_mro()
        for cls in s.package.__class__.__mro__:
            current_module = cls.module
            if current_module == spack.package_base:
                break
            assert current_module.SOME_ATTRIBUTE == 1


def test_effective_deptype_build_environment(default_mock_concretization):
    s = default_mock_concretization("dttop")

    #  [    ]  dttop@1.0                    #
    #  [b   ]      ^dtbuild1@1.0            # <- direct build dep
    #  [b   ]          ^dtbuild2@1.0        # <- indirect build-only dep is dropped
    #  [bl  ]          ^dtlink2@1.0         # <- linkable, and runtime dep of build dep
    #  [  r ]          ^dtrun2@1.0          # <- non-linkable, exectuable runtime dep of build dep
    #  [bl  ]      ^dtlink1@1.0             # <- direct build dep
    #  [bl  ]          ^dtlink3@1.0         # <- linkable, and runtime dep of build dep
    #  [b   ]              ^dtbuild2@1.0    # <- indirect build-only dep is dropped
    #  [bl  ]              ^dtlink4@1.0     # <- linkable, and runtime dep of build dep
    #  [  r ]      ^dtrun1@1.0              # <- run-only dep is pruned (should it be in PATH?)
    #  [bl  ]          ^dtlink5@1.0         # <- children too
    #  [  r ]          ^dtrun3@1.0          # <- children too
    #  [b   ]              ^dtbuild3@1.0    # <- children too

    expected_flags = {
        "dttop": UseMode.ROOT,
        "dtbuild1": UseMode.BUILDTIME_DIRECT,
        "dtlink1": UseMode.BUILDTIME_DIRECT | UseMode.BUILDTIME,
        "dtlink3": UseMode.BUILDTIME | UseMode.RUNTIME,
        "dtlink4": UseMode.BUILDTIME | UseMode.RUNTIME,
        "dtrun2": UseMode.RUNTIME | UseMode.RUNTIME_EXECUTABLE,
        "dtlink2": UseMode.RUNTIME,
    }

    for spec, effective_type in spack.build_environment.effective_deptypes(
        s, context=Context.BUILD
    ):
        assert effective_type & expected_flags.pop(spec.name) == effective_type
    assert not expected_flags, f"Missing {expected_flags.keys()} from effective_deptypes"


def test_effective_deptype_run_environment(default_mock_concretization):
    s = default_mock_concretization("dttop")

    #  [    ]  dttop@1.0                    #
    #  [b   ]      ^dtbuild1@1.0            # <- direct build-only dep is pruned
    #  [b   ]          ^dtbuild2@1.0        # <- children too
    #  [bl  ]          ^dtlink2@1.0         # <- children too
    #  [  r ]          ^dtrun2@1.0          # <- children too
    #  [bl  ]      ^dtlink1@1.0             # <- runtime, not executable
    #  [bl  ]          ^dtlink3@1.0         # <- runtime, not executable
    #  [b   ]              ^dtbuild2@1.0    # <- indirect build only dep is pruned
    #  [bl  ]              ^dtlink4@1.0     # <- runtime, not executable
    #  [  r ]      ^dtrun1@1.0              # <- runtime and executable
    #  [bl  ]          ^dtlink5@1.0         # <- runtime, not executable
    #  [  r ]          ^dtrun3@1.0          # <- runtime and executable
    #  [b   ]              ^dtbuild3@1.0    # <- indirect build-only dep is pruned

    expected_flags = {
        "dttop": UseMode.ROOT,
        "dtlink1": UseMode.RUNTIME,
        "dtlink3": UseMode.BUILDTIME | UseMode.RUNTIME,
        "dtlink4": UseMode.BUILDTIME | UseMode.RUNTIME,
        "dtrun1": UseMode.RUNTIME | UseMode.RUNTIME_EXECUTABLE,
        "dtlink5": UseMode.RUNTIME,
        "dtrun3": UseMode.RUNTIME | UseMode.RUNTIME_EXECUTABLE,
    }

    for spec, effective_type in spack.build_environment.effective_deptypes(s, context=Context.RUN):
        assert effective_type & expected_flags.pop(spec.name) == effective_type
    assert not expected_flags, f"Missing {expected_flags.keys()} from effective_deptypes"


def test_monkey_patching_works_across_virtual(default_mock_concretization):
    """Assert that a monkeypatched attribute is found regardless we access through the
    real name or the virtual name.
    """
    s = default_mock_concretization("mpileaks ^mpich")
    s["mpich"].foo = "foo"
    assert s["mpich"].foo == "foo"
    assert s["mpi"].foo == "foo"


def test_clear_compiler_related_runtime_variables_of_build_deps(default_mock_concretization):
    """Verify that Spack drops CC, CXX, FC and F77 from the dependencies related build environment
    variable changes if they are set in setup_run_environment. Spack manages those variables
    elsewhere."""
    s = default_mock_concretization("build-env-compiler-var-a")
    ctx = spack.build_environment.SetupContext(s, context=Context.BUILD)
    result = {}
    ctx.get_env_modifications().apply_modifications(result)
    assert "CC" not in result
    assert "CXX" not in result
    assert "FC" not in result
    assert "F77" not in result
    assert result["ANOTHER_VAR"] == "this-should-be-present"


@pytest.mark.parametrize("context", [Context.BUILD, Context.RUN])
def test_build_system_globals_only_set_on_root_during_build(default_mock_concretization, context):
    """Test whether when setting up a build environment, the build related globals are set only
    in the top level spec.

    TODO: Since module instances are globals themselves, and Spack defines properties on them, they
    persist across tests. In principle this is not terrible, cause the variables are mostly static.
    But obviously it can lead to very hard to find bugs... We should get rid of those globals and
    define them instead as a property on the package instance.
    """
    root = spack.spec.Spec("mpileaks").concretized()
    build_variables = ("std_cmake_args", "std_meson_args", "std_pip_args")

    # See todo above, we clear out any properties that may have been set by the previous test.
    # Commenting this loop will make the test fail. I'm leaving it here as a reminder that those
    # globals were always a bad idea, and we should pass them to the package instance.
    for spec in root.traverse():
        for variable in build_variables:
            spec.package.module.__dict__.pop(variable, None)

    spack.build_environment.SetupContext(root, context=context).set_all_package_py_globals()

    # Excpect the globals to be set at the root in a build context only.
    should_be_set = lambda depth: context == Context.BUILD and depth == 0

    for depth, spec in root.traverse(depth=True, root=True):
        for variable in build_variables:
            assert hasattr(spec.package.module, variable) == should_be_set(depth)


def test_rpath_with_duplicate_link_deps():
    """If we have two instances of one package in the same link sub-dag, only the newest version is
    rpath'ed. This is for runtime support without splicing."""
    runtime_1 = spack.spec.Spec("runtime@=1.0")
    runtime_2 = spack.spec.Spec("runtime@=2.0")
    child = spack.spec.Spec("child@=1.0")
    root = spack.spec.Spec("root@=1.0")

    root.add_dependency_edge(child, depflag=dt.LINK, virtuals=())
    root.add_dependency_edge(runtime_2, depflag=dt.LINK, virtuals=())
    child.add_dependency_edge(runtime_1, depflag=dt.LINK, virtuals=())

    rpath_deps = spack.build_environment._get_rpath_deps_from_spec(root, transitive_rpaths=True)
    assert child in rpath_deps
    assert runtime_2 in rpath_deps
    assert runtime_1 not in rpath_deps


@pytest.mark.parametrize(
    "compiler_spec,target_name,expected_flags",
    [
        # Homogeneous compilers
        ("gcc@4.7.2", "ivybridge", "-march=core-avx-i -mtune=core-avx-i"),
        ("clang@3.5", "x86_64", "-march=x86-64 -mtune=generic"),
        ("apple-clang@9.1.0", "x86_64", "-march=x86-64"),
        # Mixed toolchain
        ("clang@8.0.0", "broadwell", ""),
    ],
)
@pytest.mark.filterwarnings("ignore:microarchitecture specific")
@pytest.mark.not_on_windows("Windows doesn't support the compiler wrapper")
def test_optimization_flags(compiler_spec, target_name, expected_flags, compiler_factory):
    target = archspec.cpu.TARGETS[target_name]
    compiler_dict = compiler_factory(spec=compiler_spec, operating_system="")["compiler"]
    if compiler_spec == "clang@8.0.0":
        compiler_dict["paths"] = {
            "cc": "/path/to/clang-8",
            "cxx": "/path/to/clang++-8",
            "f77": "/path/to/gfortran-9",
            "fc": "/path/to/gfortran-9",
        }
    compiler = spack.compilers.compiler_from_dict(compiler_dict)
    opt_flags = spack.build_environment.optimization_flags(compiler, target)
    assert opt_flags == expected_flags


@pytest.mark.parametrize(
    "compiler_str,real_version,target_str,expected_flags",
    [
        ("gcc@=9.2.0", None, "haswell", "-march=haswell -mtune=haswell"),
        # Check that custom string versions are accepted
        ("gcc@=10foo", "9.2.0", "icelake", "-march=icelake-client -mtune=icelake-client"),
        # Check that we run version detection (4.4.0 doesn't support icelake)
        ("gcc@=4.4.0-special", "9.2.0", "icelake", "-march=icelake-client -mtune=icelake-client"),
        # Check that the special case for Apple's clang is treated correctly
        # i.e. it won't try to detect the version again
        ("apple-clang@=9.1.0", None, "x86_64", "-march=x86-64"),
    ],
)
def test_optimization_flags_with_custom_versions(
    compiler_str,
    real_version,
    target_str,
    expected_flags,
    monkeypatch,
    mutable_config,
    compiler_factory,
):
    target = archspec.cpu.TARGETS[target_str]
    compiler_dict = compiler_factory(spec=compiler_str, operating_system="redhat6")
    mutable_config.set("compilers", [compiler_dict])
    if real_version:
        monkeypatch.setattr(spack.compiler.Compiler, "get_real_version", lambda x: real_version)
    compiler = spack.compilers.compiler_from_dict(compiler_dict["compiler"])

    opt_flags = spack.build_environment.optimization_flags(compiler, target)
    assert opt_flags == expected_flags
