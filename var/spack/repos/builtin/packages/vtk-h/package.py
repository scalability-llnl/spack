# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

import sys
import os
import socket


import llnl.util.tty as tty
from os import environ as env


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


class VtkH(Package, CudaPackage):
    """VTK-h is a toolkit of scientific visualization algorithms for emerging
    processor architectures. VTK-h brings together several projects like VTK-m
    and DIY2 to provide a toolkit with hybrid parallel capabilities."""

    homepage = "https://github.com/Alpine-DAV/vtk-h"
    url      = "https://github.com/Alpine-DAV/vtk-h/releases/download/v0.5.8/vtkh-v0.5.8.tar.gz"
    git      = "https://github.com/Alpine-DAV/vtk-h.git"

    maintainers = ['cyrush']

    version('develop', branch='develop', submodules=True)
    version('0.6.6', sha256="5fe8bae5f55dbeb3047a37499cc41f3b548e4d86f0058993069f1df57f7915a1")
    version('0.6.5', sha256="3e566ee06150edece8a61711d9347de216c1ae45f3b4585784b2252ee9ff2a9b")
    version('0.6.4', sha256="c1345679fa4110cba449a9e27d40774d53c1f0bbddd41e52f5eb395cec1ee2d0")
    version('0.6.3', sha256="388ad05110efac45df6ae0d565a7d16bd05ff83c95b8b2b8daa206360ab73eec")
    version('0.6.2', sha256="1623e943a5a034d474c04755be8f0f40b639183cd9b576b1289eeee687d4cf6d")
    version('0.6.1', sha256="ca30b5ff1a48fa247cd20b3f19452f7744eb744465e0b64205135aece42d274f")
    version('0.6.0', sha256="2fc054f88ae253fb1bfcae22a156bcced08eca963ba90384dcd5b5791e6dfbf4")
    version('0.5.8', sha256="203b337f4280a24a2b75722384f77e0e2f5965058b541efc153db76b7ab98133")
    version('0.5.7', sha256="e8c1925dc34ee6be17cec734121e43002e3c02b54ef8dac341b51a455b95e402")
    version('0.5.6', sha256="c78c0fa71a9687c2951a06d2112b52aa81fdcdcfbc9464d1578326d03fbb205e")
    version('0.5.4', sha256="92bf3741df7a15e36ff41a9a783f3b88eecc86e55cad1defba76f141baa2610b")
    version('0.5.3', sha256="0c4aae3bd2a5906738a6806de2b62ea2049ac8b40ebe7fc2ba25505272c2d359")
    version('0.5.2', sha256="db2e6250c0ece6381fc90540317ad7b5869dbcce0231ce9be125916a77bfdb25")

    variant("shared", default=True, description="Build vtk-h as shared libs")
    variant("mpi", default=True, description="build mpi support")
    variant("serial", default=True, description="build serial (non-mpi) libraries")
    variant("cuda", default=False, description="build cuda support")
    variant("openmp", default=(sys.platform != 'darwin'),
            description="build openmp support")
    variant("logging", default=False, description="Build vtk-h with logging enabled")
    variant("contourtree", default=False, description="Enable contour tree support")

    # Certain CMake versions have been found to break for our use cases
    depends_on("cmake@3.14.1:3.14.99,3.18.2:", type='build')

    depends_on("mpi", when="+mpi")
    depends_on("cuda", when="+cuda")

    depends_on("vtk-m@ascent_ver~tbb+openmp", when="+openmp")
    depends_on("vtk-m@ascent_ver~tbb~openmp", when="~openmp")

    depends_on("vtk-m@ascent_ver+cuda~tbb+openmp", when="+cuda+openmp")
    depends_on("vtk-m@ascent_ver+cuda~tbb~openmp", when="+cuda~openmp")

    depends_on("vtk-m@ascent_ver~tbb+openmp~shared", when="+openmp~shared")
    depends_on("vtk-m@ascent_ver~tbb~openmp~shared", when="~openmp~shared")

    depends_on("vtk-m@ascent_ver+cuda~tbb+openmp~shared", when="+cuda+openmp~shared")
    depends_on("vtk-m@ascent_ver+cuda~tbb~openmp~shared", when="+cuda~openmp~shared")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake_args = ["../src",
                          "-DVTKM_DIR={0}".format(spec["vtk-m"].prefix),
                          "-DENABLE_TESTS=OFF",
                          "-DBUILD_TESTING=OFF"]

            # shared vs static libs logic
            # force static when building with cuda
            if "+cuda" in spec:
                cmake_args.append('-DBUILD_SHARED_LIBS=OFF')
            else:
                if "+shared" in spec:
                    cmake_args.append('-DBUILD_SHARED_LIBS=ON')
                else:
                    cmake_args.append('-DBUILD_SHARED_LIBS=OFF')

            # mpi support
            if "+mpi" in spec:
                mpicc = spec['mpi'].mpicc
                mpicxx = spec['mpi'].mpicxx
                cmake_args.extend(["-DMPI_C_COMPILER={0}".format(mpicc),
                                   "-DMPI_CXX_COMPILER={0}".format(mpicxx)])
                mpiexe_bin = join_path(spec['mpi'].prefix.bin, 'mpiexec')
                if os.path.isfile(mpiexe_bin):
                    cmake_args.append("-DMPIEXEC={0}".format(mpiexe_bin))

            # openmp support
            if "+openmp" in spec:
                cmake_args.append("-DENABLE_OPENMP=ON")

            # build with logging
            if "+logging" in spec:
                cmake_args.append("-DENABLE_LOGGING=ON")

            if "+contourtree" in spec:
                cmake_args.append("-DENABLE_FILTER_CONTOUR_TREE=ON")

            # cuda support
            if "+cuda" in spec:
                cmake_args.append("-DVTKm_ENABLE_CUDA:BOOL=ON")
                cmake_args.append("-DENABLE_CUDA:BOOL=ON")
                cmake_args.append("-DCMAKE_CUDA_HOST_COMPILER={0}".format(
                                  env["SPACK_CXX"]))
            else:
                cmake_args.append("-DVTKm_ENABLE_CUDA:BOOL=OFF")
                cmake_args.append("-DENABLE_CUDA:BOOL=OFF")
            # use release, instead of release with debug symbols b/c vtkh libs
            # can overwhelm compilers with too many symbols
            for arg in std_cmake_args:
                if arg.count("CMAKE_BUILD_TYPE") == 0:
                    cmake_args.extend(std_cmake_args)
            cmake_args.append("-DCMAKE_BUILD_TYPE=Release")
            cmake(*cmake_args)
            make()
            make("install")

            host_cfg_fname = self.create_host_config(spec,
                                                     prefix)

            install(host_cfg_fname, prefix)

    def create_host_config(self, spec, prefix, py_site_pkgs_dir=None):
        """
        This method creates a 'host-config' file that specifies
        all of the options used to configure and build vtkh.
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

        cmake_exe = spec['cmake'].command.path

        host_cfg_fname = "%s-%s-%s-vtkh.cmake" % (socket.gethostname(),
                                                  sys_type,
                                                  spec.compiler)

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
        if "+shared" in spec:
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "ON"))
        else:
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "OFF"))

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
        cfg.write(cmake_cache_entry("VTKM_DIR", spec['vtk-m'].prefix))

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

        #######################
        # MPI
        #######################

        cfg.write("# MPI Support\n")

        if "+mpi" in spec:
            mpicc_path = spec['mpi'].mpicc
            mpicxx_path = spec['mpi'].mpicxx
            mpifc_path = spec['mpi'].mpifc
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
            cfg.write(cmake_cache_entry("MPI_Fortran_COMPILER", mpifc_path))
            mpiexe_bin = join_path(spec['mpi'].prefix.bin, 'mpiexec')
            if os.path.isfile(mpiexe_bin):
                # starting with cmake 3.10, FindMPI expects MPIEXEC_EXECUTABLE
                # vs the older versions which expect MPIEXEC
                if self.spec["cmake"].satisfies('@3.10:'):
                    cfg.write(cmake_cache_entry("MPIEXEC_EXECUTABLE",
                                                mpiexe_bin))
                else:
                    cfg.write(cmake_cache_entry("MPIEXEC",
                                                mpiexe_bin))
        else:
            cfg.write(cmake_cache_entry("ENABLE_MPI", "OFF"))

        #######################
        # CUDA
        #######################

        cfg.write("# CUDA Support\n")

        if "+cuda" in spec:
            cfg.write(cmake_cache_entry("ENABLE_CUDA", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_CUDA", "OFF"))

        cfg.write("##################################\n")
        cfg.write("# end spack generated host-config\n")
        cfg.write("##################################\n")
        cfg.close()

        host_cfg_fname = os.path.abspath(host_cfg_fname)
        tty.info("spack generated conduit host-config file: " + host_cfg_fname)
        return host_cfg_fname
