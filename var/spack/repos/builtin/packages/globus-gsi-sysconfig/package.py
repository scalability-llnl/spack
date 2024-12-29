# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusGsiSysconfig(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the Globus GSI System Config Library.
    """

    homepage = "https://github.com/gridcf/gct/blob/master/gsi/sysconfig/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_gsi_sysconfig-9.6.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("9.6", sha256="7d843374eb64605dda206b84cad2a5c39a1bc9b18e9bfd93591c8fcb6d5a1a7a")

    depends_on("c", type="build")

    depends_on("globus-common@15:")
    depends_on("globus-openssl-module@e3:")
    depends_on("globus-gsi-openssl-error@2:")
