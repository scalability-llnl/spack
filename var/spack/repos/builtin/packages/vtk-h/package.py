# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import socket
import sys
from os import environ as env

import llnl.util.tty as tty

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


class VtkH(CMakePackage, CudaPackage):
    """VTK-h is a toolkit of scientific visualization algorithms for emerging
    processor architectures. VTK-h brings together several projects like VTK-m
    and DIY2 to provide a toolkit with hybrid parallel capabilities."""

    homepage = "https://github.com/Alpine-DAV/vtk-h"
    url = "https://github.com/Alpine-DAV/vtk-h/releases/download/v0.5.8/vtkh-v0.5.8.tar.gz"
    git = "https://github.com/Alpine-DAV/vtk-h.git"

    maintainers("cyrush")

    version("develop", branch="develop", submodules=True)
    version("0.8.1", sha256="0cb1c84087e2b9385477fba3e7e197d6eabe1d366bd3bc87d7824e50dcdbe057")
    version("0.8.0", sha256="8366ebfe094c258555f343ba1f9bbad1d8e4804f844768b639f6ff13a6390f29")
    version("0.7.1", sha256="f28f7e6fb0f854a2293265b67cbdfb350b42c13ac08ffffe9cd246f3fe9fb77a")
    version("0.7.0", sha256="1b3c15c1340c5f66edcc2962ffe2f0d86e155f45a4932cf9c407261c203fbc19")
    version("0.6.9", sha256="8111f59c3528f02cb3c5083c17a1737dff9472266b156732794612471f3393c7")
    version("0.6.8", sha256="0a37468ca65fdc12509b9fd53c74d5afb090630280e1161415d7377cad7d45f1")
    version("0.6.7", sha256="aff3ab94cf137fbc3019149363d5d8a39d052b02ecef42c6bf6d076e538af3f2")
    version("0.6.6", sha256="5fe8bae5f55dbeb3047a37499cc41f3b548e4d86f0058993069f1df57f7915a1")
    version("0.6.5", sha256="3e566ee06150edece8a61711d9347de216c1ae45f3b4585784b2252ee9ff2a9b")
    version("0.6.4", sha256="c1345679fa4110cba449a9e27d40774d53c1f0bbddd41e52f5eb395cec1ee2d0")
    version("0.6.3", sha256="388ad05110efac45df6ae0d565a7d16bd05ff83c95b8b2b8daa206360ab73eec")
    version("0.6.2", sha256="1623e943a5a034d474c04755be8f0f40b639183cd9b576b1289eeee687d4cf6d")
    version("0.6.1", sha256="ca30b5ff1a48fa247cd20b3f19452f7744eb744465e0b64205135aece42d274f")
    version("0.6.0", sha256="2fc054f88ae253fb1bfcae22a156bcced08eca963ba90384dcd5b5791e6dfbf4")
    version("0.5.8", sha256="203b337f4280a24a2b75722384f77e0e2f5965058b541efc153db76b7ab98133")
    version("0.5.7", sha256="e8c1925dc34ee6be17cec734121e43002e3c02b54ef8dac341b51a455b95e402")
    version("0.5.6", sha256="c78c0fa71a9687c2951a06d2112b52aa81fdcdcfbc9464d1578326d03fbb205e")
    version("0.5.4", sha256="92bf3741df7a15e36ff41a9a783f3b88eecc86e55cad1defba76f141baa2610b")
    version("0.5.3", sha256="0c4aae3bd2a5906738a6806de2b62ea2049ac8b40ebe7fc2ba25505272c2d359")
    version("0.5.2", sha256="db2e6250c0ece6381fc90540317ad7b5869dbcce0231ce9be125916a77bfdb25")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Build vtk-h as shared libs")
    variant("mpi", default=True, description="build mpi support")
    # set to false for systems that implicitly link mpi
    variant("blt_find_mpi", default=True, description="Use BLT CMake Find MPI logic")
    variant("serial", default=True, description="build serial (non-mpi) libraries")
    variant("openmp", default=(sys.platform != "darwin"), description="build openmp support")
    variant("logging", default=False, description="Build vtk-h with logging enabled")
    variant("contourtree", default=False, description="Enable contour tree support")

    # Certain CMake versions have been found to break for our use cases
    depends_on("cmake@3.14.1:3.14.99,3.18.2:", type="build")

    depends_on("mpi", when="+mpi")
    depends_on("cuda", when="+cuda")
    depends_on("vtk-m+fpic")

    # use vtk-m 1.7 or newer for vtk-h 0.8 or newer
    depends_on("vtk-m@1.7", when="@0.8:")

    # use vtk-m 1.6 or lower for vtk-h 0.7 or lower
    depends_on("vtk-m@:1.6", when="@:0.7")
    depends_on("vtk-m~tbb")
    depends_on("vtk-m+openmp", when="+openmp")
    depends_on("vtk-m~openmp", when="~openmp")

    depends_on("vtk-m+openmp", when="+openmp")
    depends_on("vtk-m~openmp", when="~openmp")

    depends_on("vtk-m~cuda", when="~cuda")
    depends_on("vtk-m+cuda", when="+cuda")
    for _arch in CudaPackage.cuda_arch_values:
        depends_on(
            "vtk-m+cuda cuda_arch={0}".format(_arch),
            when="+cuda+openmp cuda_arch={0}".format(_arch),
        )

    depends_on("vtk-m~shared", when="~shared")

    patch("vtk-h-shared-cuda.patch", when="@0.8")

    # provide cmake args (pass host config as cmake cache file)
    def cmake_args(self):
        host_config = self._get_host_config_path(self.spec)
        options = []
        options.extend(["-C", host_config, "../spack-src/src/"])
        return options

    def _get_host_config_path(self, spec):
        sys_type = spec.architecture
        # if on llnl systems, we can use the SYS_TYPE
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        host_config_path = "{0}-{1}-{2}-vtkh-{3}.cmake".format(
            socket.gethostname(), sys_type, spec.compiler, spec.dag_hash()
        )
        dest_dir = spec.prefix
        host_config_path = os.path.abspath(join_path(dest_dir, host_config_path))
        return host_config_path

    @run_before("cmake")
    def hostconfig(self):
        spec = self.spec
        """
        This method creates a 'host-config' file that specifies
        all of the options used to configure and build vtkh.
        """

        if not os.path.isdir(spec.prefix):
            os.mkdir(spec.prefix)

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

        cmake_exe = spec["cmake"].command.path

        # get hostconfig name
        host_cfg_fname = self._get_host_config_path(spec)

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

        # shared vs static libs
        if "+shared" in spec:
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "ON"))
        else:
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "OFF"))

        cfg.write(cmake_cache_entry("ENABLE_TESTS", "OFF"))
        cfg.write(cmake_cache_entry("BUILD_TESTING", "OFF"))

        #######################
        # MPI
        #######################

        cfg.write("# MPI Support\n")

        if "+mpi" in spec:
            mpicc_path = spec["mpi"].mpicc
            mpicxx_path = spec["mpi"].mpicxx
            has_mpifc = hasattr(spec["mpi"], "mpifc")
            mpifc_path = spec["mpi"].mpifc if has_mpifc else None
            # if we are using compiler wrappers on cray systems
            # use those for mpi wrappers, b/c  spec['mpi'].mpicxx
            # etc make return the spack compiler wrappers
            # which can trip up mpi detection in CMake 3.14
            if cpp_compiler == "CC":
                mpicc_path = "cc"
                mpicxx_path = "CC"
                mpifc_path = "ftn"
            cfg.write(cmake_cache_entry("ENABLE_MPI", "ON"))
            cfg.write(cmake_cache_entry("MPI_C_COMPILER", mpicc_path))
            cfg.write(cmake_cache_entry("MPI_CXX_COMPILER", mpicxx_path))
            if has_mpifc:
                cfg.write(cmake_cache_entry("MPI_Fortran_COMPILER", mpifc_path))
            mpiexe_bin = join_path(spec["mpi"].prefix.bin, "mpiexec")
            if os.path.isfile(mpiexe_bin):
                # starting with cmake 3.10, FindMPI expects MPIEXEC_EXECUTABLE
                # vs the older versions which expect MPIEXEC
                if self.spec["cmake"].satisfies("@3.10:"):
                    cfg.write(cmake_cache_entry("MPIEXEC_EXECUTABLE", mpiexe_bin))
                else:
                    cfg.write(cmake_cache_entry("MPIEXEC", mpiexe_bin))
            if "+blt_find_mpi" in spec:
                cfg.write(cmake_cache_entry("ENABLE_FIND_MPI", "ON"))
            else:
                cfg.write(cmake_cache_entry("ENABLE_FIND_MPI", "OFF"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_MPI", "OFF"))

        #######################
        # CUDA
        #######################
        cfg.write("# CUDA Support\n")

        if "+cuda" in spec:
            cfg.write(cmake_cache_entry("ENABLE_CUDA", "ON"))
            cfg.write(cmake_cache_entry("VTKm_ENABLE_CUDA", "ON"))
            cfg.write(cmake_cache_entry("CMAKE_CUDA_HOST_COMPILER", env["SPACK_CXX"]))
        else:
            cfg.write(cmake_cache_entry("ENABLE_CUDA", "OFF"))
            cfg.write(cmake_cache_entry("VTKm_ENABLE_CUDA", "OFF"))

        #######################################################################
        # Core Dependencies
        #######################################################################

        #######################
        # VTK-h (and deps)
        #######################

        cfg.write("# vtk-m support \n")

        if "+openmp" in spec:
            cfg.write("# enable openmp support\n")
            cfg.write(cmake_cache_entry("ENABLE_OPENMP", "ON"))

        cfg.write("# vtk-m from spack\n")
        cfg.write(cmake_cache_entry("VTKM_DIR", spec["vtk-m"].prefix))

        #######################################################################
        # Optional Dependencies
        #######################################################################

        #######################
        # Serial
        #######################
        if "+serial" in spec:
            cfg.write(cmake_cache_entry("ENABLE_SERIAL", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_SERIAL", "OFF"))

        #######################
        # Logging
        #######################
        if "+logging" in spec:
            cfg.write(cmake_cache_entry("ENABLE_LOGGING", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_LOGGING", "OFF"))

        # contour tree
        if "+contourtree" in spec:
            cfg.write(cmake_cache_entry("ENABLE_FILTER_CONTOUR_TREE", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_FILTER_CONTOUR_TREE", "ON"))

        cfg.write("##################################\n")
        cfg.write("# end spack generated host-config\n")
        cfg.write("##################################\n")
        cfg.close()

        host_cfg_fname = os.path.abspath(host_cfg_fname)
        tty.info("spack generated host-config file: " + host_cfg_fname)
