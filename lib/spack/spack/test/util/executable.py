# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import os

import llnl.util.filesystem as fs
import spack
import spack.util.executable as ex


def test_read_unicode(tmpdir, working_env):
    script_name = 'print_unicode.py'

    with tmpdir.as_cwd():
        os.environ['LD_LIBRARY_PATH'] = spack.main.spack_ld_library_path
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

        # read the unicode back in and see whether things work
        script = ex.Executable('./%s' % script_name)
        assert u'\xc3' == script(output=str).strip()
