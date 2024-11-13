# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Test basic behavior of compilers in Spack"""
import os
from copy import copy

import pytest

import llnl.util.filesystem as fs

import spack.compiler
import spack.compilers
import spack.config
import spack.spec
import spack.util.module_cmd
from spack.compiler import Compiler
from spack.util.executable import Executable, ProcessError


def test_multiple_conflicting_compiler_definitions(mutable_config):
    compiler_def = {
        "compiler": {
            "flags": {},
            "modules": [],
            "paths": {"cc": "cc", "cxx": "cxx", "f77": "null", "fc": "null"},
            "extra_rpaths": [],
            "operating_system": "test",
            "target": "test",
            "environment": {},
            "spec": "clang@0.0.0",
        }
    }

    compiler_config = [compiler_def, compiler_def]
    compiler_config[0]["compiler"]["paths"]["f77"] = "f77"
    mutable_config.update_config("compilers", compiler_config)

    arch_spec = spack.spec.ArchSpec(("test", "test", "test"))
    cmp = spack.compilers.compiler_for_spec("clang@=0.0.0", arch_spec)
    assert cmp.f77 == "f77"


def test_compiler_flags_from_config_are_grouped():
    compiler_entry = {
        "spec": "intel@17.0.2",
        "operating_system": "foo-os",
        "paths": {"cc": "cc-path", "cxx": "cxx-path", "fc": None, "f77": None},
        "flags": {"cflags": "-O0 -foo-flag foo-val"},
        "modules": None,
    }

    compiler = spack.compilers.compiler_from_dict(compiler_entry)
    assert any(x == "-foo-flag foo-val" for x in compiler.flags["cflags"])


# Test behavior of flags and UnsupportedCompilerFlag.

# Utility function to test most flags.
default_compiler_entry = {
    "spec": "apple-clang@2.0.0",
    "operating_system": "foo-os",
    "paths": {"cc": "cc-path", "cxx": "cxx-path", "fc": "fc-path", "f77": "f77-path"},
    "flags": {},
    "modules": None,
}


# Fake up a mock compiler where everything is defaulted.
class MockCompiler(Compiler):
    def __init__(self):
        super().__init__(
            cspec="badcompiler@1.0.0",
            operating_system=default_compiler_entry["operating_system"],
            target=None,
            paths=[
                default_compiler_entry["paths"]["cc"],
                default_compiler_entry["paths"]["cxx"],
                default_compiler_entry["paths"]["fc"],
                default_compiler_entry["paths"]["f77"],
            ],
            environment={},
        )

    @property
    def name(self):
        return "mockcompiler"

    @property
    def version(self):
        return "1.0.0"

    _verbose_flag = "--verbose"

    @property
    def verbose_flag(self):
        return self._verbose_flag

    required_libs = ["libgfortran"]


@pytest.mark.not_on_windows("Not supported on Windows (yet)")
def test_implicit_rpaths(dirs_with_libfiles):
    lib_to_dirs, all_dirs = dirs_with_libfiles
    compiler = MockCompiler()
    compiler._compile_c_source_output = "ld " + " ".join(f"-L{d}" for d in all_dirs)
    retrieved_rpaths = compiler.implicit_rpaths()
    assert set(retrieved_rpaths) == set(lib_to_dirs["libstdc++"] + lib_to_dirs["libgfortran"])


without_flag_output = "ld -L/path/to/first/lib -L/path/to/second/lib64"
with_flag_output = "ld -L/path/to/first/with/flag/lib -L/path/to/second/lib64"


def call_compiler(exe, *args, **kwargs):
    # This method can replace Executable.__call__ to emulate a compiler that
    # changes libraries depending on a flag.
    if "--correct-flag" in exe.exe:
        return with_flag_output
    return without_flag_output


@pytest.mark.not_on_windows("Not supported on Windows (yet)")
@pytest.mark.parametrize(
    "exe,flagname",
    [
        ("cxx", "cxxflags"),
        ("cxx", "cppflags"),
        ("cxx", "ldflags"),
        ("cc", "cflags"),
        ("cc", "cppflags"),
    ],
)
@pytest.mark.enable_compiler_execution
def test_compile_dummy_c_source_adds_flags(monkeypatch, exe, flagname):
    # create fake compiler that emits mock verbose output
    compiler = MockCompiler()
    monkeypatch.setattr(Executable, "__call__", call_compiler)

    if exe == "cxx":
        compiler.cc = None
        compiler.fc = None
        compiler.f77 = None
    elif exe == "cc":
        compiler.cxx = None
        compiler.fc = None
        compiler.f77 = None
    else:
        assert False

    # Test without flags
    assert compiler._compile_dummy_c_source() == without_flag_output

    if flagname:
        # set flags and test
        compiler.flags = {flagname: ["--correct-flag"]}
        assert compiler._compile_dummy_c_source() == with_flag_output


@pytest.mark.enable_compiler_execution
def test_compile_dummy_c_source_no_path():
    compiler = MockCompiler()
    compiler.cc = None
    compiler.cxx = None
    assert compiler._compile_dummy_c_source() is None


