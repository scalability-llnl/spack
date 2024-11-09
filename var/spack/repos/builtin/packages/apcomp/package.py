# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import socket

import llnl.util.tty as tty

from spack.build_systems.cmake import CMakeBuilder
from spack.package import *


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


class Apcomp(Package):
    """A multi use-case image compositor"""

    homepage = "https://github.com/Alpine-DAV/ap_compositor"
    git = "https://github.com/Alpine-DAV/ap_compositor.git"
    url = (
        "https://github.com/Alpine-DAV/ap_compositor/releases/download/v0.0.1/apcomp-v0.0.1.tar.gz"
    )

    maintainers("cyrush")

    with default_args(deprecated=True):  # part of ascent
        version("master", branch="master", submodules="True")
        version("0.0.4", sha256="061876dd55e443de91a40d10662496f6bb58b0a3835aec78f5710f5a737d0494")
        version("0.0.3", sha256="07e8c1d6a23205f4cc66d0a030e65a69e8344545f4d56213d968b67a410adc6e")
        version("0.0.2", sha256="cb2e2c4524889408de2dd3d29665512c99763db13e6f5e35c3b55e52948c649c")
        version("0.0.1", sha256="cbf85fe58d5d5bc2f468d081386cc8b79861046b3bb7e966edfa3f8e95b998b2")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("openmp", default=True, description="Build with openmp support")
    variant("mpi", default=True, description="Build with MPI support")
    variant("shared", default=True, description="Build Shared Library")
    # set to false for systems that implicitly link mpi
    variant("blt_find_mpi", default=True, description="Use BLT CMake Find MPI logic")

    depends_on("cmake@3.9:", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("llvm-openmp", when="+openmp %apple-clang")

    root_cmakelists_dir = "src"

    def install(self, spec, prefix):
        """
        Build and install APComp
        """
        with working_dir("spack-build", create=True):
            host_cfg_fname = self.create_host_config(spec, prefix)
            print("Configuring APComp...")
            cmake(*CMakeBuilder.std_args(self), "-C", host_cfg_fname, "../src")
            print("Building APComp...")
            make()
            print("Installing APComp...")
            make("install")
            # install copy of host config for provenance
            install(host_cfg_fname, prefix)

    def create_host_config(self, spec, prefix):
        """
        This method creates a 'host-config' file that specifies
        all of the options used to configure and build apcomp.
        """

        #######################
        # Compiler Info
        #######################
        c_compiler = env["SPACK_CC"]
        cpp_compiler = env["SPACK_CXX"]

        #######################################################################
        # We directly fetch the names of the actual compilers to create a
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

        host_cfg_fname = "%s-%s-%s-apcomp.cmake" % (socket.gethostname(), sys_type, spec.compiler)

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

        # shared vs static libs
        if spec.satisfies("+shared"):
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "ON"))
        else:
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "OFF"))

        if spec.satisfies("+openmp"):
            cfg.write(cmake_cache_entry("ENABLE_OPENMP", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_OPENMP", "OFF"))

        if spec.satisfies("+mpi"):
            mpicc_path = spec["mpi"].mpicc
            mpicxx_path = spec["mpi"].mpicxx
            # if we are using compiler wrappers on cray systems
            # use those for mpi wrappers, b/c  spec['mpi'].mpicxx
            # etc make return the spack compiler wrappers
            # which can trip up mpi detection in CMake 3.14
            if cpp_compiler == "CC":
                mpicc_path = "cc"
                mpicxx_path = "CC"
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

        cfg.write("##################################\n")
        cfg.write("# end spack generated host-config\n")
        cfg.write("##################################\n")
        cfg.close()

        host_cfg_fname = os.path.abspath(host_cfg_fname)
        tty.info("spack generated conduit host-config file: " + host_cfg_fname)
        return host_cfg_fname
