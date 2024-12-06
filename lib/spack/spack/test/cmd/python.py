# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
import sys

import pytest

import spack
from spack.main import SpackCommand

python = SpackCommand("python")


def test_python():
    out = python("-c", "import spack; print(spack.spack_version)")
    assert out.strip() == spack.spack_version


def test_python_interpreter_path():
    out = python("--path")
    assert out.strip() == sys.executable


def test_python_version():
    out = python("-V")
    assert platform.python_version() in out


def test_python_with_module():
    # pytest rewrites a lot of modules, which interferes with runpy, so
    # it's hard to test this.  Trying to import a module like sys, that
    # has no code associated with it, raises an error reliably in python
    # 2 and 3, which indicates we successfully ran runpy.run_module.
    with pytest.raises(ImportError, match="No code object"):
        python("-m", "sys")


def test_python_raises():
    out = python("--foobar", fail_on_error=False)
    assert "Error: Unknown arguments" in out
