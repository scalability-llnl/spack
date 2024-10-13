# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusGsiCertUtils(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the Globus GSI Cert Utils Library Programs.
    """

    homepage = "https://github.com/gridcf/gct/blob/master/gsi/cert_utils/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_gsi_cert_utils-10.11.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("10.11", sha256="0bcbef5e04feda1900407970e52e81ad94f68bceef35313f82c810ddb5bff6ba")

    depends_on("c", type="build")
    depends_on("openssl@1:")
    depends_on("globus-common@14:")
    depends_on("globus-openssl-module@3:")
    depends_on("globus-gsi-openssl-error@2:")
