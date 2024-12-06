# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGitcreds(RPackage):
    """Query 'git' Credentials from 'R'.

    Query, set, delete credentials from the 'git' credential store. Manage
    'GitHub' tokens and other 'git' credentials. This package is to be used by
    other packages that need to authenticate to 'GitHub' and/or other 'git'
    repositories."""

    cran = "gitcreds"

    license("MIT")

    version("0.1.2", sha256="41c6abcca5635062b123ffb5af2794770eca5ebd97b05c5a64b24fa1c803c75d")
    version("0.1.1", sha256="b14aaf4e910a9d2d6c65c93e645f0b0159c00898e669f917f83c03dfedb1dfea")

    depends_on("r@3.4:", type=("build", "run"), when="@0.1.2:")

    depends_on("git", type="run")
