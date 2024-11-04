# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import socket

import llnl.util.tty as tty

from spack.build_systems.cmake import CMakeBuilder
from spack.package import *


def propagate_cuda_arch(package, spec=None):
    if not spec:
        spec = ""
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on(
            "{0} +cuda cuda_arch={1}".format(package, cuda_arch),
            when="{0} +cuda cuda_arch={1}".format(spec, cuda_arch),
        )


def cmake_cache_entry(name, value, vtype=None):
    """
    Helper that creates CMake cache entry strings used in
    'host-config' files.
    """
    if vtype is None:
        if value == "ON" or value == "OFF":
            vtype = "BOOL"
        else:
            vtype = "PATH"
    return 'set({0} "{1}" CACHE {2} "")\n\n'.format(name, value, vtype)


class Dray(Package, CudaPackage):
    """High-Order Mesh Ray Tracer."""

    homepage = "https://github.com/LLNL/devil_ray"
    git = "https://github.com/LLNL/devil_ray.git"
    url = "https://github.com/LLNL/devil_ray/releases/download/v0.1.2/dray-v0.1.2.tar.gz"

    maintainers("cyrush")

    license("BSD-3-Clause")

    with default_args(deprecated=True):  # part of ascent
        version("develop", branch="develop", submodules="True")
        version("0.1.8", sha256="ae78ca6a5a31f06f6400a4a1ff6fc1d75347c8b41027a80662179f5b877eee30")
        version("0.1.7", sha256="11ea794c1a24d7ed0d76bad7209d62bafc033ec40a2ea3a00e68fe598c6aa46d")
        version("0.1.6", sha256="43f39039599e3493cbbaeaf5621b611bef301ff504bed6e32c98f30bb2179e92")
        version("0.1.5", sha256="aaf0975561a8e7910b9353e2dc30bd78abf9f01c306ec042422b7da223d3a8b8")
        version("0.1.4", sha256="e763a3aa537b23486a4788f9d68db0a3eb545f6a2e617cd7c8a876682ca2d0a0")
        version("0.1.3", sha256="b2f624a072463189997343b1ed911cc34c9bb1b6c7f0c3e48efeb40c05dd0d92")
        version("0.1.2", sha256="46937f20124b28dc78a634e8e063a3e7a3bbfd9f424ce2680b08417010c376da")
        version("0.1.1", sha256="e5daa49ee3367c087f5028dc5a08655298beb318014c6f3f65ef4a08fcbe346c")
        version("0.1.0", sha256="8b341138e1069361351e0a94478608c5af479cca76e2f97d556229aed45c0169")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("openmp", default=True, description="Build OpenMP backend")
    variant("shared", default=True, description="Build as shared libs")
    variant("test", default=True, description="Build unit tests")
    variant("utils", default=True, description="Build utilities")
    variant("logging", default=False, description="Enable logging")
    variant("stats", default=False, description="Enable stats")
    variant("mpi", default=True, description="Enable MPI compiler")
    # set to false for systems that implicitly link mpi
    variant("blt_find_mpi", default=True, description="Use BLT CMake Find MPI logic")

    depends_on("mpi", when="+mpi")

    depends_on("cmake@3.9:", type="build")
    depends_on("cmake@3.14:", when="+cuda", type="build")

    depends_on("conduit~shared", when="~shared")
    depends_on("conduit+shared", when="+shared")

    depends_on("apcomp~mpi", when="~mpi")
    depends_on("apcomp+mpi", when="+mpi")
    depends_on("apcomp~openmp", when="~openmp")
    depends_on("apcomp+openmp", when="+openmp")
    depends_on("apcomp~shared", when="~shared")
    depends_on("apcomp+shared", when="+shared")

    depends_on("raja@0.14.0:0.14", when="@0.1.8:")
    depends_on("raja@:0.14", when="@0.1.7:")
    depends_on("raja@:0.13", when="@:0.1.6")
    depends_on("raja@0.12.0:")
    depends_on("raja~cuda", when="~cuda")
    depends_on("raja+cuda", when="+cuda")
    propagate_cuda_arch("raja")
    depends_on("raja~shared", when="~shared")
    depends_on("raja+shared", when="+shared")
    depends_on("raja~openmp", when="~openmp")
    depends_on("raja+openmp", when="+openmp")

    depends_on("umpire@:4.9", when="@:0.1.6")
    # Only use umpire cuda if not shared.
    depends_on("umpire+cuda", when="+cuda")
    depends_on("umpire~cuda", when="~cuda")
    depends_on("umpire+cuda~shared", when="+cuda+shared")
    depends_on("umpire~cuda+shared", when="~cuda+shared")
    propagate_cuda_arch("umpire")
    depends_on("umpire~shared", when="~shared")

    depends_on("mfem+conduit~threadsafe")
    depends_on("mfem+shared", when="+shared")
    depends_on("mfem~shared", when="~shared")

    def setup_build_environment(self, env):
        env.set("CTEST_OUTPUT_ON_FAILURE", "1")

    def install(self, spec, prefix):
        """
        Build and install Devil Ray.
        """
        with working_dir("spack-build", create=True):
            host_cfg_fname = self.create_host_config(spec, prefix)
            print("Configuring Devil Ray...")
            cmake(
                *CMakeBuilder.std_args(self, generator="Unix Makefiles"),
                "-C",
                host_cfg_fname,
                "../src",
            )
            print("Building Devil Ray...")
            make()
            # run unit tests if requested
            if "+test" in spec and self.run_tests:
                print("Running Devil Ray Unit Tests...")
                make("test")
            print("Installing Devil Ray...")
            make("install")
            # install copy of host config for provenance
            install(host_cfg_fname, prefix)

    def create_host_config(self, spec, prefix):
        """
        This method creates a 'host-config' file that specifies
        all of the options used to configure and build ascent.

        For more details about 'host-config' files see:
            https://ascent.readthedocs.io/en/latest/BuildingAscent.html
        """

        #######################
        # Compiler Info
        #######################
        c_compiler = env["SPACK_CC"]
        cpp_compiler = env["SPACK_CXX"]

        #######################################################################
        # By directly fetching the names of the actual compilers we appear
        # to doing something evil here, but this is necessary to create a
        # 'host config' file that works outside of the spack install env.
        #######################################################################

        sys_type = spec.architecture
        # if on llnl systems, we can use the SYS_TYPE
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]

        ##############################################
        # Find and record what CMake is used
        ##############################################

        if spec.satisfies("+cmake"):
            cmake_exe = spec["cmake"].command.path
        else:
            cmake_exe = which("cmake")
            if cmake_exe is None:
                msg = "failed to find CMake (and cmake variant is off)"
                raise RuntimeError(msg)
            cmake_exe = cmake_exe.path

        host_cfg_fname = "%s-%s-%s-devil_ray.cmake" % (
            socket.gethostname(),
            sys_type,
            spec.compiler,
        )

        cfg = open(host_cfg_fname, "w")
        cfg.write("##################################\n")
        cfg.write("# spack generated host-config\n")
        cfg.write("##################################\n")
        cfg.write("# {0}-{1}\n".format(sys_type, spec.compiler))
        cfg.write("##################################\n\n")

        # Include path to cmake for reference
        cfg.write("# cmake from spack \n")
        cfg.write("# cmake executable path: %s\n\n" % cmake_exe)

        #######################
        # Compiler Settings
        #######################
        cfg.write("#######\n")
        cfg.write("# using %s compiler spec\n" % spec.compiler)
        cfg.write("#######\n\n")
        cfg.write("# c compiler used by spack\n")
        cfg.write(cmake_cache_entry("CMAKE_C_COMPILER", c_compiler))
        cfg.write("# cpp compiler used by spack\n")
        cfg.write(cmake_cache_entry("CMAKE_CXX_COMPILER", cpp_compiler))

        if spec.satisfies("+mpi"):
            mpicc_path = spec["mpi"].mpicc
            mpicxx_path = spec["mpi"].mpicxx
            # if we are using compiler wrappers on cray systems
            # use those for mpi wrappers, b/c  spec['mpi'].mpicxx
            # etc make return the spack compiler wrappers
            # which can trip up mpi detection in CMake 3.14
            if spec["mpi"].mpicc == spack_cc:
                mpicc_path = c_compiler
                mpicxx_path = cpp_compiler
            cfg.write(cmake_cache_entry("ENABLE_MPI", "ON"))
            cfg.write(cmake_cache_entry("MPI_C_COMPILER", mpicc_path))
            cfg.write(cmake_cache_entry("MPI_CXX_COMPILER", mpicxx_path))
            if spec.satisfies("+blt_find_mpi"):
                cfg.write(cmake_cache_entry("ENABLE_FIND_MPI", "ON"))
            else:
                cfg.write(cmake_cache_entry("ENABLE_FIND_MPI", "OFF"))
            mpiexe_bin = join_path(spec["mpi"].prefix.bin, "mpiexec")
            if os.path.isfile(mpiexe_bin):
                # starting with cmake 3.10, FindMPI expects MPIEXEC_EXECUTABLE
                # vs the older versions which expect MPIEXEC
                if self.spec["cmake"].satisfies("@3.10:"):
                    cfg.write(cmake_cache_entry("MPIEXEC_EXECUTABLE", mpiexe_bin))
                else:
                    cfg.write(cmake_cache_entry("MPIEXEC", mpiexe_bin))
        else:
            cfg.write(cmake_cache_entry("ENABLE_MPI", "OFF"))

        # use global spack compiler flags
        cppflags = " ".join(spec.compiler_flags["cppflags"])
        if cppflags:
            # avoid always ending up with ' ' with no flags defined
            cppflags += " "
        cflags = cppflags + " ".join(spec.compiler_flags["cflags"])
        if cflags:
            cfg.write(cmake_cache_entry("CMAKE_C_FLAGS", cflags))
        cxxflags = cppflags + " ".join(spec.compiler_flags["cxxflags"])
        if cxxflags:
            cfg.write(cmake_cache_entry("CMAKE_CXX_FLAGS", cxxflags))
        fflags = " ".join(spec.compiler_flags["fflags"])
        if self.spec.satisfies("%cce"):
            fflags += " -ef"
        if fflags:
            cfg.write(cmake_cache_entry("CMAKE_Fortran_FLAGS", fflags))

        #######################
        # Backends
        #######################

        cfg.write("# CUDA Support\n")

        if spec.satisfies("+cuda"):
            cfg.write(cmake_cache_entry("ENABLE_CUDA", "ON"))
            if "cuda_arch" in spec.variants:
                cuda_value = spec.variants["cuda_arch"].value
                cuda_arch = cuda_value[0]
                cfg.write(cmake_cache_entry("CUDA_ARCH", "sm_{0}".format(cuda_arch)))
        else:
            cfg.write(cmake_cache_entry("ENABLE_CUDA", "OFF"))

        if spec.satisfies("+openmp"):
            cfg.write(cmake_cache_entry("ENABLE_OPENMP", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_OPENMP", "OFF"))

        # shared vs static libs
        if spec.satisfies("+shared"):
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "ON"))
        else:
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "OFF"))

        #######################
        # Unit Tests
        #######################
        if spec.satisfies("+test"):
            cfg.write(cmake_cache_entry("DRAY_ENABLE_TESTS", "ON"))
            # we need this to control BLT tests
            cfg.write(cmake_cache_entry("ENABLE_TESTS", "ON"))
        else:
            cfg.write(cmake_cache_entry("DRAY_ENABLE_TESTS", "OFF"))
            # we need this to control BLT tests
            cfg.write(cmake_cache_entry("ENABLE_TESTS", "OFF"))

        #######################
        # Utilities
        #######################
        if spec.satisfies("+utils"):
            cfg.write(cmake_cache_entry("DRAY_ENABLE_UTILS", "ON"))
        else:
            cfg.write(cmake_cache_entry("DRAY_ENABLE_UTILS", "OFF"))

        #######################
        # Logging
        #######################
        if spec.satisfies("+logging"):
            cfg.write(cmake_cache_entry("ENABLE_LOGGING", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_LOGGING", "OFF"))

        #######################
        # Status
        #######################
        if spec.satisfies("+stats"):
            cfg.write(cmake_cache_entry("ENABLE_STATS", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_STATS", "OFF"))

        #######################################################################
        # Core Dependencies
        #######################################################################

        cfg.write("# conduit from spack \n")
        cfg.write(cmake_cache_entry("CONDUIT_DIR", spec["conduit"].prefix))

        cfg.write("# mfem from spack \n")
        cfg.write(cmake_cache_entry("MFEM_DIR", spec["mfem"].prefix))

        cfg.write("# raja from spack \n")
        cfg.write(cmake_cache_entry("RAJA_DIR", spec["raja"].prefix))

        cfg.write("# umpire from spack \n")
        cfg.write(cmake_cache_entry("UMPIRE_DIR", spec["umpire"].prefix))

        cfg.write("# apcompositor from spack \n")
        cfg.write(cmake_cache_entry("APCOMP_DIR", spec["apcomp"].prefix))

        cfg.write("##################################\n")
        cfg.write("# end spack generated host-config\n")
        cfg.write("##################################\n")
        cfg.close()

        host_cfg_fname = os.path.abspath(host_cfg_fname)
        tty.info("spack generated conduit host-config file: " + host_cfg_fname)
        return host_cfg_fname
