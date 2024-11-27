# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenmc(PythonPackage):
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

    version("develop", branch="develop")
    version("master", branch="master")
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

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=False, description="Enable MPI support")

    # keep py-openmc and openmc at the same version
    for ver in [
        "develop",
        "master",
        "0.15.0",
        "0.14.0",
        "0.13.3",
        "0.13.2",
        "0.13.1",
        "0.13.0",
        "0.12.2",
        "0.12.1",
        "0.12.0",
        "0.11.0",
    ]:
        depends_on(
            "openmc+mpi@{0}".format(ver), when="@{0}+mpi".format(ver), type=("build", "run")
        )
        depends_on(
            "openmc~mpi@{0}".format(ver), when="@{0}~mpi".format(ver), type=("build", "run")
        )

    depends_on("git", type="build")
    depends_on("python@3.10:", type=("build", "run"), when="@0.15.0:")
    depends_on("python@3.7:", type=("build", "run"), when="@0.13.2:0.14.0")
    depends_on("python@3.6:", type=("build", "run"), when="@0.13.0:0.13.1")
    depends_on("python@3.5:", type=("build", "run"), when="@:0.12")
    depends_on("py-cython", type="build")
    depends_on("py-h5py~mpi", when="~mpi", type=("build", "run"))
    depends_on("py-h5py+mpi", when="+mpi", type=("build", "run"))
    depends_on("py-ipython", type=("build", "run"))
    depends_on("py-lxml", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-mpi4py", when="+mpi", type=("build", "run"))
    depends_on("py-numpy@1.9:1.21", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-uncertainties", type=("build", "run"))

    @run_after("install")
    def install_lib(self):
        install(join_path(self.spec["openmc"].prefix.lib, "libopenmc.*"), self.prefix.lib)
