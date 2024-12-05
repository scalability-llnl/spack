# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pickle
import sys

import pytest

import spack.error
from spack.main import SpackCommand

build_env = SpackCommand("build-env")


@pytest.mark.parametrize("pkg", [("zlib",), ("zlib", "--")])
@pytest.mark.usefixtures("config", "mock_packages", "working_env")
def test_it_just_runs(pkg):
    build_env(*pkg)


@pytest.mark.usefixtures("config", "mock_packages", "working_env")
def test_error_when_multiple_specs_are_given():
    output = build_env("libelf libdwarf", fail_on_error=False)
    assert "only takes one spec" in output


@pytest.mark.parametrize("args", [("--", "/bin/sh", "-c", "echo test"), ("--",), ()])
@pytest.mark.usefixtures("config", "mock_packages", "working_env")
def test_build_env_requires_a_spec(args):
    output = build_env(*args, fail_on_error=False)
    assert "requires a spec" in output


_out_file = "env.out"


@pytest.mark.parametrize("shell", ["pwsh", "bat"] if sys.platform == "win32" else ["sh"])
@pytest.mark.usefixtures("config", "mock_packages", "working_env")
def test_dump(shell_as, shell, tmpdir):
    with tmpdir.as_cwd():
        build_env("--dump", _out_file, "zlib")
        with open(_out_file) as f:
            if shell == "pwsh":
                assert any(line.startswith("$Env:PATH") for line in f.readlines())
            elif shell == "bat":
                assert any(line.startswith('set "PATH=') for line in f.readlines())
            else:
                assert any(line.startswith("PATH=") for line in f.readlines())


@pytest.mark.usefixtures("config", "mock_packages", "working_env")
def test_pickle(tmpdir):
    with tmpdir.as_cwd():
        build_env("--pickle", _out_file, "zlib")
        environment = pickle.load(open(_out_file, "rb"))
        assert isinstance(environment, dict)
        assert "PATH" in environment


def test_failure_when_uninstalled_deps(config, mock_packages):
    with pytest.raises(
        spack.error.SpackError, match="Not all dependencies of dttop are installed"
    ):
        build_env("dttop")
