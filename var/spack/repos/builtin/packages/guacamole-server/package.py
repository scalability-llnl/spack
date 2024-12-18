# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GuacamoleServer(AutotoolsPackage):
    """The guacamole-server package is a set of software which forms the
    basis of the Guacamole stack. It consists of guacd, libguac, and
    several protocol support libraries."""

    homepage = "https://guacamole.apache.org/"
    url = "https://github.com/apache/guacamole-server/archive/1.1.0.tar.gz"

    license("GPL-3.0-or-later")

    version("1.5.5", sha256="50430c0f0f3b92f2cd3e60436fab0cedee8c1a9f762696a666016347039c731e")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2023-43826
        version("1.1.0", sha256="d0f0c66ebfa7a4fd6689ae5240f21797b5177945a042388b691b15b8bd5c81a8")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("cairo +pdf +png")  # pdf enables zlib support required for CairoScript
    depends_on("libjpeg")
    depends_on("libpng")
    depends_on("uuid")
