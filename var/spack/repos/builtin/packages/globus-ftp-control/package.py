# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusFtpControl(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the GridFTP Control Library.
    """

    homepage = "https://github.com/gridcf/gct/tree/master/gridftp/control/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_ftp_control-9.7.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("9.10", sha256="86677b4aef54b32bcdc11bb48d63f0a30ee520c8aa60e1f0f51d6cd671ee4010")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("globus-common@14:")
    depends_on("globus-gss-assist@11:")
    depends_on("globus-gssapi-gsi@13:")
    depends_on("globus-io@11:")
    depends_on("globus-xio@3:")
    depends_on("globus-gssapi-error@4:")
