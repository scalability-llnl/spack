# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack.package import *


class Laynii(MakefilePackage):
    """Stand alone fMRI software suite for layer-fMRI analyses."""

    homepage = "https://layerfmri.com"
    url = "https://github.com/layerfMRI/LAYNII/archive/refs/tags/v2.7.0.tar.gz"

    license("BSD-3-Clause")

    version("2.7.0", sha256="f0f45c6e80afaca1d89a4721dda70f152c175434e19358974a221ef9c713826b")

    depends_on("cxx", type="build")

    depends_on("zlib")

    def edit(self, spec, prefix):
        pass

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        for file in glob.glob("LN*"):
            install(file, prefix.bin)
