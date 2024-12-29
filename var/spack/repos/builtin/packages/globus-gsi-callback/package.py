# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusGsiCallback(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the Globus GSI Callback Library.
    """

    homepage = "https://github.com/gridcf/gct/tree/master/gsi/callback/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_gsi_callback-6.2.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("6.2", sha256="ffac5435b7d3a78db3c1f856fbe41e7951d5f7d60df3af4ce8cf5b9e303a6f68")

    depends_on("c", type="build")

    depends_on("globus-common@14:")
    depends_on("globus-openssl-module@3:")
    depends_on("globus-gsi-openssl-error@2:")
    depends_on("globus-gsi-cert-utils@8:")
    depends_on("globus-gsi-sysconfig@5:")
