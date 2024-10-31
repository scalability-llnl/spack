# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusGsiOpensslError(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the Globus OpenSSL Error Handling.
    """

    homepage = "https://github.com/gridcf/gct/blob/master/gsi/openssl_error/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_gsi_openssl_error-4.4.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("4.4", sha256="1879ff269154431700ed158a75acc6e10ca0c96af95d92bc2fa63b7fe998fa6e")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("openssl@1:")
    depends_on("globus-common@14:")
