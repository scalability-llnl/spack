# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BppPhylOmics(CMakePackage):
    """Bio++ Phylogenetic Omics Library"""

    homepage = "http://biopp.univ-montp2.fr/wiki/index.php/Installation"
    url = "https://github.com/BioPP/bpp-phyl-omics/archive/v2.4.1.tar.gz"

    license("CECILL-2.0")

    version("2.4.1", sha256="fb0908422e59c71065db874e68d5c71acddf66d8a51776f7e04a5f8d5f0f6577")
    version("2.4.0", sha256="56cc0da613e72dbb8d0ed10d8209e182804a850fd96df1481e4710df97f18435")
    version("2.3.2", sha256="2320e2d33f7bc66bd1a1f0771a8d85e41ad3cec0347cef0f09463ba86f6efa96")
    version("2.3.1", sha256="f4853b99bf0baacf96c9ba567a5875242283cba5fb6f066d74716c6f7d84bd34")
    version("2.3.0", sha256="c4dc3aa39826c50bd8fe7ee4c56a92c8eb9922edc143864a0e2da34481036009")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.6:", type="build")
    depends_on("bpp-core")
    depends_on("bpp-phyl")
    depends_on("bpp-seq")
    depends_on("bpp-seq-omics")
