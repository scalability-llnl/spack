# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fipscheck(AutotoolsPackage):
    """The integrity check is only one of many requirements needed for
    validation of a software cryptographic module."""

    homepage = "https://github.com/LairdCP/fipscheck"
    url = "https://github.com/LairdCP/fipscheck/archive/LRD-REL-7.0.0.398.tar.gz"

    version("7.0.0.398", sha256="1b78c71b8b39d948926910644ad544719ce6f69672d3205bc36a5924a07f6e9b")
    version("7.0.0.397", sha256="6bce42faabf372d08b6f8fadb4fa9e65671bebf6c0c91eab8c59ae96b1e7d600")
    version("7.0.0.396", sha256="058aafac78f3c0c5b65107686538b09eeb52cbb9b7ede688f3502df7d69c1209")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")
