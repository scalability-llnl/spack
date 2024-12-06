# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAssertiveDataUs(RPackage):
    """Assertions to Check Properties of Strings.

    A set of predicates and assertions for checking the properties of
    US-specific complex data types. This is mainly for use by other package
    developers who want to include run-time testing features in their own
    packages.  End-users will usually want to use assertive directly."""

    cran = "assertive.data.us"

    version("0.0-2", sha256="180e64dfe6339d25dd27d7fe9e77619ef697ef6e5bb6a3cf4fb732a681bdfaad")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-assertive-base@0.0-2:", type=("build", "run"))
    depends_on("r-assertive-strings", type=("build", "run"))
