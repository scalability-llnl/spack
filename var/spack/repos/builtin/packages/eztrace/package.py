# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import autotools, cmake
from spack.package import *


class Eztrace(CMakePackage, AutotoolsPackage, CudaPackage):
    """EZTrace is a tool to automatically generate execution traces of HPC applications."""

    homepage = "https://gitlab.com/eztrace"
    git = "https://gitlab.com/eztrace/eztrace.git"

    maintainers("trahay")
    license("CECILL-B")

    version("master", branch="master")
    version("2.1", sha256="ab5076086eced78e4c6cf7736e7765ca1337dec95a881c9270a42b3251aeea19")
    version("2.0", sha256="67bd296f059cdfab303c62f674af3e1e858213d6945bd79cb8ede4a035c0c2d6")
    version("1.1-13", sha256="6144d04fb62b3ccad41af0268cd921161f168d0cca3f6c210c448bb0b07be7e0")
    version("1.1-10", sha256="63d1af2db38b04efa817614574f381e7536e12db06a2c75375d1795adda3d1d8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("starpu", default=False, description="Enable StarPU support", when="@2.1:")
    variant("netcdf", default=False, description="Enable NetCDF support", when="@2.1:")
    variant("pnetcdf", default=False, description="Enable PNetCDF support", when="@2.1:")

    build_system(
        conditional("cmake", when="@2:"), conditional("autotools", when="@:1"), default="cmake"
    )

    depends_on("mpi")
    depends_on("opari2")
    depends_on("binutils")
    depends_on("otf2", when="@2:")

    with when("build_system=autotools"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("libtool", type="build")

    with when("build_system=cmake"):
        depends_on("cmake@3.1:", type="build")

    depends_on("starpu", when="+starpu")
    depends_on("cuda", when="+cuda")
    depends_on("netcdf-c", when="+netcdf")
    depends_on("parallel-netcdf", when="+pnetcdf")

    patch(
        "https://gitlab.com/eztrace/eztrace/-/commit/3aafa74b12bc2c7e0687f2dbcfc35a699487eb10.diff",
        sha256="45321b0fd15db84840280c34a91ab877d0ceec6eb825f699f08a7bd135be3d79",
        when="@:1",
    )

    # Does not work on Darwin due to MAP_POPULATE
    conflicts("platform=darwin", when="@:1")

    # CUDA support from 2.1
    conflicts("+cuda", when="@:2.0")

    def url_for_version(self, version):
        return f"https://gitlab.com/eztrace/eztrace/-/archive/{version}/eztrace-{version}.tar.gz"

    @when("@:1")
    def patch(self):
        filter_file(
            '"DEFAULT_OUTFILE"',
            '" DEFAULT_OUTFILE "',
            "extlib/gtg/extlib/otf/tools/otfshrink/otfshrink.cpp",
            string=True,
        )


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        spec = self.spec
        args = [
            self.define("EZTRACE_ENABLE_MEMORY", True),
            self.define("EZTRACE_ENABLE_MPI", True),
            self.define("EZTRACE_ENABLE_OPENMP", True),
            self.define("EZTRACE_ENABLE_POSIXIO", True),
            self.define("EZTRACE_ENABLE_PTHREAD", True),
            self.define("OTF2_INCLUDE_PATH", spec["otf2"].prefix.include),
            self.define("OTF2_LIBRARY_PATH", spec["otf2"].libs),
        ]

        if spec.satisfies("@2.1: %llvm-openmp-ompt"):
            args.append(self.define("EZTRACE_ENABLE_OMPT", True))
        if spec.satisfies("+starpu"):
            args.append(self.define("EZTRACE_ENABLE_STARPU", True))
        if spec.satisfies("+cuda"):
            args.append(self.define("EZTRACE_ENABLE_CUDA", True))
        if spec.satisfies("+netcdf"):
            args.append(self.define("EZTRACE_ENABLE_NETCDF", True))
        if spec.satisfies("+pnetcdf"):
            args.append(self.define("EZTRACE_ENABLE_PNETCDF", True))

        return args


class AutotoolsBuilder(autotools.AutotoolsBuilder):
    def setup_build_environment(self, env):
        env.set("LDFLAGS", "--linkfortran")

    def autoreconf(self, pkg, spec, prefix):
        Executable("/bin/sh")("./bootstrap")

    def configure_args(self):
        return [f"--with-mpi={self.spec['mpi'].prefix}"]
