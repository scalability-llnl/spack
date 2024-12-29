# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusGssAssist(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the GSSAPI Assist library Programs.
    """

    homepage = "https://github.com/gridcf/gct/blob/master/gsi/gss_assist/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_gss_assist-12.7.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("12.7", sha256="5184e0f1a09a64651472f19b79101fc6d966056fd9e1ee29512e41f694eae759")

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("globus-common@14:")
    depends_on("globus-gsi-sysconfig@7:")
    depends_on("globus-gsi-cert-utils@8:")
    depends_on("globus-gssapi-gsi@13:")
    depends_on("globus-callout@2:")
    depends_on("globus-gsi-credential@6:")
