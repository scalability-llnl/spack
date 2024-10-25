# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSf(RPackage):
    """Simple Features for R.

    Support for simple features, a standardized way to encode spatial vector
    data. Binds to 'GDAL' for reading and writing data, to 'GEOS' for
    geometrical operations, and to 'PROJ' for projection conversions and datum
    transformations. Optionally uses the 's2' package for spherical geometry
    operations on geographic coordinates."""

    cran = "sf"

    license("GPL-2.0-only OR MIT")

    version("1.0-12", sha256="3778ebf58d824b1dfa6297ca8363714d5d85eda04c55ab2bf39597cac1d91287")
    version("1.0-9", sha256="85c0c71a0a64750281e79aa96e36d13e6285927008b2d37d699e52aba7d8013b")
    version("1.0-8", sha256="3ddc7090e79d6b5e3fad69e01254677ab5ec86a0b25e7e73493c8eac0ea98732")
    version("1.0-7", sha256="d0731fab9438d73a55af7232f0474b36f4b2a4e6d66adaa141632f4a60265453")
    version("1.0-5", sha256="290c28fa5ea777d555e70962c59079c134f02f7bdf60259a72eea79a064a1ac4")
    version("0.9-7", sha256="4acac2f78badf9d252da5bf377975f984927c14a56a72d9f83d285c0adadae9c")
    version("0.7-7", sha256="d1780cb46a285b30c7cc41cae30af523fbc883733344e53f7291e2d045e150a4")
    version("0.7-5", sha256="53ed0567f502216a116c4848f5a9262ca232810f82642df7b98e0541a2524868")
    with default_args(deprecated=True):
        # deprecated @:0.7-3 as gdal@:2 is deprecated, and gdal@3: requires proj@6:
        version("0.5-5", sha256="82ad31f98243b6982302fe245ee6e0d8d0546e5ff213ccc00ec3025dfec62229")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r-classint@0.2-1:", type=("build", "run"))
    depends_on("r-classint@0.4-1:", type=("build", "run"), when="@0.9-7:")
    depends_on("r-dbi@0.8:", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-rcpp@0.12.18:", type=("build", "run"))
    depends_on("r-s2@1.0.7:", type=("build", "run"), when="@1.0-5:")
    depends_on("r-s2@1.1.0:", type=("build", "run"), when="@1.0-9:")
    depends_on("r-units", type=("build", "run"))
    depends_on("r-units@0.6-0:", type=("build", "run"), when="@1.0-5:")
    depends_on("r-units@0.7-0:", type=("build", "run"), when="@1.0-8:")
    depends_on("gdal@2.0.1:")
    depends_on("geos@3.4.0:")
    depends_on("proj@4.8.0:5", when="@:0.7-3")
    depends_on("proj@4.8.0:6", when="@0.7-4:0.7-7")
    depends_on("proj@4.8.0:")
    depends_on("sqlite", when="@0.9-7:")
