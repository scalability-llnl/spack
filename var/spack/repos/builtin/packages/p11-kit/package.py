# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class P11Kit(AutotoolsPackage):
    """p11-kit aims to solve problems with coordinating the use
    of PKCS #11 by different components or libraries living
    in the same process, by providing a way to load and enumerate
    PKCS #11 modules, as well as a standard configuration setup
    for installing PKCS #11 modules in such a way that they're
    discoverable."""

    homepage = "https://p11-glue.github.io/p11-glue/p11-kit.html"
    url = "https://github.com/p11-glue/p11-kit/archive/0.23.21.tar.gz"

    license("BSD-3-Clause")

    version("0.24.1", sha256="27f3c23531b24a2672ab198a3118f4f399d3a1faa8697924cc8a1065a17ead25")
    version("0.23.21", sha256="0361bcc55858618625a8e99e7fe9069f81514849b7b51ade51f8117d3ad31d88")
    version("0.23.20", sha256="8f6116f34735f6902e9db461c5dbe3e7e25b5cb8c38f42ea2a5aede1cf693749")
    version("0.23.19", sha256="c27921404e82244d97b27f46bae654e5814b5963e0ce3c75ad37007ded46f700")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("gettext", type="build")
    depends_on("libtasn1")
    depends_on("libffi")
