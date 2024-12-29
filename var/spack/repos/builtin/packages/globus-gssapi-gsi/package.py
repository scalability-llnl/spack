# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusGssapiGsi(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the GSSAPI library.
    """

    homepage = "https://github.com/gridcf/gct/tree/master/gsi/gssapi/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_gssapi_gsi-14.20.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("14.20", sha256="2ba4e905f1dbbbee8ade01a6d0d59a9b5e816620fe5b080de0524b5331614236")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("awk", type="build")

    depends_on("openssl")

    depends_on("globus-common@14:")
    depends_on("globus-openssl-module@3:")
    depends_on("globus-gsi-openssl-error@2:")
    depends_on("globus-gsi-cert-utils@8:")
    depends_on("globus-gsi-credential@5:")
    depends_on("globus-gsi-callback@4:")
    depends_on("globus-gsi-proxy-core@8:")
    depends_on("globus-gsi-sysconfig@8:")
