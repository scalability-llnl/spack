# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusGsiProxySsl(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the Globus GSI Proxy SSL Library.
    """

    homepage = "https://github.com/gridcf/gct/tree/master/gsi/proxy/proxy_ssl/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_gsi_proxy_ssl-6.5.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("6.5", sha256="4f20042d80a1fe28b40d9f7f4a1fc9f2790645e9b3f426a659b0c3f01eb04259")

    depends_on("c", type="build")

    depends_on("openssl@1:")
