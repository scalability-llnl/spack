# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libecpint(CMakePackage):
    """A C++ library for the efficient evaluation of integrals over effective core
    potentials.
    """

    homepage = "https://github.com/robashaw/libecpint"
    url = "https://github.com/robashaw/libecpint/archive/v1.0.4.tar.gz"
    git = "https://github.com/robashaw/libecpint"

    license("MIT")

    version("master", branch="master")
    version("1.0.7", sha256="e9c60fddb2614f113ab59ec620799d961db73979845e6e637c4a6fb72aee51cc")
    version("1.0.5", sha256="3ad5ff342b1bc870f5992c296e8bd8aa590c21a9b14333958c601f8916d6f532")
    version("1.0.4", sha256="fad9d1ac98f8dcd40f7bee69aef653bfa3079f016e43277cbd554e06890aa186")
    version("1.0.3", sha256="13c3f7d1cf35355e37a903196d5cace60f6a72ae041e8b3502dfabdd19dde17a")
    version("1.0.2", sha256="2fb73af4d30a40bdd9df9e04b1f762c38ab7ed3a39c11509f3f87250fe0b5778")
    version("1.0.1", sha256="245b89fe8cb0a92cbbb79c811b48cb15fcfc937389df89387466f1bf76a096bf")
    version("1.0.0", sha256="47d741cc48a543ef9c85483cb2d5cd1c9f6677fa7e9920886d083b3c25232379")

    depends_on("cxx", type="build")  # generated

    depends_on("pugixml")
    depends_on("googletest")

    def cmake_args(self):
        args = ["-DBUILD_SHARED_LIBS=ON"]
        return args
