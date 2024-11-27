# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ftk(CMakePackage):
    """FTK is a library that simplifies, scales, and delivers feature
    tracking algorithms for scientific data."""

    # Add a proper url for your package's homepage here.
    homepage = "https://github.com/hguo/ftk"
    url = "https://github.com/hguo/ftk/archive/0.0.7.1.tar.gz"
    git = "https://github.com/hguo/ftk.git"

    # Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers("hguo")

    license("MIT")

    version("master", branch="master")
    version("dev", branch="dev")
    version("0.0.7.1", sha256="6090fd436f971316062dbb4fcbf2c44603ed5c29341df8f2b80b85770a3bcda2")
    version("0.0.6", sha256="876839c62c78dddf48ee1f15681401db266e9537b76075e23fea31874e65935c")
    version("0.0.5.1", sha256="5f7d1931d902a3f48d5c15a3b3e6dc6038b880ac869930b44ca9e196148804e8")
    version("0.0.5", sha256="9d5c84a73b7761b9fc7dac62d4296df9f3052b722ec1b06518b2b8f51a8d3440")
    version("0.0.4", sha256="1674904da8d88dbd4c7d2b6a2629883f0444e70aefc99b48d285735d394897fa")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # variants
    variant("adios2", default=False, description="Use ADIOS2")
    variant("cuda", default=False, description="Use CUDA")
    variant("gmp", default=False, description="Use GMP")
    variant("hdf5", default=False, description="Use HDF5")
    variant("metis", default=False, description="Use METIS")
    variant("mpi", default=False, description="Use MPI")
    variant("netcdf", default=False, description="Use NetCDF")
    variant("vtk", default=False, description="Use VTK")

    # optional dependencies
    depends_on("adios2", when="+adios2")
    depends_on("cuda", when="+cuda")
    depends_on("hdf5", when="+hdf5")
    depends_on("gmp", when="+gmp")
    depends_on("metis", when="+metis")
    depends_on("metis", when="+mpi")
    depends_on("mpi", when="+mpi")
    depends_on("netcdf-c", when="+netcdf")
    depends_on("vtk", when="+vtk")

    def add_cmake_option(self, args, dependency, option):
        if dependency in self.spec:
            args.append("-D" + option + "=ON")
        else:
            args.append("-D" + option + "=OFF")

    def cmake_args(self):
        args = []

        self.add_cmake_option(args, "+adios2", "FTK_USE_ADIOS2")
        self.add_cmake_option(args, "+cuda", "FTK_USE_CUDA")
        self.add_cmake_option(args, "+gmp", "FTK_USE_GMP")
        self.add_cmake_option(args, "+hdf5", "FTK_USE_HDF5")
        self.add_cmake_option(args, "+metis", "FTK_USE_METIS")
        self.add_cmake_option(args, "+mpi", "FTK_USE_MPI")
        self.add_cmake_option(args, "+netcdf", "FTK_USE_NETCDF")
        self.add_cmake_option(args, "+vtk", "FTK_USE_VTK")

        return args
