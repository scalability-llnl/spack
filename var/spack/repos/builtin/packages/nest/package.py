# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nest(CMakePackage):
    """NEST is a simulator for spiking neural network models

    It focuses on the dynamics, size and structure of neural systems rather
    than on the exact morphology of individual neurons."""

    homepage = "https://www.nest-simulator.org"
    url = "https://github.com/nest/nest-simulator/archive/refs/tags/v3.0.tar.gz"
    git = "https://github.com/nest/nest-simulator.git"

    license("GPL-2.0-or-later")

    version("master", branch="master")
    version("3.0", sha256="d481ea67f3251fe3aadf5252ab0a999172f0cd5536c5985366d271d772e686e6")
    version("2.20.1", sha256="df3d32b5899d5d444f708037b290f889ac6ff8eae6b7be9e9faee2c0d660d8e5")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    maintainers("ikitayama")

    variant("python", default=False, description="Build the PyNest interface")
    variant("mpi", default=False, description="Build with MPI bindings")
    variant("openmp", default=True, description='"Enable OpenMP support"')
    variant("optimize", default=True, description="Build with MPI bindings")
    variant("modules", default=False, description="Enables external module support")
    variant("gsl", default=True, description="Enable GNU Scientific Library")
    variant("shared", default=True, description="Build shared libraries")
    # TODO add variants for neurosim and music when these are in spack

    conflicts("~gsl", when="@:2.10", msg="Option only introduced for non-ancient versions.")
    conflicts("~shared", when="@:2.10", msg="Option only introduced for non-ancient versions.")
    conflicts("~openmp", when="@:2.10", msg="Option only introduced for non-ancient versions.")

    depends_on("python@2.6:", when="+python", type=("build", "run"))
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-scipy", when="+python", type=("run"))
    depends_on("py-cython@0.19.2:", when="+python", type="build")
    depends_on("py-nose", when="+python", type="test")
    depends_on("py-setuptools", when="+python", type="build")

    depends_on("mpi", when="+mpi")

    depends_on("doxygen", type="build")

    depends_on("gsl", when="+gsl")
    depends_on("readline")
    depends_on("libtool", type="link")  # links against libltdl
    depends_on("pkgconfig", type="build")

    extends("python", when="+python")

    # Before 2.12.0 it was an autotools package
    @when("@:2.10")
    def cmake(self, spec, prefix):
        pass

    @when("@:2.10")
    def build(self, spec, prefix):
        pass

    @when("@:2.10")
    def install(self, spec, prefix):
        configure_args = ["CXXFLAGS=-std=c++03", "--prefix=" + prefix, "--with-openmp"]
        if "+python" in spec:
            configure_args.append("--with-python")
        else:
            configure_args.append("--without-python")
        if "+mpi" in spec:
            configure_args.append("--with-mpi")
        else:
            configure_args.append("--without-mpi")
        if "+optimize" in spec:
            configure_args.append("--with-optimize")
        else:
            configure_args.append("--without-optimize")

        configure(*configure_args)

        make()
        make("install")

    def cmake_args(self):
        args = []

        if "+mpi" in self.spec:
            args.append("-Dwith-mpi=ON")
        else:
            args.append("-Dwith-mpi=OFF")

        if "+python" in self.spec:
            args.append("-Dwith-python=ON")
            args.append("-Dcythonize-pynest=" + self.spec["py-cython"].prefix)
        else:
            args.append("-Dwith-python=OFF")
            args.append("-Dcythonize-pynest=OFF")

        if "+optimize" in self.spec:
            args.append("-Dwith-optimize=ON")
        else:
            args.append("-Dwith-optimize=OFF")

        if "+gsl" in self.spec:
            args.append("-Dwith-gsl=" + self.spec["gsl"].prefix)
        else:
            args.append("-Dwith-gsl=OFF")

        if "+openmp" in self.spec:
            args.append("-Dwith-openmp=ON")
        else:
            args.append("-Dwith-openmp=OFF")

        if "+shared" in self.spec:
            args.append("-Dstatic-libraries=OFF")
        else:
            args.append("-Dstatic-libraries=ON")

        return args

    @when("@:2.14.0+modules")
    @run_after("install")
    def install_headers(self):
        # copy source files to installation folder for older versions
        # (these are needed for modules to build against)
        # see https://github.com/nest/nest-simulator/pull/844
        path_headers = join_path(prefix, "include", "nest")

        mkdirp(path_headers)

        for suffix in ["h", "hpp"]:
            for f in find_headers("*.{0}".format(suffix), self.stage.source_path, recursive=True):
                install(f, path_headers)

    def setup_run_environment(self, env):
        env.set("NEST_INSTALL_DIR", self.spec.prefix)
