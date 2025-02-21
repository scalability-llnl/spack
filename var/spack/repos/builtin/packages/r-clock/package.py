# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RClock(RPackage):
    """Date-Time Types and Tools.

    Provides a comprehensive library for date-time manipulations using a new
    family of orthogonal date-time classes (durations, time points,
    zoned-times, and calendars) that partition responsibilities so that the
    complexities of time zones are only considered when they are really needed.
    Capabilities include: date-time parsing, formatting, arithmetic, extraction
    and updating of components, and rounding."""

    cran = "clock"

    license("MIT")

    version("0.7.1", sha256="432d2fc39d3f20e348f09a9b6136a02a588db585bab428d184da71bf6aa1f0d8")
    version("0.6.1", sha256="f80c385fd8229538968ffb71d7de53ddc82bfcec6641f8e76f299546c43c1702")

    depends_on("r@3.4:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@0.7.1:")
    depends_on("r-cli@3.6.1:", type=("build", "run"), when="@0.7.0:")
    depends_on("r-lifecycle@1.0.3:", type=("build", "run"), when="@0.7.0:")
    depends_on("r-rlang@1.0.4:", type=("build", "run"))
    depends_on("r-rlang@1.1.0:", type=("build", "run"), when="@0.7.0:")
    depends_on("r-tzdb@0.3.0:", type=("build", "run"))
    depends_on("r-tzdb@0.4.0:", type=("build", "run"), when="@0.7.0:")
    depends_on("r-vctrs@0.4.1:", type=("build", "run"))
    depends_on("r-vctrs@0.6.1:", type=("build", "run"), when="@0.7.0:")
    depends_on("r-cpp11@0.4.2:", type=("build", "run"))
    depends_on("r-cpp11@0.4.3:", type=("build", "run"), when="@0.7.0:")
