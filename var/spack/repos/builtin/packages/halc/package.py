# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Halc(MakefilePackage):
    """HALC is software that makes error correction for long reads with
     high throughput."""

    homepage = "https://github.com/lanl001/halc"
    url      = "https://github.com/lanl001/halc/archive/v1.1.tar.gz"

    version('1.1', sha256='79675c3d6c40f567c2e1a5b5e7ec4fb150036582054f6ad079e06b73bd71c1ad')

    depends_on('blasr', type='run')
    depends_on('lordec', type='run')
    depends_on('dos2unix', type='build')
    depends_on('python', type='run')

    parallel = False

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
        install('runHALC.py', prefix.bin)
        dos2unix = which('dos2unix')
        dos2unix(join_path(self.prefix.bin, 'runHALC.py'))
