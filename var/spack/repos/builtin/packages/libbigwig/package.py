# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libbigwig(CMakePackage):
    """A C library for reading/parsing local and remote bigWig and bigBed files."""

    homepage = "https://github.com/dpryan79/libBigWig"
    url = "https://github.com/dpryan79/libBigWig/archive/refs/tags/0.4.7.tar.gz"
    maintainers("snehring")

    license("MIT")

    version("0.4.7", sha256="8e057797011d93fa00e756600898af4fe6ca2d48959236efc9f296abe94916d9")

    depends_on("c", type="build")  # generated

    variant("curl", default=True, description="Build with curl support")

    depends_on("curl", when="+curl")

    def cmake_args(self):
        args = []
        if self.spec.satisfies("~curl"):
            args.append("-DWITH_CURL=OFF")
        return args
