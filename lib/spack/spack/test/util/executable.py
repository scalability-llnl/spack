# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import os

import pytest

import llnl.util.filesystem as fs

import spack
import spack.util.executable as ex
from spack.hooks.sbang import filter_shebangs_in_directory


def test_read_unicode(tmpdir, working_env):
    script_name = 'print_unicode.py'

    with tmpdir.as_cwd():
        for var, val in spack.main.spack_python_env:
            if val is None:
                os.environ.pop(var, None)
            else:
                os.environ[var] = val
        # make a script that prints some unicode
        with open(script_name, 'w') as f:
            f.write('''#!{0}
from __future__ import print_function
import sys
if sys.version_info < (3, 0, 0):
    reload(sys)
    sys.setdefaultencoding('utf8')
print(u'\\xc3')
'''.format(sys.executable))

        # make it executable
        fs.set_executable(script_name)
        filter_shebangs_in_directory('.', [script_name])

        # read the unicode back in and see whether things work
        script = ex.Executable('./%s' % script_name)
        assert u'\xc3' == script(output=str).strip()


def test_which_relative_path_with_slash(tmpdir, working_env):
    tmpdir.ensure('exe')
    path = str(tmpdir.join('exe'))
    os.environ['PATH'] = ''

    with tmpdir.as_cwd():
        no_exe = ex.which('./exe')
        assert no_exe is None

        fs.set_executable(path)
        exe = ex.which('./exe')
        assert exe.path == path


def test_which_with_slash_ignores_path(tmpdir, working_env):
    tmpdir.ensure('exe')
    tmpdir.ensure('bin{0}exe'.format(os.path.sep))

    path = str(tmpdir.join('exe'))
    wrong_path = str(tmpdir.join('bin', 'exe'))
    os.environ['PATH'] = os.path.dirname(wrong_path)

    fs.set_executable(path)
    fs.set_executable(wrong_path)

    with tmpdir.as_cwd():
        exe = ex.which('./exe')
        assert exe.path == path


def test_which(tmpdir):
    os.environ["PATH"] = str(tmpdir)
    assert ex.which("spack-test-exe") is None
    with pytest.raises(ex.CommandNotFoundError):
        ex.which("spack-test-exe", required=True)

    with tmpdir.as_cwd():
        fs.touch("spack-test-exe")
        fs.set_executable('spack-test-exe')

    exe = ex.which("spack-test-exe")
    assert exe is not None
    assert exe.path == str(tmpdir.join("spack-test-exe"))
