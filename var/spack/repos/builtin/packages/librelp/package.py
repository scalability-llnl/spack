# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Librelp(AutotoolsPackage):
    """Librelp is an easy to use library for the RELP protocol. RELP
    (stands for Reliable Event Logging Protocol) is a general-purpose,
    extensible logging protocol."""

    homepage = "https://www.rsyslog.com/librelp/"
    url = "https://github.com/rsyslog/librelp/archive/v1.7.0.tar.gz"

    license("GPL-3.0-or-later")

    version("1.7.0", sha256="ff46bdd74798934663d1388d010270325dc6a6ed6d44358ca69b280a8304b1e9")
    version("1.6.0", sha256="acaaa6b8e295ecd8e9d9b70c1c3c8fb3cc3c95a9ed5ce1689688510d0eecb37e")
    version("1.5.0", sha256="ce7f463944417ba77d7b586590e41e276f7b107d3e35a77ce768cf3889b5e1a6")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("valgrind", type="test")
    depends_on("openssl")
    depends_on("gnutls@2.0.0:")
