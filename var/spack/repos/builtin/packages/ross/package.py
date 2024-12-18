# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ross(CMakePackage):
    """Rensselaer Optimistic Simulation System"""

    homepage = "https://ross-org.github.io"
    git = "https://github.com/ROSS-org/ROSS.git"
    url = "https://github.com/ROSS-org/ROSS/archive/v7.0.0.tar.gz"

    license("BSD-3-Clause")

    version("develop", branch="develop")
    version("master", branch="master")
    version("8.0.0", sha256="5339c9afcf77821fb6ebbcd93b8a1e651c7883e94dff250528815a08f84f1694")
    version("7.2.0", sha256="c937f4c7baa1918b6cd08f4eafae8cab44eddcd4aaa1175c23ff8562583ad726")
    version("7.1.1", sha256="550e3288cefedcbc7e6ca16cfbee0477b70399d63e94f554b60b32d714029722")
    version("7.1.0", sha256="478063f36d96466faef3db3cc15e1c0e1a8b60b9152fcce0eedf367be8252733")
    version("7.0.1", sha256="40780dada4ab501d2b8ea229f70b9fea920404431d7a60081ba84dd4a50b2517")
    version("7.0.0", sha256="fd16be2c86d9d71ae64eef67c02933471ab758c8a5b01b04fe358d9228fc581e")
    version("6.0.0", sha256="07ff70518a58503e116bb7386f490e901212798afdd471da1bcd34f78a7e6030")

    depends_on("c", type="build")  # generated

    depends_on("mpi")
    depends_on("cmake@3.5:", when="@7.0.1:", type="build")

    @when("@:7.0.0")
    def cmake_args(self):
        args = []

        args.append("-DBUILD_SHARED_LIBS=ON")
        args.append(f"-DARCH={self.spec.target}")
        args.append(f"-DCMAKE_C_COMPILER={self.spec['mpi'].mpicc}")
        args.append(f"-DCMAKE_CXX_COMPILER={self.spec['mpi'].mpicxx}")

        return args
