# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Montage(MakefilePackage):
    """Montage is a toolkit for assembling Flexible Image Transport System
       (FITS) images into custom mosaics."""

    homepage = "http://montage.ipac.caltech.edu/"
    url      = "http://montage.ipac.caltech.edu/download/Montage_v6.0.tar.gz"

    version('6.0', sha256='1f540a7389d30fcf9f8cd9897617cc68b19350fbcde97c4d1cdc5634de1992c6')

    depends_on('freetype')
    depends_on('bzip2')
    depends_on('libpng')

    def install(self, spec, prefix):
        # not using autotools, just builds bin and lib in the source directory
        mkdirp(prefix.bin, prefix.lib)

        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
