# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hapcut2(MakefilePackage):
    """HapCUT2 is a maximum-likelihood-based tool for assembling haplotypes
       from DNA sequence reads, designed to 'just work' with excellent speed
       and accuracy."""

    homepage = "https://github.com/vibansal/HapCUT2"
    git      = "https://github.com/vibansal/HapCUT2.git"

    version('2017-07-10', commit='2966b94c2c2f97813b757d4999b7a6471df1160e',
            submodules=True)

    depends_on('zlib', type='link')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir('build'):
            install('extractFOSMID', prefix.bin)
            install('extractHAIRS', prefix.bin)
            install('HAPCUT2', prefix.bin)
