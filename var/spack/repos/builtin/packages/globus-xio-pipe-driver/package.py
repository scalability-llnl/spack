# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusXioPipeDriver(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the Globus Pipe Driver.
    """

    homepage = "https://github.com/gridcf/gct/blob/master/xio/drivers/pipe/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_xio_pipe_driver-4.1.tar.gz"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("4.1", sha256="90860e3bf7c66791f873f488b3b31892d386ac9d73dd4bb366ae8d39fd16ba66")

    depends_on("c", type="build")

    depends_on("globus-common@14:")
    depends_on("globus-xio@3:")
