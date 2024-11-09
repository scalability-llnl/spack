# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusGsiProxyCore(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the Globus GSI Proxy Core Library.
    """

    homepage = "https://github.com/gridcf/gct/blob/master/gsi/proxy/proxy_core/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_gsi_proxy_core-9.8.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("9.8", sha256="b0865b298d96ffbf6963c0fcb14eb7fd311de67fb25890a677bd6ace13475da3")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("openssl@1:")
    depends_on("globus-common@14:")
    depends_on("globus-openssl-module@3:")
    depends_on("globus-gsi-openssl-error@2:")
    depends_on("globus-gsi-cert-utils@8:")
    depends_on("globus-gsi-sysconfig@5:")
    depends_on("globus-gsi-proxy-ssl@4:")
    depends_on("globus-gsi-credential@5:")
