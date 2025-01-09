# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusGsiCredential(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the Globus GSI Credential Library.
    """

    homepage = "https://github.com/gridcf/gct/tree/master/gsi/credential/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_gsi_credential-8.4.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("8.4", sha256="19e8fde9d4b335d60a021ac58c7559e5c34981e9332a8e574eda0b44ec160fa7")

    depends_on("c", type="build")
    depends_on("globus-common@14:")
    depends_on("globus-gsi-openssl-error@2:")
    depends_on("globus-gsi-cert-utils@8:")
    depends_on("globus-gsi-sysconfig@5:")
    depends_on("globus-gsi-callback@4:")
