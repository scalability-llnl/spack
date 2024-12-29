# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Hermes(CMakePackage):
    """
    Hermes is a heterogeneous-aware, multi-tiered, dynamic, and distributed
    I/O buffering system that aims to significantly accelerate I/O performance.
    """

    homepage = "https://grc.iit.edu/research/projects/hermes"
    git = "https://github.com/HDFGroup/hermes.git"

    maintainers("lukemartinlogan", "hyoklee")

    version("master", branch="master", submodules=True)

    version(
        "1.2.1",
        url="https://github.com/HDFGroup/hermes/archive/refs/tags/v1.2.1.tar.gz",
        sha256="d60ee5d6856dc1a1f389fb08f61252cc7736d1c38d3049043749640897fe3b6d",
    )
    version(
        "0.9.0-beta",
        url="https://github.com/HDFGroup/hermes/archive/refs/tags/v0.9.0-beta.tar.gz",
        sha256="abf258a52fa79729dfeb28559957abf8945f3ad37cadefb3bc685227c5f057a8",
    )

    variant("adios", default=False, description="Build Adios tests")
    variant("ares", default=False, description="Enable full libfabric install")
    variant("compress", default=False, description="Enable compression")
    variant("encrypt", default=False, description="Enable encryption")
    variant("mpiio", default=True, description="Enable MPI I/O adapter")
    # Builds with hermes@master. 1.2.1, we'd need to extract pybind11 source in external/pybind11:
    variant("python", default=False, description="Build Python Wrapper", when="@master")
    variant("stdio", default=True, description="Enable STDIO adapter")
    variant("vfd", default=False, description="Enable HDF5 VFD")
    variant("zmq", default=False, description="Build ZeroMQ tests")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("libelf")

    depends_on("hermes-shm@master+boost+cereal+mochi")

    depends_on("hermes-shm+adios", when="+adios")
    depends_on("hermes-shm+ares", when="+ares")
    depends_on("hermes-shm+compress", when="+compress")
    depends_on("hermes-shm+encrypt", when="+encrypt")
    depends_on("hermes-shm+mpiio", when="+mpiio")
    depends_on("hermes-shm+vfd", when="+vfd")
    depends_on("hermes-shm+zmq", when="+zmq")

    depends_on("py-jarvis-util", type="test")

    depends_on("mpi", when="+mpiio")
    conflicts("^[virtuals=mpi] nvhpc", when="+mpiio", msg="+mpio does not support nvhpc MPI")

    def cmake_args(self):
        args = []
        if "+mpiio" in self.spec:
            args.append("-DHERMES_ENABLE_MPIIO_ADAPTER=ON")
            mpi_name = self.spec["mpi"].name
            if mpi_name == "openmpi":
                args.append("-DHERMES_OPENMPI=ON")
            elif mpi_name == "mpich":
                args.append("-DHERMES_MPICH=ON")
            else:
                raise InstallError("hermes+mpiio needs openmpi or mpich, got " + mpi_name)
        if "+stdio" in self.spec:
            args.append("-DHERMES_ENABLE_STDIO_ADAPTER=ON")
        if "+vfd" in self.spec:
            args.append("-DHERMES_ENABLE_VFD=ON")
        if "+compress" in self.spec:
            args.append(self.define("HERMES_ENABLE_COMPRESSION", "ON"))
        if "+encrypt" in self.spec:
            args.append(self.define("HERMES_ENABLE_ENCRYPTION", "ON"))
        if "+adios" in self.spec:
            args.append(self.define("HERMES_ENABLE_ADIOS", "ON"))
        if "+python" in self.spec:
            args.append(self.define("HERMES_ENABLE_PYTHON", "ON"))
        return args

    def set_include(self, env, path):
        env.append_flags("CFLAGS", "-I{}".format(path))
        env.append_flags("CXXFLAGS", "-I{}".format(path))
        env.prepend_path("INCLUDE", "{}".format(path))
        env.prepend_path("CPATH", "{}".format(path))

    def set_lib(self, env, path):
        env.prepend_path("LIBRARY_PATH", path)
        env.prepend_path("LD_LIBRARY_PATH", path)
        env.append_flags("LDFLAGS", "-L{}".format(path))
        env.prepend_path("PYTHONPATH", "{}".format(path))

    def set_flags(self, env):
        self.set_include(env, "{}/include".format(self.prefix))
        self.set_include(env, "{}/include".format(self.prefix))
        self.set_lib(env, "{}/lib".format(self.prefix))
        self.set_lib(env, "{}/lib64".format(self.prefix))
        env.prepend_path("CMAKE_PREFIX_PATH", "{}/cmake".format(self.prefix))
        env.prepend_path("CMAKE_MODULE_PATH", "{}/cmake".format(self.prefix))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        self.set_flags(spack_env)

    def setup_run_environment(self, env):
        self.set_flags(env)
