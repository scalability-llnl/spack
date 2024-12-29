# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusGassCopy(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the Globus Gass Copy Programs.
    """

    homepage = "https://github.com/gridcf/gct/tree/master/gass/copy/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_gass_copy-10.13.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("10.13", sha256="f8b301b99de8f236733486767409d952024e16ff44ccfa8627063eefcbc8fe45")

    depends_on("c", type="build")

    depends_on("globus-common@15:")
    depends_on("globus-ftp-client@7:")
    depends_on("globus-ftp-control@4:")
    depends_on("globus-gsi-sysconfig@4:")
    depends_on("globus-gass-transfer@7:")
    depends_on("globus-io@8:")
    depends_on("globus-gssapi-gsi@9:")
    depends_on("globus-gssapi-error@4:")
