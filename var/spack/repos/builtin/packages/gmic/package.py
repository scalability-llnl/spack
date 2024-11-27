# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gmic(MakefilePackage):
    """G'MIC is an open-source framework for digital image processing.
    G'MIC is a full-featured open-source framework for digital image
    processing, distributed under the CeCILL free software licenses (LGPL-like
    and/or GPL-compatible). It provides several user interfaces to convert /
    process / visualize generic image datasets, ranging from 1D scalar signals
    to 3D+t sequences of multi-spectral volumetric images, hence including 2D
    color images."""

    homepage = "https://gmic.eu/"
    git = "https://github.com/GreycLab/gmic.git"

    license("CECILL-2.1")

    version("develop", branch="master")
    version("3.1.6", tag="v.3.1.6")

    depends_on("curl")
    depends_on("fftw")
    depends_on("libjpeg")
    depends_on("libtiff")
    depends_on("libxau")
    depends_on("libxcb")
    depends_on("libpng")
    depends_on("openexr")
    depends_on("opencv")
    depends_on("zlib-api")
    depends_on("zstd")
    depends_on("libx11")

    def build(self, spec, prefix):
        make("cli")

    def install(self, spec, prefix):
        make("install PREFIX='' USR='' DESTDIR={0}".format(self.prefix))
