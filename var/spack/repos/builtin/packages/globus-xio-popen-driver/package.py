# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GlobusXioPopenDriver(AutotoolsPackage):
    """The Grid Community Toolkit (GCT) is an open source software
    toolkit used for building grid systems and applications. It is a fork
    of the Globus Toolkit originally created by the Globus Alliance.
    It is supported by the Grid Community Forum (GridCF) that provides
    community-based support for core software packages in grid computing.

    This package contains the Globus XIO Pipe Open Driver, which allows
    a user to execute a program and treat it as a transport driver by
    routing data through pipes.
    """

    homepage = "https://github.com/gridcf/gct/blob/master/xio/drivers/popen/source"
    url = "https://repo.gridcf.org/gct6/sources/globus_xio_popen_driver-4.1.tar.gz"

    maintainers("github_user1", "github_user2")

    license("Apache-2.0", checked_by="wdconinc")

    version("4.1", sha256="6e9875c0d279511d8c476f71a46346712512284ade0623cd780c4e504908c110")

    depends_on("c", type="build")

    depends_on("globus-common@14:")
    depends_on("globus-xio@3:")
