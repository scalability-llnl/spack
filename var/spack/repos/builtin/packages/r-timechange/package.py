# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTimechange(RPackage):
    """Efficient Manipulation of Date-Times.

    Efficient routines for manipulation of date-time objects while accounting
    for time-zones and daylight saving times. The package includes utilities
    for updating of date-time components (year, month, day etc.), modification
    of time-zones, rounding of date-times, period addition and subtraction etc.
    Parts of the 'CCTZ' source code, released under the Apache 2.0 License, are
    included in this package. See <https://github.com/google/cctz> for more
    details."""

    cran = "timechange"

    license("GPL-3.0-only")

    version("0.3.0", sha256="d85c0b5514ab9578d16032e703c33f197feaed1a424c834ebfcbf0ad46ae46b4")
    version("0.2.0", sha256="3d602008052123daef94a5c3f5154c5461b4ec0432ab70c37273d7ddd252f7f1")
    version("0.1.1", sha256="8503919d233d7d7b81fe47692f0f2d6742ff4cae7320a5522bf98f077f5d7f70")

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r-cpp11@0.2.7:", type=("build", "run"))
