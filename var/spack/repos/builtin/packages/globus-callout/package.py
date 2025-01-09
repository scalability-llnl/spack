# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusCallout(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the Globus Callout Library - provides a
    platform independent way of dealing with runtime loadable functions.
    """

    homepage = "https://github.com/gridcf/gct/tree/master/callout/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_callout-4.3.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("4.3", sha256="367e3fda18c3c3eb2b12496abc504186d0bfa0dadc666f626f580a443bba3000")

    depends_on("c", type="build")

    depends_on("globus-common@15:")
