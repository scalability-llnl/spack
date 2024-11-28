# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusXioGsiDriver(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the Globus XIO GSI Driver.
    """

    homepage = "https://github.com/gridcf/gct/blob/master/xio/drivers/gsi"
    url = "https://repo.gridcf.org/gct6/sources/globus_xio_gsi_driver-5.4.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("5.4", sha256="9a28f8da77efbd8560bcfacdd514f81f5653d1c612d7fe3c479e52a4c8c1ed76")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("globus-common@14:")
    depends_on("globus-gssapi-gsi@13:")
    depends_on("globus-gssapi-error@4:")
    depends_on("globus-gss-assist@11:")
    depends_on("globus-xio@3:")
