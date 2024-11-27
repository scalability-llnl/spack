# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XcbUtilXrm(AutotoolsPackage):
    """XCB util-xrm module provides the 'xrm' library, i.e.  utility functions
    for the X resource manager."""

    homepage = "https://github.com/Airblader/xcb-util-xrm"
    git = "https://github.com/Airblader/xcb-util-xrm.git"

    license("MIT")

    # This GitHub project includes some git submodules, which must be fetched
    # in order to build it.
    version("1.2", tag="v1.2", commit="a45b3d0bbaa94bf8a68405ab8c5c61404da464ce", submodules=True)

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("libxcb@1.4:")
