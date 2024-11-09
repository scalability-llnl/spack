# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CgsiGsoap(CMakePackage):
    """Client and server side library to secure gSOAP
    using the Globus Security Infrastructure."""

    homepage = "https://github.com/cern-fts/cgsi-gsoap"
    url = "https://github.com/cern-fts/cgsi-gsoap/archive/refs/tags/v1.3.12.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("1.3.12", sha256="ebb141ea7fe6d883ebeca031b4f2e3697895efb8fde55ee214128d5ca37e13e4")

    depends_on("c", type="build")

    depends_on("pkg-config", type="build")
    depends_on("gsoap")
    depends_on("voms")
    depends_on("globus-common")
    depends_on("globus-gssapi-gsi")
    depends_on("globus-gss-assist")
    depends_on("globus-gsi-cert-utils")
    depends_on("globus-gsi-credential")
    depends_on("globus-openssl-module")
