# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import spack
import spack.util.module_cmd
from spack.util.module_cmd import (
    get_path_args_from_module_line,
    get_path_from_module_contents,
    module,
    path_from_modules,
)

pytestmark = pytest.mark.not_on_windows("Tests fail on Windows")

test_module_lines = [
    "prepend-path LD_LIBRARY_PATH /path/to/lib",
    "setenv MOD_DIR /path/to",
    "setenv LDFLAGS -Wl,-rpath/path/to/lib",
    "setenv LDFLAGS -L/path/to/lib",
    "prepend-path PATH /path/to/bin",
]


def test_module_function_change_env(tmp_path):
    environb = {b"TEST_MODULE_ENV_VAR": b"TEST_FAIL", b"NOT_AFFECTED": b"NOT_AFFECTED"}
    src_file = tmp_path / "src_me"
    src_file.write_text("export TEST_MODULE_ENV_VAR=TEST_SUCCESS\n")
    module("load", str(src_file), module_template=f". {src_file} 2>&1", environb=environb)
    assert environb[b"TEST_MODULE_ENV_VAR"] == b"TEST_SUCCESS"
    assert environb[b"NOT_AFFECTED"] == b"NOT_AFFECTED"


def test_module_function_no_change(tmpdir):
    src_file = str(tmpdir.join("src_me"))
    with open(src_file, "w") as f:
        f.write("echo TEST_MODULE_FUNCTION_PRINT")

    old_env = os.environ.copy()
    text = module("show", src_file, module_template=". {0} 2>&1".format(src_file))

    assert text == "TEST_MODULE_FUNCTION_PRINT\n"
    assert os.environ == old_env


def test_get_path_from_module_faked(monkeypatch):
    for line in test_module_lines:

        def fake_module(*args):
            return line

        monkeypatch.setattr(spack.util.module_cmd, "module", fake_module)

        path = path_from_modules(["mod"])
        assert path == "/path/to"


def test_get_path_from_module_contents():
    # A line with "MODULEPATH" appears early on, and the test confirms that it
    # is not extracted as the package's path
    module_show_output = """
os.environ["MODULEPATH"] = "/path/to/modules1:/path/to/modules2";
----------------------------------------------------------------------------
   /root/cmake/3.9.2.lua:
----------------------------------------------------------------------------
help([[CMake Version 3.9.2
]])
whatis("Name: CMake")
whatis("Version: 3.9.2")
whatis("Category: Tools")
whatis("URL: https://cmake.org/")
prepend_path("LD_LIBRARY_PATH","/bad/path")
prepend_path("PATH","/path/to/cmake-3.9.2/bin:/other/bad/path")
prepend_path("MANPATH","/path/to/cmake/cmake-3.9.2/share/man")
prepend_path("LD_LIBRARY_PATH","/path/to/cmake-3.9.2/lib64")
"""
    module_show_lines = module_show_output.split("\n")

    # PATH and LD_LIBRARY_PATH outvote MANPATH and the other PATH and
    # LD_LIBRARY_PATH entries
    assert (
        get_path_from_module_contents(module_show_lines, "cmake-3.9.2") == "/path/to/cmake-3.9.2"
    )


def test_get_path_from_empty_module():
    assert get_path_from_module_contents("", "test") is None


def test_pkg_dir_from_module_name():
    module_show_lines = ["setenv FOO_BAR_DIR /path/to/foo-bar"]

    assert get_path_from_module_contents(module_show_lines, "foo-bar") == "/path/to/foo-bar"

    assert get_path_from_module_contents(module_show_lines, "foo-bar/1.0") == "/path/to/foo-bar"


def test_get_argument_from_module_line():
    simple_lines = [
        "prepend-path LD_LIBRARY_PATH /lib/path",
        "prepend-path  LD_LIBRARY_PATH  /lib/path",
        "prepend_path('PATH' , '/lib/path')",
        'prepend_path( "PATH" , "/lib/path" )',
        'prepend_path("PATH",' + "'/lib/path')",
    ]

    complex_lines = [
        "prepend-path LD_LIBRARY_PATH /lib/path:/pkg/path",
        "prepend-path  LD_LIBRARY_PATH  /lib/path:/pkg/path",
        "prepend_path('PATH' , '/lib/path:/pkg/path')",
        'prepend_path( "PATH" , "/lib/path:/pkg/path" )',
        'prepend_path("PATH",' + "'/lib/path:/pkg/path')",
    ]

    bad_lines = ["prepend_path(PATH,/lib/path)", "prepend-path (LD_LIBRARY_PATH) /lib/path"]

    assert all(get_path_args_from_module_line(x) == ["/lib/path"] for x in simple_lines)
    assert all(
        get_path_args_from_module_line(x) == ["/lib/path", "/pkg/path"] for x in complex_lines
    )
    for bl in bad_lines:
        with pytest.raises(ValueError):
            get_path_args_from_module_line(bl)


# lmod is entirely unsupported on Windows
def test_lmod_quote_parsing():
    lines = ['setenv("SOME_PARTICULAR_DIR","-L/opt/cray/pe/mpich/8.1.4/gtl/lib")']
    result = get_path_from_module_contents(lines, "some-module")
    assert "/opt/cray/pe/mpich/8.1.4/gtl" == result