@pytest.mark.enable_compiler_execution
def test_compile_dummy_c_source_no_verbose_flag():
    compiler = MockCompiler()
    compiler._verbose_flag = None
    assert compiler._compile_dummy_c_source() is None


@pytest.mark.not_on_windows("Not supported on Windows (yet)")
@pytest.mark.enable_compiler_execution
def test_compile_dummy_c_source_load_env(working_env, monkeypatch, tmpdir):
    gcc = str(tmpdir.join("gcc"))
    with open(gcc, "w") as f:
        f.write(
            f"""#!/bin/sh
if [ "$ENV_SET" = "1" ] && [ "$MODULE_LOADED" = "1" ]; then
  printf '{without_flag_output}'
fi
"""
        )
    fs.set_executable(gcc)

    # Set module load to turn compiler on
    def module(*args):
        if args[0] == "show":
            return ""
        elif args[0] == "load":
            os.environ["MODULE_LOADED"] = "1"

    monkeypatch.setattr(spack.util.module_cmd, "module", module)

    compiler = MockCompiler()
    compiler.cc = gcc
    compiler.environment = {"set": {"ENV_SET": "1"}}
    compiler.modules = ["turn_on"]

    assert compiler._compile_dummy_c_source() == without_flag_output


# Get the desired flag from the specified compiler spec.
def flag_value(flag, spec):
    compiler = None
    if spec is None:
        compiler = MockCompiler()
    else:
        compiler_entry = copy(default_compiler_entry)
        compiler_entry["spec"] = spec
        compiler = spack.compilers.compiler_from_dict(compiler_entry)

    return getattr(compiler, flag)


# Utility function to verify that the expected exception is thrown for
# an unsupported flag.
def unsupported_flag_test(flag, spec=None):
    caught_exception = None
    try:
        flag_value(flag, spec)
    except spack.compiler.UnsupportedCompilerFlag:
        caught_exception = True

    assert caught_exception and "Expected exception not thrown."


# Verify the expected flag value for the give compiler spec.
def supported_flag_test(flag, flag_value_ref, spec=None):
    assert flag_value(flag, spec) == flag_value_ref


# Tests for UnsupportedCompilerFlag exceptions from default
# implementations of flags.
def test_default_flags():
    supported_flag_test("cc_rpath_arg", "-Wl,-rpath,")
    supported_flag_test("cxx_rpath_arg", "-Wl,-rpath,")
    supported_flag_test("f77_rpath_arg", "-Wl,-rpath,")
    supported_flag_test("fc_rpath_arg", "-Wl,-rpath,")
    supported_flag_test("linker_arg", "-Wl,")
    unsupported_flag_test("openmp_flag")
    unsupported_flag_test("cxx11_flag")
    unsupported_flag_test("cxx14_flag")
    unsupported_flag_test("cxx17_flag")
    supported_flag_test("cxx98_flag", "")
    unsupported_flag_test("c99_flag")
    unsupported_flag_test("c11_flag")
    supported_flag_test("cc_pic_flag", "-fPIC")
    supported_flag_test("cxx_pic_flag", "-fPIC")
    supported_flag_test("f77_pic_flag", "-fPIC")
    supported_flag_test("fc_pic_flag", "-fPIC")
    supported_flag_test("debug_flags", ["-g"])
    supported_flag_test("opt_flags", ["-O", "-O0", "-O1", "-O2", "-O3"])


