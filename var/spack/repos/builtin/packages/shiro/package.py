# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shiro(MavenPackage):
    """Apache Shiro is a powerful and easy-to-use Java security framework
    that performs authentication, authorization, cryptography, and session
    management. With Shiro's easy-to-understand API, you can quickly and
    easily secure any application - from the smallest mobile applications
    to the largest web and enterprise applications."""

    homepage = "https://shiro.apache.org/"
    url = "https://github.com/apache/shiro/archive/shiro-root-1.6.0.tar.gz"

    license("Apache-2.0")

    version("1.6.0", sha256="50338badfd3261076060fbe70330089512d38071bc51aa3f84ad23e707d2b7c9")
    version("1.5.3", sha256="25c5d99eddf790969e0f80bd9769f773465c9c9e1e8ec1f549f476bdae8c6983")

    depends_on("java@8:", type=("build", "run"))
    depends_on("maven@3.5:3", type="build")
