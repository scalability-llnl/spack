# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gsibec(CMakePackage):
    """GSIbec: Extracts the background error covariance (BEC) model
    capabilities from the Gridpoint Statistical Interpolation (GSI)
    atmospheric analysis system into a library of its own."""

    homepage = "https://github.com/GEOS-ESM/gsibec"
    git = "https://github.com/GEOS-ESM/gsibec.git"
    url = "https://github.com/GEOS-ESM/gsibec/archive/refs/tags/1.0.2.tar.gz"

    maintainers("mathomp4", "danholdaway")

    license("Apache-2.0")

    version("develop", branch="develop")
    version("1.2.1", sha256="83bf12ad6603d66e2e48b50cfcb57b7acd64e0d428a597a842db978a3277baf6")
    version("1.1.3", sha256="9cac000562250487c16608e8245d97457cc1663b1793b3833be5a76ebccb4b47")
    version("1.1.2", sha256="8bdcdf1663e6071b6ad9e893a76307abc70a6de744fb75a13986e70242993ada")
    version("1.0.7", sha256="53912f1f19d46f4941b377803cc2fce89a2b50d2ece7562f8fd65215a8908158")
    version("1.0.6", sha256="10e2561685156bcfba35c7799732c77f9c05bd180888506a339540777db833dd")
    version("1.0.5", sha256="ac0cecc59e38da7eefb5a8f27975b33752fa61a4abd3bdbbfb55578ea59d95b3")
    version("1.0.4", sha256="6460e221f2a45640adab016336c070fbe3e7c4b6fc55257945bf5cdb38d5d3e2")
    version("1.0.3", sha256="f104daf55705c5093a3d984073f082017bc9166f51ded36c7f7bb8adf233c916")
    version("1.0.2", sha256="7dc02f1f499e0d9f2843440f517d6c8e5d10ea084cbb2567ec198ba06816bc8b")

    depends_on("fortran", type="build")  # generated

    depends_on("mpi", type=("build", "run"))
    depends_on("netcdf-c +mpi", type=("build", "run"))
    depends_on("netcdf-fortran", type=("build", "run"))

    depends_on("lapack", type=("build", "run"))

    depends_on("ecbuild", type=("build"))
    depends_on("jedi-cmake", type=("build"))
    depends_on("sp", type=("build"))

    def cmake_args(self):
        args = []

        mkl_providers = ["intel-mkl", "intel-oneapi-mkl", "intel-parallel-studio"]
        args.append(self.define("ENABLE_MKL", self.spec["lapack"].name in mkl_providers))

        return args
