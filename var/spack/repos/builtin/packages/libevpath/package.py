# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libevpath(CMakePackage):
    """EVpath is an event transport middleware layer designed to allow
    for the easy implementation of overlay networks, with
    active data processing, routing and management at all points
    in the overlay. EVPath is designed for high performance systems.
    """

    homepage = "https://github.com/GTkorvo/evpath"
    url = "https://github.com/GTkorvo/evpath/archive/v4.1.1.tar.gz"
    git = "https://github.com/GTkorvo/evpath.git"

    version("develop", branch="master")
    version("4.4.0", sha256="c8d20d33c84d8d826493f453760eceb792d601734ff61238662c16fa6243dc29")
    version("4.2.4", sha256="070698a068798e2e34dd73debb936cf275af23987a4cb0d06aa3e50c481042ff")
    version("4.2.1", sha256="c745946f2ecff65bfc80978c2038c37c3803076064cfd29ea3023d671c950770")
    version("4.1.2", sha256="2c0d5acc0e1c5aadd32d7147d2f0ce26220e3870e21c7d5429372d8f881e519e")
    version("4.1.1", sha256="cfc9587f98c1f057eb25712855d14311fd91d6284151eee7bd8936c4ff7ee001")

    depends_on("c", type="build")  # generated

    variant("enet_transport", default=False, description="Build an ENET transport for EVpath")

    depends_on("gtkorvo-enet", when="@4.4.0: +enet_transport")
    depends_on("gtkorvo-enet@1.3.13", when="@:4.2.4 +enet_transport")
    depends_on("libffs")

    def cmake_args(self):
        args = ["-DTARGET_CNL=1"]
        if self.spec.satisfies("@4.4.0:"):
            args.append("-DBUILD_SHARED_LIBS=OFF")
        else:
            args.append("-DENABLE_BUILD_STATIC=STATIC")

        if self.run_tests:
            args.append("-DENABLE_TESTING=1")
        else:
            args.append("-DENABLE_TESTING=0")

        return args
