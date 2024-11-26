# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusFtpClient(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the GridFTP Client Library.
    """

    homepage = "https://github.com/gridcf/gct/tree/master/gridftp/client/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_ftp_client-9.8.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("9.8", sha256="aa83229f70352e106fc29f28cef4fc8fdab37c794603e7b425f193d947e5926c")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("openssl")
    depends_on("globus-common@15:")
    depends_on("globus-ftp-control@4:")
    depends_on("globus-gsi-callback@4:")
    depends_on("globus-gsi-credential@5:")
    depends_on("globus-gsi-sysconfig@5:")
    depends_on("globus-gssapi-gsi@10:")
    depends_on("globus-xio@3:")
    depends_on("globus-xio-popen-driver@2:")
