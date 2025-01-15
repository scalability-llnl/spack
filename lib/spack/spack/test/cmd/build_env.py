# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import pickle
import subprocess
import sys

import pytest

import spack.error
from spack.cmd.common.env_utility import run_command_in_subshell
from spack.context import Context
from spack.main import SpackCommand
from spack.spec import Spec

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
        with open(_out_file, encoding="utf-8") as f:
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


# TODO params [i, b, c] require a spec that has proceeded with a directory
# TODO praram [e] requires an active env
@pytest.mark.parametrize("cd_key", ["r", "spack-root"])
@pytest.mark.usefixtures("config", "mock_packages", "working_env")
def test_cd(cd_key, tmpdir, monkeypatch, capfd):
    """test that a subshell will navigate using spack cd before running commands"""
    cmd = "pwd" if sys.platform != "win32" else 'powershell.exe -Command "& {(Get-Location).Path}"'

    def mock_execvp(_, args):
        """os.execvp will kill take over the pytest process when it is successful"""
        result = subprocess.check_output(args, universal_newlines=True)
        print(result)

    with tmpdir.as_cwd():
        monkeypatch.setattr(os, "execvp", mock_execvp)

        pwd = os.getcwd()
        spec = Spec("zlib").concretized()
        run_command_in_subshell(spec, Context.BUILD, [cmd], cd_arg=cd_key)

        output = capfd.readouterr()
        assert pwd not in output.out
        assert output.err == ""


def test_failure_when_uninstalled_deps(config, mock_packages):
    with pytest.raises(
        spack.error.SpackError, match="Not all dependencies of dttop are installed"
    ):
        build_env("dttop")
