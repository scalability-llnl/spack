# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Seemake(Package):
    """A build tool."""

    homepage = "http://www.example.com"
    url = "http://www.example.com/tdep-1.0.tar.gz"

    tags = ["build-tools"]

    variant("rundep", default=False, description="activate run-time dependency")
    variant("nestedrundep", default=False, description="activate nested run-time dependency")

    version("4.0", md5="0123456789abcdef0123456789abcdef")
    version("3.0", md5="0123456789abcdef0123456789abcdef")

    depends_on("gmake@4", when="@4", type=("build"))
    depends_on("gmake@3", when="@3", type=("build"))

    depends_on("curl@4", when="@4+rundep", type=("build", "link", "run"))
    depends_on("curl@3", when="@3+rundep", type=("build", "link", "run"))

    depends_on("buildtool@4", when="@4+nestedrundep", type=("build"))
    depends_on("buildtool@3", when="@3+nestedrundep", type=("build"))
