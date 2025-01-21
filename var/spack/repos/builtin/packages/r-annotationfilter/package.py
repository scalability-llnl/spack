# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAnnotationfilter(RPackage):
    """Facilities for Filtering Bioconductor Annotation Resources.

    This package provides class and other infrastructure to implement
    filters for manipulating Bioconductor annotation resources. The filters
    will be used by ensembldb, Organism.dplyr, and other packages."""

    bioc = "AnnotationFilter"

    version("1.30.0", commit="1204cb5c19fde6628e99279ffca8e1b0b2a1219b")
    version("1.28.0", commit="61709ad226a834e6c80b02199c170d7784f23196")
    version("1.26.0", commit="be933b32635c36571f43c1aa6ec3b1efab0dd1da")
    version("1.24.0", commit="172d9c149d9025154f7b26982d07f571499b03e8")
    version("1.22.0", commit="c9fea4a829ce9419b6e0af987915b2d469358597")
    version("1.20.0", commit="2818aff6502fd6fe819521cd8d97695ef6f9198e")
    version("1.18.0", commit="60a9b666d7362d7ed5c357fd4a5d2744d8598c20")
    version("1.14.0", commit="6ee3a13ed93a535ed452cbc8c118151a2cbb732c")
    version("1.8.0", commit="9bf70ead899e32e84e2908f2b29cd38250d2d1ed")
    version("1.6.0", commit="fa40a7e17e93fac9e85091ff93f256adf145dec3")
    version("1.4.0", commit="acbd3309f478843a7899bd9773af5f19f986b829")
    version("1.2.0", commit="744b82915d7b85031de462d9d0a2bf9fdfd0e29d")
    version("1.0.0", commit="a9f79b26defe3021eea60abe16ce1fa379813ec9")

    depends_on("r@3.4.0:", type=("build", "run"))
    depends_on("r-genomicranges", type=("build", "run"))
    depends_on("r-lazyeval", type=("build", "run"))
