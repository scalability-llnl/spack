# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mrcpp(CMakePackage):
    """The MultiResolution Computation Program Package (MRCPP) is a general purpose
    numerical mathematics library based on multiresolution analysis and the
    multiwavelet basis which provide low-scaling algorithms as well as rigorous
    error control in numerical computations."""

    homepage = "https://mrcpp.readthedocs.io/en/latest/"
    url = "https://github.com/MRChemSoft/mrcpp/archive/v1.3.6.tar.gz"

    maintainers("robertodr", "stigrj", "ilfreddy")

    license("LGPL-3.0-only")

    version("1.4.2", sha256="cc7a4200eb0383967d984e770a95e621e76c88b79c5e7443433f5e642aee035b")
    version("1.3.6", sha256="2502e71f086a8bb5ea635d0c6b86e7ff60220a45583e96a08b3cfe7c9db4cecf")
    version("1.3.5", sha256="3072cf60db6fa1e621bc6e6dfb6d35f9367a44d9d312a4b8c455894769140aed")
    version("1.3.4", sha256="fe6d1ad5804f605c7ba0da6831a8dc7fed72de6f2476b162961038aaa2321656")
    version("1.3.3", sha256="78c43161d0a4deffaf5d199e77535f6acbd88cc718ebc342d6ec9d72165c243e")
    version("1.3.2", sha256="61ffdfa36af37168090ba9d85550ca4072eb11ebfe3613da32e9c462351c9813")
    version("1.3.1", sha256="6ab05bc760c5d4f3f2925c87a0db8eab3417d959c747b27bac7a2fe5d3d6f7d1")
    version("1.3.0", sha256="74122ec2f2399472381df31f77ce0decbadd9d2f76e2aef6b07c815cc319ac52")
    version("1.2.0", sha256="faa6088ed20fb853bd0de4fe9cd578630d183f69e004601d4e464fe737e9f32d")
    version("1.1.0", sha256="e9ffb87eccbd45305f822a0b46b875788b70386b3c1d38add6540dc4e0327ab2")
    version("1.0.2", sha256="d2b26f7d7b16fa67f16788119abc0f6c7562cb37ece9ba075c116463dcf19df3")
    version("1.0.1", sha256="b4d7120545da3531bc7aa0a4cb4eb579fdbe1f8e5d32b1fd1086976583e3e27c")
    version("1.0.0", sha256="0858146141d3a60232e8874380390f9e9fa0b1bd6e67099d5833704478213efd")

    depends_on("cxx", type="build")  # generated

    variant("openmp", default=True, description="Enable OpenMP support.")

    variant("mpi", default=True, description="Enable MPI support")
    depends_on("mpi", when="+mpi")

    depends_on("cmake@3.11:", type="build")
    depends_on("eigen")

    def cmake_args(self):
        args = [
            "-DENABLE_OPENMP={0}".format("ON" if "+openmp" in self.spec else "OFF"),
            "-DENABLE_MPI={0}".format("ON" if "+mpi" in self.spec else "OFF"),
            "-DENABLE_TESTS=OFF",
        ]
        return args
