# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tppred(Package):
    """TPPRED is a software package for the prediction of mitochondrial
       targeting peptides from protein primary sequence."""

    homepage = "https://tppred2.biocomp.unibo.it/tppred2/default/software"
    url      = "http://biocomp.unibo.it/savojard/tppred2.tar.gz"

    version('2.0', sha256='0e180d5ce1f0bccfdbc3dbf9981b3fbe2101c85491c58c58c88856861688a4f5')

    depends_on('python@2.7:2.999', type='run')
    depends_on('py-scikit-learn@0.13.1', type='run')
    depends_on('emboss')

    def url_for_version(self, version):
        url = 'http://biocomp.unibo.it/savojard/tppred{0}.tar.gz'
        return url.format(version.up_to(1))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir('bin'):
            install('tppred2.py', prefix.bin)
        install_tree('data', prefix.data)
        install_tree('example', prefix.example)
        install_tree('tppred2modules', prefix.modules)

    def setup_run_environment(self, env):
        env.set('TPPRED_ROOT', self.prefix)
