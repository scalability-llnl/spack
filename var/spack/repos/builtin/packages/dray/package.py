# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import socket

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


class Dray(Package, CudaPackage):
    """High-Order Mesh Ray Tracer."""

    homepage = "https://github.com/LLNL/devil_ray"
    git      = "https://github.com/LLNL/devil_ray.git"
    url      = "https://github.com/LLNL/devil_ray/releases/download/v0.1.2/dray-v0.1.2.tar.gz"

    maintainers = ['mclarsen', 'cyrush']

    version('develop', branch='develop', submodules='True')
    version('0.1.2',  sha256='46937f20124b28dc78a634e8e063a3e7a3bbfd9f424ce2680b08417010c376da')
    version('0.1.1',  sha256='e5daa49ee3367c087f5028dc5a08655298beb318014c6f3f65ef4a08fcbe346c')
    version('0.1.0',  sha256='8b341138e1069361351e0a94478608c5af479cca76e2f97d556229aed45c0169')

    variant('cuda', default=False, description='Build with CUDA backend')
    variant('openmp', default=True, description='Build OpenMP backend')
    variant("shared", default=True, description="Build as shared libs")
    variant("test", default=True, description='Build unit tests')
    variant("utils", default=True, description='Build utilities')
    variant("logging", default=False, description='Enable logging')
    variant("stats", default=False, description='Enable stats')
    variant("mpi", default=True, description='Enable MPI compiler')

    depends_on('cuda', when='+cuda')
    depends_on('mpi', when='+mpi')

    depends_on('cmake@3.9:', type='build')
    depends_on('cmake@3.14:', when='+cuda', type='build')

    depends_on("conduit~shared", when="~shared")
    depends_on("conduit+shared", when="+shared")

    depends_on("apcomp~shared+openmp+mpi", when="~shared+openmp+mpi")
    depends_on("apcomp+shared+openmp+mpi", when="+shared+openmp+mpi")
    depends_on("apcomp~shared~openmp+mpi", when="~shared~openmp+mpi")
    depends_on("apcomp+shared~openmp+mpi", when="+shared~openmp+mpi")
    depends_on("apcomp~shared+openmp~mpi", when="~shared+openmp~mpi")
    depends_on("apcomp+shared+openmp~mpi", when="+shared+openmp~mpi")
    depends_on("apcomp~shared~openmp~mpi", when="~shared~openmp~mpi")
    depends_on("apcomp+shared~openmp~mpi", when="+shared~openmp~mpi")

    depends_on("raja@0.9.0+cuda~openmp+shared", when="+cuda~openmp+shared")
    depends_on("raja@0.9.0+cuda+openmp+shared", when="+cuda+openmp+shared")
    depends_on("raja@0.9.0+cuda~openmp~shared", when="+cuda~openmp~shared")
    depends_on("raja@0.9.0+cuda+openmp~shared", when="+cuda+openmp~shared")

    depends_on("raja@0.9.0~cuda~openmp+shared", when="~cuda~openmp+shared")
    depends_on("raja@0.9.0~cuda+openmp+shared", when="~cuda+openmp+shared")
    depends_on("raja@0.9.0~cuda~openmp~shared", when="~cuda~openmp~shared")
    depends_on("raja@0.9.0~cuda+openmp~shared", when="~cuda+openmp~shared")

    depends_on("umpire@1.0.0+cuda+shared", when="+cuda+shared")
    depends_on("umpire@1.0.0+cuda~shared", when="+cuda~shared")
    depends_on("umpire@1.0.0~cuda+shared", when="~cuda+shared")
    depends_on("umpire@1.0.0~cuda~shared", when="~cuda~shared")

    depends_on("mfem+shared+conduit~threadsafe", when="+shared")
    depends_on("mfem~shared+conduit~threadsafe", when="~shared")

    def setup_build_environment(self, env):
        env.set('CTEST_OUTPUT_ON_FAILURE', '1')

    def install(self, spec, prefix):
        """
        Build and install Devil Ray.
        """
        with working_dir('spack-build', create=True):
            host_cfg_fname = self.create_host_config(spec,
                                                     prefix)
            cmake_args = []
            # if we have a static build, we need to avoid any of
            # spack's default cmake settings related to rpaths
            # (see: https://github.com/LLNL/spack/issues/2658)
            if "+shared" in spec:
                cmake_args.extend(std_cmake_args)
            else:
                for arg in std_cmake_args:
                    if arg.count("RPATH") == 0:
                        cmake_args.append(arg)
            cmake_args.extend(["-C", host_cfg_fname, "../src"])
            print("Configuring Devil Ray...")
            cmake(*cmake_args)
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
            http://ascent.readthedocs.io/en/latest/BuildingAscent.html
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

        if "+cmake" in spec:
            cmake_exe = spec['cmake'].command.path
        else:
            cmake_exe = which("cmake")
            if cmake_exe is None:
                msg = 'failed to find CMake (and cmake variant is off)'
                raise RuntimeError(msg)
            cmake_exe = cmake_exe.path

        host_cfg_fname = "%s-%s-%s-devil_ray.cmake" % (socket.gethostname(),
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

        if "+mpi" in spec:
            cfg.write(cmake_cache_entry("ENABLE_MPI", "ON"))
            mpicc_path = spec['mpi'].mpicc
            mpicxx_path = spec['mpi'].mpicxx
            # if we are using compiler wrappers on cray systems
            # use those for mpi wrappers, b/c  spec['mpi'].mpicxx
            # etc make return the spack compiler wrappers
            # which can trip up mpi detection in CMake 3.14
            if cpp_compiler == "CC":
                mpicc_path = "cc"
                mpicxx_path = "CC"

            cfg.write(cmake_cache_entry("CMAKE_C_COMPILER", mpicc_path))
            cfg.write(cmake_cache_entry("CMAKE_CXX_COMPILER", mpicxx_path))
        else:
            cfg.write(cmake_cache_entry("ENABLE_MPI", "OFF"))
            cfg.write("# c compiler used by spack\n")
            cfg.write(cmake_cache_entry("CMAKE_C_COMPILER", c_compiler))
            cfg.write("# cpp compiler used by spack\n")
            cfg.write(cmake_cache_entry("CMAKE_CXX_COMPILER", cpp_compiler))

        #######################
        # Backends
        #######################

        cfg.write("# CUDA Support\n")

        if "+cuda" in spec:
            cfg.write(cmake_cache_entry("ENABLE_CUDA", "ON"))
            if 'cuda_arch' in spec.variants:
                cuda_value = spec.variants['cuda_arch'].value
                cuda_arch = cuda_value[0]
                cfg.write(cmake_cache_entry('CUDA_ARCH',
                                            'sm_{0}'.format(cuda_arch)))
        else:
            cfg.write(cmake_cache_entry("ENABLE_CUDA", "OFF"))

        if "+openmp" in spec:
            cfg.write(cmake_cache_entry("ENABLE_OPENMP", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_OPENMP", "OFF"))

        # shared vs static libs
        if "+shared" in spec:
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "ON"))
        else:
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "OFF"))

        #######################
        # Unit Tests
        #######################
        if "+test" in spec:
            cfg.write(cmake_cache_entry("DRAY_ENABLE_TESTS", "ON"))
        else:
            cfg.write(cmake_cache_entry("DRAY_ENABLE_TESTS", "OFF"))

        #######################
        # Utilities
        #######################
        if "+utils" in spec:
            cfg.write(cmake_cache_entry("DRAY_ENABLE_UTILS", "ON"))
        else:
            cfg.write(cmake_cache_entry("DRAY_ENABLE_UTILS", "OFF"))

        #######################
        # Logging
        #######################
        if "+logging" in spec:
            cfg.write(cmake_cache_entry("ENABLE_LOGGING", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_LOGGING", "OFF"))

        #######################
        # Logging
        #######################
        if "+stats" in spec:
            cfg.write(cmake_cache_entry("ENABLE_STATS", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_STATS", "OFF"))

        #######################################################################
        # Core Dependencies
        #######################################################################

        cfg.write("# conduit from spack \n")
        cfg.write(cmake_cache_entry("CONDUIT_DIR", spec['conduit'].prefix))

        cfg.write("# mfem from spack \n")
        cfg.write(cmake_cache_entry("MFEM_DIR", spec['mfem'].prefix))

        cfg.write("# raja from spack \n")
        cfg.write(cmake_cache_entry("RAJA_DIR", spec['raja'].prefix))

        cfg.write("# umpire from spack \n")
        cfg.write(cmake_cache_entry("UMPIRE_DIR", spec['umpire'].prefix))

        cfg.write("# apcompositor from spack \n")
        cfg.write(cmake_cache_entry("APCOMP_DIR", spec['apcomp'].prefix))

        cfg.write("##################################\n")
        cfg.write("# end spack generated host-config\n")
        cfg.write("##################################\n")
        cfg.close()

        host_cfg_fname = os.path.abspath(host_cfg_fname)
        tty.info("spack generated conduit host-config file: " + host_cfg_fname)
        return host_cfg_fname

    def cmake_args(self):
        spec = self.spec

        options = []

        if '+openmp' in spec:
            options.extend([
                '-DENABLE_OPENMP=On'])

        if '+cuda' in spec:
            options.extend([
                '-DENABLE_CUDA=On',
                '-DCUDA_TOOLKIT_ROOT_DIR=%s' % (spec['cuda'].prefix)])
            if 'cuda_arch' in spec.variants:
                cuda_value = spec.variants['cuda_arch'].value
                cuda_arch = cuda_value[0]
                options.append('-DCUDA_ARCH=sm_{0}'.format(cuda_arch))
        else:
            options.extend(['-DENABLE_CUDA=OFF'])

        options.extend(['-DRAJA_DIR=%s' % (spec['raja'].prefix)])
        options.extend(['-DMFEM_DIR=%s' % (spec['mfem'].prefix)])
        options.extend(['-DUMPIRE_DIR=%s' % (spec['umpire'].prefix)])
        options.extend(['-DCONDUIT_DIR=%s' % (spec['conduit'].prefix)])
        options.extend(['-DDRAY_ENABLE_TESTS=OFF'])
        options.extend(['-DENABLE_LOGGING=OFF'])
        options.extend(['-DENABLE_STATS=OFF'])
        options.extend(['../src'])

        return options
