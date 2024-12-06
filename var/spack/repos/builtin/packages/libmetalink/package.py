# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmetalink(AutotoolsPackage):
    """Libmetalink is a library to read Metalink XML download description
    format. It supports both Metalink version 3 and Metalink version 4
    (RFC 5854)."""

    homepage = "https://launchpad.net/libmetalink"
    url = "https://github.com/metalink-dev/libmetalink/archive/release-0.1.3.tar.gz"

    license("MIT")

    version("0.1.3", sha256="7469c4a64b9dd78c3f23fa575fe001bbfd548c181492a2067b59609872122d7a")
    version("0.1.2", sha256="64af0979c11658f7a1659ca97ebc3c7bac8104253bf504015ac3b9c363382bae")
    version("0.1.1", sha256="e9b8dff68b0b999884c21f68d9b1cc0c1993270e3e1f639f82e27b1eb960cb66")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("expat@2.1.0:")
    depends_on("libxml2@2.7.8:")
