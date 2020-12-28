# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


class PyMixedhtseq(PythonPackage):
    """HTSeq for mixed single and paired end reads"""

    homepage = "https://github.com/schae234/MixedHTSeq"
    url      = "https://github.com/schae234/MixedHTSeq/archive/v0.1.0.tar.gz"

    version('0.1.0', sha256='234689c8743ae2ba7ad13bc1809a5248184a4b8d16112d5413e09164ab67e157')

    depends_on('python@2.5:2.8', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-htseq', type=('build', 'run'))
    depends_on('py-ipython', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))

    depends_on('py-setuptools', type='build')

    @run_after('install')
    def install_scripts(self):
        shebang = '#!{0}\n'.format(self.spec['python'].command)

        for fname in glob.glob('scripts/*.py'):
            filter_file('^#!.*', '', fname)
            with open(fname, 'r') as orig:
                fdata = orig.read()
            with open(fname, 'w') as new:
                new.write(shebang + fdata)
            set_executable(fname)

        mkdirp(self.prefix.bin)
        install_tree('scripts', self.prefix.bin)
