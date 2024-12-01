# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusGassTransfer(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the  Globus Gass Transfer.
    """

    homepage = "https://github.com/gridcf/gct/blob/master/gass/transfer/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_gass_transfer-9.4.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("9.4", sha256="c5ad54d0e4959f7dc4131918ad9d40d49db2823b84aec8229127826a9601fbf9")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("globus-common@14:")
    depends_on("globus-gssapi-gsi@10:")
    depends_on("globus-gss-assist@8:")
    depends_on("globus-io@8:")
