# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTclust(RPackage):
    """Robust Trimmed Clustering.

    Provides functions for robust trimmed clustering. The methods are described
    in Garcia-Escudero (2008) <doi:10.1214/07-AOS515>, Fritz et al. (2012)
    <doi:10.18637/jss.v047.i12>, Garcia-Escudero et al. (2011)
    <doi:10.1007/s11222-010-9194-z> and others."""

    cran = "tclust"

    license("GPL-3.0-only")

    version("2.0-4", sha256="a6667167778b974afc968340161171a7911415bcc1220dc7f0f350552f560578")
    version("1.5-4", sha256="2b55da5e351c5054c9627f57a43084518a138a1d8097e35a364db0eff63471a8")
    version("1.5-2", sha256="492674b30a465e5f4a22ba0ce5556ed4d8e57b29090f9b5b94ad655d064e6f8b")
    version("1.5-1", sha256="73328b30774bb0767d613d7f2b60b75706b19fab864c712645ea18181f1af327")
    version("1.4-2", sha256="95dcd07dbd16383f07f5cea8561e7f3bf314e4a7483879841103b149fc8c65d9")
    version("1.4-1", sha256="4b0be612c8ecd7b4eb19a44ab6ac8f5d40515600ae1144c55989b6b41335ad9e")
    version("1.3-1", sha256="fe4479a73b947d8f6c1cc63587283a8b6223d430d39eee4e5833a06d3d1726d2")
    version("1.2-7", sha256="7d2cfa35bbd44086af45be842e6c4743380c7cc8a0f985d2bb7c1a0690c878d7")
    version("1.2-3", sha256="d749d4e4107b876a22ca2c0299e30e2c77cb04f53f7e5658348e274aae3f2b28")
    version("1.1-03", sha256="b8a62a1d27e69ac7e985ba5ea2ae5d182d2e51665bfbfb178e22b63041709270")
    version("1.1-02", sha256="f73c0d7a495552f901b710cf34e114c0ba401d5a17c48156313245904bcccad4")

    depends_on("r@2.12.0:", type=("build", "run"))
    depends_on("r@3.6.2:", type=("build", "run"), when="@1.5-6:")

    depends_on("r-doparallel", type=("build", "run"), when="@2.0:")
    depends_on("r-foreach", type=("build", "run"), when="@2.0:")
    depends_on("r-mass", type=("build", "run"), when="@2.0:")
    depends_on("r-rcpp@1.0.7:", type=("build", "run"), when="@2.0:")
    depends_on("r-rcpparmadillo", type=("build", "run"), when="@2.0:")
