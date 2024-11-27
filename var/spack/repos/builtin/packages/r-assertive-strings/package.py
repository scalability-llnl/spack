# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAssertiveStrings(RPackage):
    """Assertions to Check Properties of Strings.

    A set of predicates and assertions for checking the properties of strings.
    This is mainly for use by other package developers who want to include
    run-time testing features in their own packages. End-users will usually
    want to use assertive directly."""

    cran = "assertive.strings"

    version("0.0-3", sha256="d541d608a01640347d661cc9a67af8202904142031a20caa270f1c83d0ccd258")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-assertive-base@0.0-2:", type=("build", "run"))
    depends_on("r-assertive-types", type=("build", "run"))
    depends_on("r-stringi", type=("build", "run"))