# Verify behavior of particular compiler definitions.
def test_arm_flags():
    supported_flag_test("openmp_flag", "-fopenmp", "arm@1.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "arm@1.0")
    supported_flag_test("cxx14_flag", "-std=c++14", "arm@1.0")
    supported_flag_test("cxx17_flag", "-std=c++1z", "arm@1.0")
    supported_flag_test("c99_flag", "-std=c99", "arm@1.0")
    supported_flag_test("c11_flag", "-std=c11", "arm@1.0")
    supported_flag_test("cc_pic_flag", "-fPIC", "arm@1.0")
    supported_flag_test("cxx_pic_flag", "-fPIC", "arm@1.0")
    supported_flag_test("f77_pic_flag", "-fPIC", "arm@1.0")
    supported_flag_test("fc_pic_flag", "-fPIC", "arm@1.0")
    supported_flag_test("opt_flags", ["-O", "-O0", "-O1", "-O2", "-O3", "-Ofast"], "arm@1.0")


def test_cce_flags():
    supported_flag_test("version_argument", "--version", "cce@9.0.1")
    supported_flag_test("version_argument", "-V", "cce@9.0.1-classic")
    supported_flag_test("openmp_flag", "-fopenmp", "cce@9.0.1")
    supported_flag_test("openmp_flag", "-h omp", "cce@9.0.1-classic")
    supported_flag_test("openmp_flag", "-h omp", "cce@1.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "cce@9.0.1")
    supported_flag_test("cxx11_flag", "-h std=c++11", "cce@9.0.1-classic")
    supported_flag_test("cxx11_flag", "-h std=c++11", "cce@1.0")
    unsupported_flag_test("c99_flag", "cce@8.0")
    supported_flag_test("c99_flag", "-std=c99", "cce@9.0.1")
    supported_flag_test("c99_flag", "-h c99,noconform,gnu", "cce@8.1")
    supported_flag_test("c99_flag", "-h std=c99,noconform,gnu", "cce@8.4")
    unsupported_flag_test("c11_flag", "cce@8.4")
    supported_flag_test("c11_flag", "-std=c11", "cce@9.0.1")
    supported_flag_test("c11_flag", "-h std=c11,noconform,gnu", "cce@8.5")
    supported_flag_test("cc_pic_flag", "-h PIC", "cce@1.0")
    supported_flag_test("cxx_pic_flag", "-h PIC", "cce@1.0")
    supported_flag_test("f77_pic_flag", "-h PIC", "cce@1.0")
    supported_flag_test("fc_pic_flag", "-h PIC", "cce@1.0")
    supported_flag_test("cc_pic_flag", "-fPIC", "cce@9.1.0")
    supported_flag_test("cxx_pic_flag", "-fPIC", "cce@9.1.0")
    supported_flag_test("f77_pic_flag", "-fPIC", "cce@9.1.0")
    supported_flag_test("fc_pic_flag", "-fPIC", "cce@9.1.0")
    supported_flag_test("stdcxx_libs", (), "cce@1.0")
    supported_flag_test("debug_flags", ["-g", "-G0", "-G1", "-G2", "-Gfast"], "cce@1.0")


def test_apple_clang_flags():
    supported_flag_test("openmp_flag", "-Xpreprocessor -fopenmp", "apple-clang@2.0.0")
    unsupported_flag_test("cxx11_flag", "apple-clang@2.0.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "apple-clang@4.0.0")
    unsupported_flag_test("cxx14_flag", "apple-clang@5.0.0")
    supported_flag_test("cxx14_flag", "-std=c++1y", "apple-clang@5.1.0")
    supported_flag_test("cxx14_flag", "-std=c++14", "apple-clang@6.1.0")
    unsupported_flag_test("cxx17_flag", "apple-clang@6.0.0")
    supported_flag_test("cxx17_flag", "-std=c++1z", "apple-clang@6.1.0")
    supported_flag_test("c99_flag", "-std=c99", "apple-clang@6.1.0")
    unsupported_flag_test("c11_flag", "apple-clang@3.0.0")
    supported_flag_test("c11_flag", "-std=c11", "apple-clang@6.1.0")
    supported_flag_test("cc_pic_flag", "-fPIC", "apple-clang@2.0.0")
    supported_flag_test("cxx_pic_flag", "-fPIC", "apple-clang@2.0.0")
    supported_flag_test("f77_pic_flag", "-fPIC", "apple-clang@2.0.0")
    supported_flag_test("fc_pic_flag", "-fPIC", "apple-clang@2.0.0")


def test_clang_flags():
    supported_flag_test("version_argument", "--version", "clang@foo.bar")
    supported_flag_test("openmp_flag", "-fopenmp", "clang@3.3")
    unsupported_flag_test("cxx11_flag", "clang@3.2")
    supported_flag_test("cxx11_flag", "-std=c++11", "clang@3.3")
    unsupported_flag_test("cxx14_flag", "clang@3.3")
    supported_flag_test("cxx14_flag", "-std=c++1y", "clang@3.4")
    supported_flag_test("cxx14_flag", "-std=c++14", "clang@3.5")
    unsupported_flag_test("cxx17_flag", "clang@3.4")
    supported_flag_test("cxx17_flag", "-std=c++1z", "clang@3.5")
    supported_flag_test("cxx17_flag", "-std=c++17", "clang@5.0")
    unsupported_flag_test("cxx20_flag", "clang@4.0")
    supported_flag_test("cxx20_flag", "-std=c++2a", "clang@5.0")
    supported_flag_test("cxx20_flag", "-std=c++20", "clang@11.0")
    unsupported_flag_test("cxx23_flag", "clang@11.0")
    supported_flag_test("cxx23_flag", "-std=c++2b", "clang@12.0")
    supported_flag_test("cxx23_flag", "-std=c++23", "clang@17.0")
    supported_flag_test("c99_flag", "-std=c99", "clang@3.3")
    unsupported_flag_test("c11_flag", "clang@2.0")
    supported_flag_test("c11_flag", "-std=c11", "clang@6.1.0")
    unsupported_flag_test("c23_flag", "clang@8.0")
    supported_flag_test("c23_flag", "-std=c2x", "clang@9.0")
    supported_flag_test("c23_flag", "-std=c23", "clang@18.0")
    supported_flag_test("cc_pic_flag", "-fPIC", "clang@3.3")
    supported_flag_test("cxx_pic_flag", "-fPIC", "clang@3.3")
    supported_flag_test("f77_pic_flag", "-fPIC", "clang@3.3")
    supported_flag_test("fc_pic_flag", "-fPIC", "clang@3.3")
    supported_flag_test(
        "debug_flags",
        [
            "-gcodeview",
            "-gdwarf-2",
            "-gdwarf-3",
            "-gdwarf-4",
            "-gdwarf-5",
            "-gline-tables-only",
            "-gmodules",
            "-g",
        ],
        "clang@3.3",
    )
    supported_flag_test(
        "opt_flags",
        ["-O0", "-O1", "-O2", "-O3", "-Ofast", "-Os", "-Oz", "-Og", "-O", "-O4"],
        "clang@3.3",
    )


def test_aocc_flags():
    supported_flag_test(
        "debug_flags",
        [
            "-gcodeview",
            "-gdwarf-2",
            "-gdwarf-3",
            "-gdwarf-4",
            "-gdwarf-5",
            "-gline-tables-only",
            "-gmodules",
            "-g",
        ],
        "aocc@2.2.0",
    )
    supported_flag_test(
        "opt_flags",
        ["-O0", "-O1", "-O2", "-O3", "-Ofast", "-Os", "-Oz", "-Og", "-O", "-O4"],
        "aocc@2.2.0",
    )

    supported_flag_test("stdcxx_libs", ("-lstdc++",), "aocc@2.2.0")
    supported_flag_test("openmp_flag", "-fopenmp", "aocc@2.2.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "aocc@2.2.0")
    supported_flag_test("cxx14_flag", "-std=c++14", "aocc@2.2.0")
    supported_flag_test("cxx17_flag", "-std=c++17", "aocc@2.2.0")
    supported_flag_test("c99_flag", "-std=c99", "aocc@2.2.0")
    supported_flag_test("c11_flag", "-std=c11", "aocc@2.2.0")
    supported_flag_test("cc_pic_flag", "-fPIC", "aocc@2.2.0")
    supported_flag_test("cxx_pic_flag", "-fPIC", "aocc@2.2.0")
    supported_flag_test("f77_pic_flag", "-fPIC", "aocc@2.2.0")
    supported_flag_test("fc_pic_flag", "-fPIC", "aocc@2.2.0")
    supported_flag_test("version_argument", "--version", "aocc@2.2.0")
    flg = "-Wno-unused-command-line-argument -mllvm -eliminate-similar-expr=false"
    supported_flag_test("cflags", flg, "aocc@3.0.0")
    supported_flag_test("cxxflags", flg, "aocc@3.0.0")
    supported_flag_test("fflags", flg, "aocc@3.0.0")


def test_fj_flags():
    supported_flag_test("openmp_flag", "-Kopenmp", "fj@4.0.0")
    supported_flag_test("cxx98_flag", "-std=c++98", "fj@4.0.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "fj@4.0.0")
    supported_flag_test("cxx14_flag", "-std=c++14", "fj@4.0.0")
    supported_flag_test("cxx17_flag", "-std=c++17", "fj@4.0.0")
    supported_flag_test("c99_flag", "-std=c99", "fj@4.0.0")
    supported_flag_test("c11_flag", "-std=c11", "fj@4.0.0")
    supported_flag_test("cc_pic_flag", "-KPIC", "fj@4.0.0")
    supported_flag_test("cxx_pic_flag", "-KPIC", "fj@4.0.0")
    supported_flag_test("f77_pic_flag", "-KPIC", "fj@4.0.0")
    supported_flag_test("fc_pic_flag", "-KPIC", "fj@4.0.0")
    supported_flag_test("opt_flags", ["-O0", "-O1", "-O2", "-O3", "-Ofast"], "fj@4.0.0")
    supported_flag_test("debug_flags", "-g", "fj@4.0.0")


def test_gcc_flags():
    supported_flag_test("openmp_flag", "-fopenmp", "gcc@4.1")
    supported_flag_test("cxx98_flag", "", "gcc@5.2")
    supported_flag_test("cxx98_flag", "-std=c++98", "gcc@6.0")
    unsupported_flag_test("cxx11_flag", "gcc@4.2")
    supported_flag_test("cxx11_flag", "-std=c++0x", "gcc@4.3")
    supported_flag_test("cxx11_flag", "-std=c++11", "gcc@4.7")
    unsupported_flag_test("cxx14_flag", "gcc@4.7")
    supported_flag_test("cxx14_flag", "-std=c++1y", "gcc@4.8")
    supported_flag_test("cxx14_flag", "-std=c++14", "gcc@4.9")
    supported_flag_test("cxx14_flag", "-std=c++14", "gcc@6.0")
    unsupported_flag_test("cxx17_flag", "gcc@4.9")
    supported_flag_test("cxx17_flag", "-std=c++1z", "gcc@5.0")
    supported_flag_test("cxx17_flag", "-std=c++17", "gcc@6.0")
    unsupported_flag_test("c99_flag", "gcc@4.4")
    supported_flag_test("c99_flag", "-std=c99", "gcc@4.5")
    unsupported_flag_test("c11_flag", "gcc@4.6")
    supported_flag_test("c11_flag", "-std=c11", "gcc@4.7")
    supported_flag_test("cc_pic_flag", "-fPIC", "gcc@4.0")
    supported_flag_test("cxx_pic_flag", "-fPIC", "gcc@4.0")
    supported_flag_test("f77_pic_flag", "-fPIC", "gcc@4.0")
    supported_flag_test("fc_pic_flag", "-fPIC", "gcc@4.0")
    supported_flag_test("stdcxx_libs", ("-lstdc++",), "gcc@4.1")
    supported_flag_test(
        "debug_flags", ["-g", "-gstabs+", "-gstabs", "-gxcoff+", "-gxcoff", "-gvms"], "gcc@4.0"
    )
    supported_flag_test(
        "opt_flags", ["-O", "-O0", "-O1", "-O2", "-O3", "-Os", "-Ofast", "-Og"], "gcc@4.0"
    )


def test_intel_flags():
    supported_flag_test("openmp_flag", "-openmp", "intel@=15.0")
    supported_flag_test("openmp_flag", "-qopenmp", "intel@=16.0")
    unsupported_flag_test("cxx11_flag", "intel@=11.0")
    supported_flag_test("cxx11_flag", "-std=c++0x", "intel@=12.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "intel@=13")
    unsupported_flag_test("cxx14_flag", "intel@=14.0")
    supported_flag_test("cxx14_flag", "-std=c++1y", "intel@=15.0")
    supported_flag_test("cxx14_flag", "-std=c++14", "intel@=15.0.2")
    unsupported_flag_test("cxx17_flag", "intel@=18")
    supported_flag_test("cxx17_flag", "-std=c++17", "intel@=19.0")
    unsupported_flag_test("c99_flag", "intel@=11.0")
    supported_flag_test("c99_flag", "-std=c99", "intel@=12.0")
    unsupported_flag_test("c11_flag", "intel@=15.0")
    supported_flag_test("c18_flag", "-std=c18", "intel@=21.5.0")
    unsupported_flag_test("c18_flag", "intel@=21.4.0")
    supported_flag_test("c11_flag", "-std=c1x", "intel@=16.0")
    supported_flag_test("cc_pic_flag", "-fPIC", "intel@=1.0")
    supported_flag_test("cxx_pic_flag", "-fPIC", "intel@=1.0")
    supported_flag_test("f77_pic_flag", "-fPIC", "intel@=1.0")
    supported_flag_test("fc_pic_flag", "-fPIC", "intel@=1.0")
    supported_flag_test("stdcxx_libs", ("-cxxlib",), "intel@=1.0")
    supported_flag_test("debug_flags", ["-debug", "-g", "-g0", "-g1", "-g2", "-g3"], "intel@=1.0")
    supported_flag_test(
        "opt_flags", ["-O", "-O0", "-O1", "-O2", "-O3", "-Ofast", "-Os"], "intel@=1.0"
    )


def test_oneapi_flags():
    supported_flag_test("openmp_flag", "-fiopenmp", "oneapi@=2020.8.0.0827")
    supported_flag_test("cxx11_flag", "-std=c++11", "oneapi@=2020.8.0.0827")
    supported_flag_test("cxx14_flag", "-std=c++14", "oneapi@=2020.8.0.0827")
    supported_flag_test("c99_flag", "-std=c99", "oneapi@=2020.8.0.0827")
    supported_flag_test("c11_flag", "-std=c1x", "oneapi@=2020.8.0.0827")
    supported_flag_test("cc_pic_flag", "-fPIC", "oneapi@=2020.8.0.0827")
    supported_flag_test("cxx_pic_flag", "-fPIC", "oneapi@=2020.8.0.0827")
    supported_flag_test("f77_pic_flag", "-fPIC", "oneapi@=2020.8.0.0827")
    supported_flag_test("fc_pic_flag", "-fPIC", "oneapi@=2020.8.0.0827")
    supported_flag_test("stdcxx_libs", ("-cxxlib",), "oneapi@=2020.8.0.0827")
    supported_flag_test(
        "debug_flags", ["-debug", "-g", "-g0", "-g1", "-g2", "-g3"], "oneapi@=2020.8.0.0827"
    )
    supported_flag_test(
        "opt_flags", ["-O", "-O0", "-O1", "-O2", "-O3", "-Ofast", "-Os"], "oneapi@=2020.8.0.0827"
    )


def test_nag_flags():
    supported_flag_test("openmp_flag", "-openmp", "nag@=1.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "nag@=1.0")
    supported_flag_test("cc_pic_flag", "-fPIC", "nag@=1.0")
    supported_flag_test("cxx_pic_flag", "-fPIC", "nag@=1.0")
    supported_flag_test("f77_pic_flag", "-PIC", "nag@=1.0")
    supported_flag_test("fc_pic_flag", "-PIC", "nag@=1.0")
    supported_flag_test("cc_rpath_arg", "-Wl,-rpath,", "nag@=1.0")
    supported_flag_test("cxx_rpath_arg", "-Wl,-rpath,", "nag@=1.0")
    supported_flag_test("f77_rpath_arg", "-Wl,-Wl,,-rpath,,", "nag@=1.0")
    supported_flag_test("fc_rpath_arg", "-Wl,-Wl,,-rpath,,", "nag@=1.0")
    supported_flag_test("linker_arg", "-Wl,-Wl,,", "nag@=1.0")
    supported_flag_test("debug_flags", ["-g", "-gline", "-g90"], "nag@=1.0")
    supported_flag_test("opt_flags", ["-O", "-O0", "-O1", "-O2", "-O3", "-O4"], "nag@=1.0")


def test_nvhpc_flags():
    supported_flag_test("openmp_flag", "-mp", "nvhpc@=20.9")
    supported_flag_test("cxx11_flag", "--c++11", "nvhpc@=20.9")
    supported_flag_test("cxx14_flag", "--c++14", "nvhpc@=20.9")
    supported_flag_test("cxx17_flag", "--c++17", "nvhpc@=20.9")
    supported_flag_test("c99_flag", "-c99", "nvhpc@=20.9")
    supported_flag_test("c11_flag", "-c11", "nvhpc@=20.9")
    supported_flag_test("cc_pic_flag", "-fpic", "nvhpc@=20.9")
    supported_flag_test("cxx_pic_flag", "-fpic", "nvhpc@=20.9")
    supported_flag_test("f77_pic_flag", "-fpic", "nvhpc@=20.9")
    supported_flag_test("fc_pic_flag", "-fpic", "nvhpc@=20.9")
    supported_flag_test("debug_flags", ["-g", "-gopt"], "nvhpc@=20.9")
    supported_flag_test("opt_flags", ["-O", "-O0", "-O1", "-O2", "-O3", "-O4"], "nvhpc@=20.9")
    supported_flag_test("stdcxx_libs", ("-c++libs",), "nvhpc@=20.9")


def test_pgi_flags():
    supported_flag_test("openmp_flag", "-mp", "pgi@=1.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "pgi@=1.0")
    unsupported_flag_test("c99_flag", "pgi@=12.9")
    supported_flag_test("c99_flag", "-c99", "pgi@=12.10")
    unsupported_flag_test("c11_flag", "pgi@=15.2")
    supported_flag_test("c11_flag", "-c11", "pgi@=15.3")
    supported_flag_test("cc_pic_flag", "-fpic", "pgi@=1.0")
    supported_flag_test("cxx_pic_flag", "-fpic", "pgi@=1.0")
    supported_flag_test("f77_pic_flag", "-fpic", "pgi@=1.0")
    supported_flag_test("fc_pic_flag", "-fpic", "pgi@=1.0")
    supported_flag_test("stdcxx_libs", ("-pgc++libs",), "pgi@=1.0")
    supported_flag_test("debug_flags", ["-g", "-gopt"], "pgi@=1.0")
    supported_flag_test("opt_flags", ["-O", "-O0", "-O1", "-O2", "-O3", "-O4"], "pgi@=1.0")


def test_xl_flags():
    supported_flag_test("openmp_flag", "-qsmp=omp", "xl@=1.0")
    unsupported_flag_test("cxx11_flag", "xl@=13.0")
    supported_flag_test("cxx11_flag", "-qlanglvl=extended0x", "xl@=13.1")
    unsupported_flag_test("c99_flag", "xl@=10.0")
    supported_flag_test("c99_flag", "-qlanglvl=extc99", "xl@=10.1")
    supported_flag_test("c99_flag", "-std=gnu99", "xl@=13.1.1")
    unsupported_flag_test("c11_flag", "xl@=12.0")
    supported_flag_test("c11_flag", "-qlanglvl=extc1x", "xl@=12.1")
    supported_flag_test("c11_flag", "-std=gnu11", "xl@=13.1.2")
    supported_flag_test("cc_pic_flag", "-qpic", "xl@=1.0")
    supported_flag_test("cxx_pic_flag", "-qpic", "xl@=1.0")
    supported_flag_test("f77_pic_flag", "-qpic", "xl@=1.0")
    supported_flag_test("fc_pic_flag", "-qpic", "xl@=1.0")
    supported_flag_test("fflags", "-qzerosize", "xl@=1.0")
    supported_flag_test("debug_flags", ["-g", "-g0", "-g1", "-g2", "-g8", "-g9"], "xl@=1.0")
    supported_flag_test(
        "opt_flags", ["-O", "-O0", "-O1", "-O2", "-O3", "-O4", "-O5", "-Ofast"], "xl@=1.0"
    )


def test_xl_r_flags():
    supported_flag_test("openmp_flag", "-qsmp=omp", "xl_r@=1.0")
    unsupported_flag_test("cxx11_flag", "xl_r@=13.0")
    supported_flag_test("cxx11_flag", "-qlanglvl=extended0x", "xl_r@=13.1")
    unsupported_flag_test("c99_flag", "xl_r@=10.0")
    supported_flag_test("c99_flag", "-qlanglvl=extc99", "xl_r@=10.1")
    supported_flag_test("c99_flag", "-std=gnu99", "xl_r@=13.1.1")
    unsupported_flag_test("c11_flag", "xl_r@=12.0")
    supported_flag_test("c11_flag", "-qlanglvl=extc1x", "xl_r@=12.1")
    supported_flag_test("c11_flag", "-std=gnu11", "xl_r@=13.1.2")
    supported_flag_test("cc_pic_flag", "-qpic", "xl_r@=1.0")
    supported_flag_test("cxx_pic_flag", "-qpic", "xl_r@=1.0")
    supported_flag_test("f77_pic_flag", "-qpic", "xl_r@=1.0")
    supported_flag_test("fc_pic_flag", "-qpic", "xl_r@=1.0")
    supported_flag_test("fflags", "-qzerosize", "xl_r@=1.0")
    supported_flag_test("debug_flags", ["-g", "-g0", "-g1", "-g2", "-g8", "-g9"], "xl@=1.0")
    supported_flag_test(
        "opt_flags", ["-O", "-O0", "-O1", "-O2", "-O3", "-O4", "-O5", "-Ofast"], "xl@=1.0"
    )


@pytest.mark.parametrize(
    "compiler_spec,expected_result",
    [("gcc@4.7.2", False), ("clang@3.3", False), ("clang@8.0.0", True)],
)
@pytest.mark.not_on_windows("GCC and LLVM currently not supported on the platform")
def test_detecting_mixed_toolchains(
    compiler_spec, expected_result, mutable_config, compiler_factory
):
    mixed_c = compiler_factory(spec="clang@8.0.0", operating_system="debian6")
    mixed_c["compiler"]["paths"] = {
        "cc": "/path/to/clang-8",
        "cxx": "/path/to/clang++-8",
        "f77": "/path/to/gfortran-9",
        "fc": "/path/to/gfortran-9",
    }
    mutable_config.set(
        "compilers",
        [
            compiler_factory(spec="gcc@4.7.2", operating_system="debian6"),
            compiler_factory(spec="clang@3.3", operating_system="debian6"),
            mixed_c,
        ],
    )

    compiler = spack.compilers.compilers_for_spec(compiler_spec).pop()
    assert spack.compilers.is_mixed_toolchain(compiler) is expected_result


@pytest.mark.regression("14798,13733")
def test_raising_if_compiler_target_is_over_specific(config):
    # Compiler entry with an overly specific target
    compilers = [
        {
            "compiler": {
                "spec": "gcc@9.0.1",
                "paths": {
                    "cc": "/usr/bin/gcc-9",
                    "cxx": "/usr/bin/g++-9",
                    "f77": "/usr/bin/gfortran-9",
                    "fc": "/usr/bin/gfortran-9",
                },
                "flags": {},
                "operating_system": "ubuntu18.04",
                "target": "haswell",
                "modules": [],
                "environment": {},
                "extra_rpaths": [],
            }
        }
    ]
    arch_spec = spack.spec.ArchSpec(("linux", "ubuntu18.04", "haswell"))
    with spack.config.override("compilers", compilers):
        cfg = spack.compilers.get_compiler_config(config)
        with pytest.raises(ValueError):
            spack.compilers.get_compilers(cfg, spack.spec.CompilerSpec("gcc@9.0.1"), arch_spec)


@pytest.mark.not_on_windows("Not supported on Windows (yet)")
def test_compiler_get_real_version(working_env, monkeypatch, tmpdir):
    # Test variables
    test_version = "2.2.2"

    # Create compiler
    gcc = str(tmpdir.join("gcc"))
    with open(gcc, "w") as f:
        f.write(
            """#!/bin/sh
if [ "$CMP_ON" = "1" ]; then
    echo "$CMP_VER"
fi
"""
        )
    fs.set_executable(gcc)

    # Add compiler to config
    compiler_info = {
        "spec": "gcc@foo",
        "paths": {"cc": gcc, "cxx": None, "f77": None, "fc": None},
        "flags": {},
        "operating_system": "fake",
        "target": "fake",
        "modules": ["turn_on"],
        "environment": {"set": {"CMP_VER": test_version}},
        "extra_rpaths": [],
    }
    compiler_dict = {"compiler": compiler_info}

    # Set module load to turn compiler on
    def module(*args):
        if args[0] == "show":
            return ""
        elif args[0] == "load":
            os.environ["CMP_ON"] = "1"

    monkeypatch.setattr(spack.util.module_cmd, "module", module)

    # Run and confirm output
    compilers = spack.compilers.get_compilers([compiler_dict])
    assert len(compilers) == 1
    compiler = compilers[0]
    version = compiler.get_real_version()
    assert version == test_version


@pytest.mark.regression("42679")
def test_get_compilers(config):
    """Tests that we can select compilers whose versions differ only for a suffix."""
    common = {
        "flags": {},
        "operating_system": "ubuntu23.10",
        "target": "x86_64",
        "modules": [],
        "environment": {},
        "extra_rpaths": [],
    }
    with_suffix = {
        "spec": "gcc@13.2.0-suffix",
        "paths": {
            "cc": "/usr/bin/gcc-13.2.0-suffix",
            "cxx": "/usr/bin/g++-13.2.0-suffix",
            "f77": "/usr/bin/gfortran-13.2.0-suffix",
            "fc": "/usr/bin/gfortran-13.2.0-suffix",
        },
        **common,
    }
    without_suffix = {
        "spec": "gcc@13.2.0",
        "paths": {
            "cc": "/usr/bin/gcc-13.2.0",
            "cxx": "/usr/bin/g++-13.2.0",
            "f77": "/usr/bin/gfortran-13.2.0",
            "fc": "/usr/bin/gfortran-13.2.0",
        },
        **common,
    }

    compilers = [{"compiler": without_suffix}, {"compiler": with_suffix}]

    assert spack.compilers.get_compilers(
        compilers, cspec=spack.spec.CompilerSpec("gcc@=13.2.0-suffix")
    ) == [spack.compilers._compiler_from_config_entry(with_suffix)]

    assert spack.compilers.get_compilers(
        compilers, cspec=spack.spec.CompilerSpec("gcc@=13.2.0")
    ) == [spack.compilers._compiler_from_config_entry(without_suffix)]


def test_compiler_get_real_version_fails(working_env, monkeypatch, tmpdir):
    # Test variables
    test_version = "2.2.2"

    # Create compiler
    gcc = str(tmpdir.join("gcc"))
    with open(gcc, "w") as f:
        f.write(
            """#!/bin/sh
if [ "$CMP_ON" = "1" ]; then
    echo "$CMP_VER"
fi
"""
        )
    fs.set_executable(gcc)

    # Add compiler to config
    compiler_info = {
        "spec": "gcc@foo",
        "paths": {"cc": gcc, "cxx": None, "f77": None, "fc": None},
        "flags": {},
        "operating_system": "fake",
        "target": "fake",
        "modules": ["turn_on"],
        "environment": {"set": {"CMP_VER": test_version}},
        "extra_rpaths": [],
    }
    compiler_dict = {"compiler": compiler_info}

    # Set module load to turn compiler on
    def module(*args):
        if args[0] == "show":
            return ""
        elif args[0] == "load":
            os.environ["SPACK_TEST_CMP_ON"] = "1"

    monkeypatch.setattr(spack.util.module_cmd, "module", module)

    # Make compiler fail when getting implicit rpaths
    def _call(*args, **kwargs):
        raise ProcessError("Failed intentionally")

    monkeypatch.setattr(Executable, "__call__", _call)

    # Run and no change to environment
    compilers = spack.compilers.get_compilers([compiler_dict])
    assert len(compilers) == 1
    compiler = compilers[0]
    try:
        _ = compiler.get_real_version()
        assert False
    except ProcessError:
        # Confirm environment does not change after failed call
        assert "SPACK_TEST_CMP_ON" not in os.environ


@pytest.mark.not_on_windows("Bash scripting unsupported on Windows (for now)")
def test_compiler_flags_use_real_version(working_env, monkeypatch, tmpdir):
    # Create compiler
    gcc = str(tmpdir.join("gcc"))
    with open(gcc, "w") as f:
        f.write(
            """#!/bin/sh
echo "4.4.4"
"""
        )  # Version for which c++11 flag is -std=c++0x
    fs.set_executable(gcc)

    # Add compiler to config
    compiler_info = {
        "spec": "gcc@foo",
        "paths": {"cc": gcc, "cxx": None, "f77": None, "fc": None},
        "flags": {},
        "operating_system": "fake",
        "target": "fake",
        "modules": ["turn_on"],
        "environment": {},
        "extra_rpaths": [],
    }
    compiler_dict = {"compiler": compiler_info}

    # Run and confirm output
    compilers = spack.compilers.get_compilers([compiler_dict])
    assert len(compilers) == 1
    compiler = compilers[0]
    flag = compiler.cxx11_flag
    assert flag == "-std=c++0x"


@pytest.mark.enable_compiler_verification
def test_compiler_executable_verification_raises(tmpdir):
    compiler = MockCompiler()
    compiler.cc = "/this/path/does/not/exist"

    with pytest.raises(spack.compiler.CompilerAccessError):
        compiler.verify_executables()


@pytest.mark.enable_compiler_verification
def test_compiler_executable_verification_success(tmpdir):
    def prepare_executable(name):
        real = str(tmpdir.join("cc").ensure())
        fs.set_executable(real)
        setattr(compiler, name, real)

    # setup mock compiler with real paths
    compiler = MockCompiler()
    for name in ("cc", "cxx", "f77", "fc"):
        prepare_executable(name)

    # testing that this doesn't raise an error because the paths exist and
    # are executable
    compiler.verify_executables()

    # Test that null entries don't fail
    compiler.cc = None
    compiler.verify_executables()


@pytest.mark.parametrize(
    "compilers_extra_attributes,expected_length",
    [
        # If we detect a C compiler we expect the result to be valid
        ({"c": "/usr/bin/clang-12", "cxx": "/usr/bin/clang-12"}, 1),
        # If we detect only a C++ compiler we expect the result to be discarded
        ({"cxx": "/usr/bin/clang-12"}, 0),
    ],
)
def test_detection_requires_c_compiler(compilers_extra_attributes, expected_length):
    """Tests that compilers automatically added to the configuration have
    at least a C compiler.
    """
    packages_yaml = {
        "llvm": {
            "externals": [
                {
                    "spec": "clang@12.0.0",
                    "prefix": "/usr",
                    "extra_attributes": {"compilers": compilers_extra_attributes},
                }
            ]
        }
    }
    result = spack.compilers.CompilerConfigFactory.from_packages_yaml(packages_yaml)
    assert len(result) == expected_length


def test_compiler_environment(working_env):
    """Test whether environment modifications from compilers are applied in compiler_environment"""
    os.environ.pop("TEST", None)
    compiler = Compiler(
        "gcc@=13.2.0",
        operating_system="ubuntu20.04",
        target="x86_64",
        paths=["/test/bin/gcc", "/test/bin/g++"],
        environment={"set": {"TEST": "yes"}},
    )
    with compiler.compiler_environment():
        assert os.environ["TEST"] == "yes"
