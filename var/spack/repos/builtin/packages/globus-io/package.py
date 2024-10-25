# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusIo(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the uniform I/O interface to stream and
    datagram style communications.
    """

    homepage = "https://github.com/gridcf/gct/tree/master/io/compat"
    url = "https://repo.gridcf.org/gct6/sources/globus_io-12.4.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("12.4", sha256="992de8d1d6c1a0c4edccd798084b6a7f8b93155ba7ae110d836dc248a2f7005a")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("globus-common@14:")
    depends_on("globus-xio@3:")
    depends_on("globus-gss-assist@8:")
    depends_on("globus-gssapi-gsi@10:")
    depends_on("globus-xio-gsi-driver@2:")
    depends_on("globus-gssapi-error@4:")
