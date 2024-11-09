# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Openmc(CMakePackage):
    """OpenMC is a community-developed Monte Carlo neutron and photon transport
    simulation code. It is capable of performing fixed source, k-eigenvalue, and
    subcritical multiplication calculations on models built using either a
    constructive solid geometry or CAD representation. OpenMC supports both
    continuous-energy and multigroup transport. The continuous-energy particle
    interaction data is based on a native HDF5 format that can be generated from ACE
    files produced by NJOY. Parallelism is enabled via a hybrid MPI and OpenMP
    programming model."""

    homepage = "https://docs.openmc.org/"
    url = "https://github.com/openmc-dev/openmc/tarball/v0.15.0"
    git = "https://github.com/openmc-dev/openmc.git"
    maintainers("paulromano")

    version("develop", branch="develop", submodules=True)
    version("master", branch="master", submodules=True)
    version("0.15.0", commit="55b52b7ef3c9415ce045712132bf31c2a013d8c8", submodules=True)
    version("0.14.0", commit="fa2330103de61a864c958d1a7250f11e5dd91468", submodules=True)
    version("0.13.3", commit="27cb0dc97960fe6d750eb5a93584a9a0ca532ac8", submodules=True)
    version("0.13.2", commit="030f73a8690ed19e91806e46c8caf338d252e74a", submodules=True)
    version("0.13.1", commit="33bc948f4b855c037975f16d16091fe4ecd12de3", submodules=True)
    version("0.13.0", commit="cff247e35785e7236d67ccf64a3401f0fc50a469", submodules=True)
    version("0.12.2", commit="cbfcf908f8abdc1ef6603f67872dcf64c5c657b1", submodules=True)
    version("0.12.1", commit="36913589c4f43b7f843332181645241f0f10ae9e", submodules=True)
    version("0.12.0", commit="93d6165ecb455fc57242cd03a3f0805089c0e0b9", submodules=True)
    version("0.11.0", sha256="19a9d8e9c3b581e9060fbd96d30f1098312d217cb5c925eb6372a5786d9175af")
    version("0.10.0", sha256="47650cb45e2c326ae439208d6f137d75ad3e5c657055912d989592c6e216178f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=False, description="Enable MPI support")
    variant("openmp", default=True, description="Enable OpenMP support")

    depends_on("git", type="build")
    depends_on("hdf5+hl~mpi", when="~mpi")
    depends_on("mpi", when="+mpi")
    depends_on("hdf5+hl+mpi", when="+mpi")

    def cmake_args(self):
        options = ["-DCMAKE_INSTALL_LIBDIR=lib"]  # forcing bc sometimes goes to lib64

        use_newer_options = self.spec.satisfies("@0.13.1:")
        if "+mpi" in self.spec:
            options += [
                "-DCMAKE_C_COMPILER=%s" % self.spec["mpi"].mpicc,
                "-DCMAKE_CXX_COMPILER=%s" % self.spec["mpi"].mpicxx,
            ]
            if use_newer_options:
                options += [self.define("OPENMC_USE_MPI", True)]

        if use_newer_options:
            options += [self.define_from_variant("OPENMC_USE_OPENMP", "openmp")]
        else:
            options += [self.define_from_variant("openmp")]

        return options
