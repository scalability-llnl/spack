# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusOpensslModule(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the Globus OpenSSL Module Wrapper.
    """

    homepage = "https://github.com/gridcf/gct/blob/master/gsi/openssl_module"
    url = "https://repo.gridcf.org/gct6/sources/globus_openssl_module-5.2.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("5.2", sha256="6dfcbe4af7a23d16745946131da938181cee3adfe08504df4bb4ab3160c23467")

    depends_on("c", type="build")

    depends_on("globus-common@14:")
    depends_on("globus-gsi-proxy-ssl@4:")
    depends_on("globus-gsi-openssl-error@2:")
