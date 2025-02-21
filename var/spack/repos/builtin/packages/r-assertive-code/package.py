# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAssertiveCode(RPackage):
    """Assertions to Check Properties of Code.

    A set of predicates and assertions for checking the properties of code.
    This is mainly for use by other package developers who want to include
    run-time testing features in their own packages. End-users will usually
    want to use assertive directly."""

    cran = "assertive.code"

    version("0.0-4", sha256="2f820474ed20e06f65b284962c87cd1e85220a11cc7fcde09716f0eee5821387")
    version("0.0-3", sha256="ef80e8d1d683d776a7618e78ddccffca7f72ab4a0fcead90c670bb8f8cb90be2")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-assertive-base@0.0-2:", type=("build", "run"))
    depends_on("r-assertive-properties", type=("build", "run"))
    depends_on("r-assertive-types", type=("build", "run"))
