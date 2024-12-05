# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mrchem(CMakePackage):
    """MRChem is a numerical real-space code for molecular electronic structure
    calculations within the self-consistent field (SCF) approximations of
    quantum chemistry: Hartree-Fock and Density Functional Theory."""

    homepage = "https://mrchem.readthedocs.io/en/latest/"
    url = "https://github.com/MRChemSoft/mrchem/archive/v1.0.0.tar.gz"

    maintainers("robertodr", "stigrj", "ilfreddy")

    license("LGPL-3.0-only")

    version("1.1.2", sha256="b4e74ad5ee89fc5e8a7329474cf0fa93155423f93a1f95c8c2888f7c53e353ea")
    version("1.0.0", sha256="9cdda4d30b2baabb26400742f78ef8f3fc50a54f5218c8b6071b0cbfbed746c3")
    version("0.2.2", sha256="7519cc104c7df51eea8902c225aac6ecce2ac4ff30765145e502342d5bf3d96b")
    version("0.2.1", sha256="c1d0da5fefae356d9746f8ee761a94f6f6cd8b735a8309a4048ad6b8943ad242")
    version("0.2.0", sha256="eea223db8275f9f2ce09601088264ec952ce2557a7050466301f53070ab03b82")
    version("0.1.0", sha256="325fa45fe1918b4d394060f36d23432ab8139596ebc22b65b1284c1f673e8164")

    depends_on("cxx", type="build")  # generated

    variant("openmp", default=True, description="Enable OpenMP support.")

    variant("mpi", default=True, description="Enable MPI support")
    depends_on("mpi", when="+mpi")

    depends_on("cmake@3.12:", type="build")
    depends_on("eigen")
    depends_on("nlohmann-json")
    depends_on("xcfun")
    depends_on("mrcpp")

    def cmake_args(self):
        args = [
            "-DENABLE_OPENMP={0}".format("ON" if "+openmp" in self.spec else "OFF"),
            "-DENABLE_MPI={0}".format("ON" if "+mpi" in self.spec else "OFF"),
        ]
        return args
