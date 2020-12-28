# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SnapBerkeley(MakefilePackage):
    """SNAP is a fast and accurate aligner for short DNA reads. It is
       optimized for modern read lengths of 100 bases or higher, and takes
       advantage of these reads to align data quickly through a hash-based
       indexing scheme."""

    homepage = "http://snap.cs.berkeley.edu/"
    url      = "https://github.com/amplab/snap/archive/v1.0beta.18.tar.gz"

    version('1.0beta.18', sha256='9e8a8dc3f17e3f533d34011afe98316c19cbd70cc8b4830375611e003697daee')
    version('0.15',       sha256='bea0174c8d01907023494d7ffd2a6dab9c38d248cfe4d3c26feedf9d5becce9a', preferred=True)

    depends_on('zlib')

    conflicts('%gcc@6:')
    conflicts('%cce')
    conflicts('%apple-clang')
    conflicts('%clang')
    conflicts('%intel')
    conflicts('%nag')
    conflicts('%pgi')
    conflicts('%xl')
    conflicts('%xl_r')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        if self.spec.satisfies('@1.0beta.18:'):
            install('snap-aligner', prefix.bin)
            install('SNAPCommand', prefix.bin)
        else:
            install('snap', prefix.bin)
