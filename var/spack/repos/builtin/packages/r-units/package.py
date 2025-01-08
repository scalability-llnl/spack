# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUnits(RPackage):
    """Measurement Units for R Vectors.

    Support for measurement units in R vectors, matrices and arrays: automatic
    propagation, conversion, derivation and simplification of units; raising
    errors in case of unit incompatibility. Compatible with the POSIXct, Date
    and difftime  classes. Uses the UNIDATA udunits library and unit database
    for  unit compatibility checking and conversion. Documentation about
    'units' is provided in the paper by Pebesma, Mailund & Hiebert (2016,
    <doi:10.32614/RJ-2016-061>), included in this package as a vignette; see
    'citation("units")' for details."""

    cran = "units"

    license("GPL-2.0-only")

    version("0.8-5", sha256="d95e80af760b053e10a1e33ce1f0c1280a84e84bd4b1d9c34d1fe9fc153603b1")
    version("0.8-1", sha256="d3e1ba246b4c97205bc3da3cf45d6b5bd5c196b8d421b84b4e94b2090985cd9a")
    version("0.8-0", sha256="9c46fe138e8c1c3d3a51268776412f02d09673656516148cccb71b1071beb21a")
    version("0.7-2", sha256="b90be023431100632b3081747af9e743e615452b4ad38810991f7b024b7040eb")
    version("0.6-7", sha256="3f73a62bafdbe0f93bbf00ac4b1adb8f919dd04649ff8f1d007f2986e35cb7e5")
    version("0.6-3", sha256="03de88d9dcfe80d22dd3813413f33657c576aed24a8091dbfc7f68602020a64f")
    version("0.6-2", sha256="5e286775d0712c8e15b6ae3a533d4c4349b0f6410c2d9d897ca519c3d0e5f170")
    version("0.4-6", sha256="db383c9b7ec221a5da29a2ddf4f74f9064c44ea2102ea7e07cc1cc5bb30fa1ef")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r-rcpp@0.12.10:", type=("build", "run"))
    depends_on("udunits", when="@0.6-0:")

    depends_on("r-udunits2@0.13:", type=("build", "run"), when="@:0.5-1")
