# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CAres(CMakePackage):
    """c-ares: A C library for asynchronous DNS requests"""

    homepage = "https://c-ares.haxx.se"
    url = "https://github.com/c-ares/c-ares/archive/cares-1_15_0.tar.gz"
    git = "https://github.com/c-ares/c-ares.git"

    license("MIT")

    version("master", branch="master")
    version("1.28.1", sha256="e520d971415e48e607819c2f4b377b0aa69044ef6619160bb41bdba15ab4d545")
    version("1.27.0", sha256="de6a839d47b93174ba260187a084027ea681a91ffe12f2d5f20645652eae246c")
    version("1.15.0", sha256="7deb7872cbd876c29036d5f37e30c4cbc3cc068d59d8b749ef85bb0736649f04")
    version("1.13.0", sha256="7c48c57706a38691041920e705d2a04426ad9c68d40edd600685323f214b2d57")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        url = "https://github.com/c-ares/c-ares/archive/cares-{0}.tar.gz"
        return url.format(version.underscored)

    @property
    def libs(self):
        return find_libraries(["libcares"], root=self.prefix, recursive=True)
