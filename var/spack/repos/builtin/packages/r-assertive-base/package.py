# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAssertiveBase(RPackage):
    """A Lightweight Core of the 'assertive' Package.

    A minimal set of predicates and assertions used by the assertive package.
    This is mainly for use by other package developers who want to include
    run-time testing features in their own packages. End-users will usually
    want to use assertive directly."""

    cran = "assertive.base"

    version("0.0-9", sha256="4bf0910b0eaa507e0e11c3c43c316b524500c548d307eb045d6f89047e6ba01e")
    version("0.0-7", sha256="f02d4eca849f512500abb266a2a751d1fa2cf064f7142e5161a77c20b7f643f7")
    version("0.0-1", sha256="6a5fb06ad912f01cd8aaf2aa7c8ca03b8ebbb1c5eb2be47fa145930f15f4d258")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@0.0-9:")
