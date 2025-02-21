# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTzdb(RPackage):
    """Time Zone Database Information.

    Provides an up-to-date copy of the Internet Assigned Numbers Authority
    (IANA) Time Zone Database. It is updated periodically to reflect changes
    made by political bodies to time zone boundaries, UTC offsets, and
    daylight saving time rules. Additionally, this package provides a C++
    interface for working with the 'date' library. 'date' provides
    comprehensive support for working with dates and date-times, which this
    package exposes to make it easier for other R packages to utilize. Headers
    are provided for calendar specific calculations, along with a limited
    interface for time zone manipulations."""

    cran = "tzdb"

    license("MIT")

    version("0.4.0", sha256="4253c66041bdddfd463c98183bf0052fbcacdb7c5cff9eadbb858b3dcf9d3a23")
    version("0.3.0", sha256="6099f0ec1fba692b51b4360aa776902a39f10dae815933c31994b8e4d4277038")
    version("0.2.0", sha256="c335905d452b400af7ed54b916b5246cb3f47ede0602911a2bcb25a1cf56d5a9")

    depends_on("r@3.3:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@0.3.0:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@0.4.0:")
    depends_on("r-cpp11@0.4.0:", type=("build", "run"))
    depends_on("r-cpp11@0.4.2:", type=("build", "run"), when="@0.3.0:")
