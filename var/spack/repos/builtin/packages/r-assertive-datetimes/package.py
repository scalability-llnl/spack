# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAssertiveDatetimes(RPackage):
    """Assertions to Check Properties of Dates and Times.

    A set of predicates and assertions for checking the properties of dates and
    times. This is mainly for use by other package developers who want to
    include run-time testing features in their own packages.  End-users will
    usually want to use assertive directly."""

    cran = "assertive.datetimes"

    version("0.0-3", sha256="014e2162f5a8d95138ed8330f7477e71c908a29341697c09a1b7198b7e012d94")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-assertive-base@0.0-7:", type=("build", "run"))
    depends_on("r-assertive-types", type=("build", "run"))
