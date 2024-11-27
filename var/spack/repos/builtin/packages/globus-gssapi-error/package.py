# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusGssapiError(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the GSSAPI Error Library.
    """

    homepage = "https://github.com/gridcf/gct/blob/master/gsi/gssapi_error/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_gssapi_error-6.3.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("6.3", sha256="943261f337ca5547f0e4fed47c8beac14cb125837b265f152c216f9b068dabc4")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("globus-common@14:")
    depends_on("globus-gss-assist@8:")
    depends_on("globus-gssapi-gsi@9:")
