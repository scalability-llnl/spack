# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import copy
import os

import pytest

import llnl.util.filesystem as fs

import spack.compilers.config
import spack.compilers.libraries
import spack.util.executable
import spack.util.module_cmd

without_flag_output = "ld -L/path/to/first/lib -L/path/to/second/lib64"
with_flag_output = "ld -L/path/to/first/with/flag/lib -L/path/to/second/lib64"


def call_compiler(exe, *args, **kwargs):
    # This method can replace Executable.__call__ to emulate a compiler that
    # changes libraries depending on a flag.
    if "--correct-flag" in exe.exe:
        return with_flag_output
    return without_flag_output


@pytest.fixture()
def mock_gcc(config):
    compilers = spack.compilers.config.all_compilers_from(configuration=config)
    compilers.sort(key=lambda x: (x.name == "gcc", x.version))
    # Deepcopy is used to avoid more boilerplate when changing the "extra_attributes"
    return copy.deepcopy(compilers[-1])


class TestCompilerPropertyDetector:
    @pytest.mark.parametrize(
        "language,flagname",
        [
            ("cxx", "cxxflags"),
            ("cxx", "cppflags"),
            ("cxx", "ldflags"),
            ("c", "cflags"),
            ("c", "cppflags"),
        ],
    )
    @pytest.mark.not_on_windows("Not supported on Windows")
    def test_compile_dummy_c_source(self, mock_gcc, monkeypatch, language, flagname):
        monkeypatch.setattr(spack.util.executable.Executable, "__call__", call_compiler)
        for key in list(mock_gcc.extra_attributes["compilers"]):
            if key == language:
                continue
            mock_gcc.extra_attributes["compilers"].pop(key)

        detector = spack.compilers.libraries.CompilerPropertyDetector(mock_gcc)

        # Test without flags
        assert detector._compile_dummy_c_source() == without_flag_output

        # Set flags and test
        if flagname:
            mock_gcc.extra_attributes.setdefault("flags", {})
            monkeypatch.setitem(mock_gcc.extra_attributes["flags"], flagname, "--correct-flag")
            assert detector._compile_dummy_c_source() == with_flag_output

    def test_compile_dummy_c_source_no_path(self, mock_gcc):
        mock_gcc.extra_attributes["compilers"] = {}
        detector = spack.compilers.libraries.CompilerPropertyDetector(mock_gcc)
        assert detector._compile_dummy_c_source() is None

    def test_compile_dummy_c_source_no_verbose_flags(self, mock_gcc, monkeypatch):
        monkeypatch.setattr(mock_gcc.package, "verbose_flags", "")
        detector = spack.compilers.libraries.CompilerPropertyDetector(mock_gcc)
        assert detector._compile_dummy_c_source() is None

    def test_compile_dummy_c_source_load_env(self, mock_gcc, monkeypatch, tmp_path):
        gcc = tmp_path / "gcc"
        gcc.write_text(
            f"""#!/bin/sh
        if [ "$ENV_SET" = "1" ] && [ "$MODULE_LOADED" = "1" ]; then
          printf '{without_flag_output}'
        fi
        """
        )
        fs.set_executable(str(gcc))

        # Set module load to turn compiler on
        def module(*args):
            if args[0] == "show":
                return ""
            elif args[0] == "load":
                monkeypatch.setenv("MODULE_LOADED", "1")

        monkeypatch.setattr(spack.util.module_cmd, "module", module)

        mock_gcc.extra_attributes["compilers"]["c"] = str(gcc)
        mock_gcc.extra_attributes["environment"] = {"set": {"ENV_SET": "1"}}
        mock_gcc.external_modules = ["turn_on"]

        detector = spack.compilers.libraries.CompilerPropertyDetector(mock_gcc)
        assert detector._compile_dummy_c_source() == without_flag_output

    @pytest.mark.not_on_windows("Not supported on Windows")
    def test_implicit_rpaths(self, mock_gcc, dirs_with_libfiles, monkeypatch):
        lib_to_dirs, all_dirs = dirs_with_libfiles
        monkeypatch.setattr(spack.compilers.libraries.CompilerPropertyDetector, "_CACHE", {})

        detector = spack.compilers.libraries.CompilerPropertyDetector(mock_gcc)
        detector._CACHE[mock_gcc.dag_hash()] = "ld " + " ".join(f"-L{d}" for d in all_dirs)

        retrieved_rpaths = detector.implicit_rpaths()
        assert set(retrieved_rpaths) == set(lib_to_dirs["libstdc++"] + lib_to_dirs["libgfortran"])

    def test_compiler_environment(self, working_env, mock_gcc, monkeypatch):
        """Test whether environment modifications are applied in compiler_environment"""
        monkeypatch.delenv("TEST", raising=False)
        mock_gcc.extra_attributes["environment"] = {"set": {"TEST": "yes"}}
        detector = spack.compilers.libraries.CompilerPropertyDetector(mock_gcc)
        with detector.compiler_environment():
            assert os.environ["TEST"] == "yes"
