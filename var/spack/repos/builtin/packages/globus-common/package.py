# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusCommon(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the Common Library Programs.
    """

    homepage = "https://github.com/gridcf/gct/tree/master/common/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_common-18.14.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("18.14", sha256="22368942a78e608d8fe6d9f7379abc628e2bd7af54a98c7d2bddc265d6f0ba45")

    depends_on("c", type="build")
