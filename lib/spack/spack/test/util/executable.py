# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys
from pathlib import PurePath

import pytest

import llnl.util.filesystem as fs

import spack
import spack.main
import spack.util.executable as ex
from spack.hooks.sbang import filter_shebangs_in_directory


def test_read_unicode(tmpdir, working_env):
    with tmpdir.as_cwd():
        script_name = "print_unicode.py"
        # read the unicode back in and see whether things work
        if sys.platform == "win32":
            script = ex.Executable("%s" % (sys.executable))
            script_args = [script_name]
        else:
            script = ex.Executable("./%s" % script_name)
            script_args = []

        os.environ["LD_LIBRARY_PATH"] = spack.main.spack_ld_library_path
        # make a script that prints some unicode
        with open(script_name, "w") as f:
            f.write(
                """#!{0}
print(u'\\xc3')
""".format(
                    sys.executable
                )
            )

        # make it executable
        fs.set_executable(script_name)
        filter_shebangs_in_directory(".", [script_name])

        assert "\xc3" == script(*script_args, output=str).strip()


def test_which_relative_path_with_slash(tmpdir, working_env):
    tmpdir.ensure("exe")
    path = str(tmpdir.join("exe"))

    os.environ["PATH"] = ""

    with tmpdir.as_cwd():
        no_exe = ex.which(".{0}exe".format(os.path.sep))
        assert no_exe is None
        if sys.platform == "win32":
            # These checks are for 'executable' files, Windows
            # determines this by file extension.
            path += ".exe"
            tmpdir.ensure("exe.exe")
        else:
            fs.set_executable(path)

        exe = ex.which(".{0}exe".format(os.path.sep))
        assert exe.path == path


def test_which_with_slash_ignores_path(tmpdir, working_env):
    tmpdir.ensure("exe")
    tmpdir.ensure("bin{0}exe".format(os.path.sep))

    path = str(tmpdir.join("exe"))
    wrong_path = str(tmpdir.join("bin", "exe"))
    os.environ["PATH"] = str(PurePath(wrong_path).parent)

    with tmpdir.as_cwd():
        if sys.platform == "win32":
            # For Windows, need to create files with .exe after any assert is none tests
            tmpdir.ensure("exe.exe")
            tmpdir.ensure("bin{0}exe.exe".format(os.path.sep))
            path = path + ".exe"
            wrong_path = wrong_path + ".exe"
        else:
            fs.set_executable(path)
            fs.set_executable(wrong_path)

        exe = ex.which(".{0}exe".format(os.path.sep))
        assert exe.path == path


def test_which(tmpdir, monkeypatch):
    monkeypatch.setenv("PATH", str(tmpdir))
    assert ex.which("spack-test-exe") is None

    with pytest.raises(ex.CommandNotFoundError):
        ex.which("spack-test-exe", required=True)

    path = str(tmpdir.join("spack-test-exe"))

    with tmpdir.as_cwd():
        if sys.platform == "win32":
            # For Windows, need to create files with .exe after any assert is none tests
            tmpdir.ensure("spack-test-exe.exe")
            path += ".exe"
        else:
            fs.touch("spack-test-exe")
            fs.set_executable("spack-test-exe")

        exe = ex.which("spack-test-exe")
        assert exe is not None
        assert exe.path == path
