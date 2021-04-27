# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import socket
import os
import glob
import shutil

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


class Conduit(CMakePackage):
    """Conduit is an open source project from Lawrence Livermore National
    Laboratory that provides an intuitive model for describing hierarchical
    scientific data in C++, C, Fortran, and Python. It is used for data
    coupling between packages in-core, serialization, and I/O tasks."""

    homepage = "http://software.llnl.gov/conduit"
    url      = "https://github.com/LLNL/conduit/releases/download/v0.3.0/conduit-v0.3.0-src-with-blt.tar.gz"
    git      = "https://github.com/LLNL/conduit.git"

    version('develop', branch='develop', submodules=True, preferred=True)
    # note: the main branch in conduit was renamed to develop, this next entry
    # is to bridge any spack dependencies that are still using the name master
    version('master', branch='develop', submodules=True)
    version('0.7.1', sha256='460a480cf08fedbf5b38f707f94f20828798327adadb077f80dbab048fd0a07d')
    version('0.7.0', sha256='ecaa9668ebec5d4efad19b104d654a587c0adbd5f502128f89601408cb4d7d0c')
    version('0.6.0', sha256='078f086a13b67a97e4ab6fe1063f2fef2356df297e45b43bb43d74635f80475d')
    version('0.5.1', sha256='68a3696d1ec6d3a4402b44a464d723e6529ec41016f9b44c053676affe516d44')
    version('0.5.0', sha256='7efac668763d02bd0a2c0c1b134d9f5ee27e99008183905bb0512e5502b8b4fe')
    version('0.4.0', sha256='c228e6f0ce5a9c0ffb98e0b3d886f2758ace1a4b40d00f3f118542c0747c1f52')
    version('0.3.1', sha256='7b358ca03bb179876291d4a55d6a1c944b7407a80a588795b9e47940b1990521')
    version('0.3.0', sha256='52e9cf5720560e5f7492876c39ef2ea20ae73187338361d2744bdf67567da155')
    # note: checksums on github automatic release source tars changed ~9/17
    version('0.2.1', sha256='796576b9c69717c52f0035542c260eb7567aa351ee892d3fbe3521c38f1520c4')
    version('0.2.0', sha256='31eff8dbc654a4b235cfcbc326a319e1752728684296721535c7ca1c9b463061')

    maintainers = ['cyrush']

    ###########################################################################
    # package variants
    ###########################################################################

    variant("shared", default=True, description="Build Conduit as shared libs")
    variant("test", default=True, description='Enable Conduit unit tests')

    # variants for python support
    variant("python", default=False, description="Build Conduit Python support")
    variant("fortran", default=True, description="Build Conduit Fortran support")

    # variants for comm and i/o
    variant("mpi", default=True, description="Build Conduit MPI Support")
    variant("hdf5", default=True, description="Build Conduit HDF5 support")
    variant("hdf5_compat", default=True,
            description="Build Conduit with HDF5 1.8.x (compatibility mode)")
    variant("silo", default=False, description="Build Conduit Silo support")
    variant("adios", default=False, description="Build Conduit ADIOS support")

    # zfp compression
    variant("zfp", default=False, description="Build Conduit ZFP support")

    # variants for dev-tools (docs, etc)
    variant("doc", default=False, description="Build Conduit's documentation")
    # doxygen support is wip, since doxygen has several dependencies
    # we want folks to explicitly opt in to building doxygen
    variant("doxygen", default=False, description="Build Conduit's Doxygen documentation")

    ###########################################################################
    # package dependencies
    ###########################################################################

    #######################
    # CMake
    #######################
    # cmake 3.14.1 or newer
    depends_on("cmake@3.14.1:", type='build')

    #######################
    # Python
    #######################
    depends_on("python", when="+python")
    extends("python", when="+python")
    depends_on("py-numpy", when="+python", type=('build', 'run'))
    depends_on("py-mpi4py", when="+python+mpi", type=('build', 'run'))

    #######################
    # I/O Packages
    #######################

    ###############
    # HDF5
    ###############
    # Note: cxx variant is disabled due to build issue Cyrus
    # experienced on BGQ. When on, the static build tries
    # to link against shared libs.
    #
    # Use HDF5 1.8, for wider output compatibly
    # variants reflect we are not using hdf5's mpi or fortran features.
    depends_on("hdf5@1.8.19:1.8.999~cxx", when="+hdf5+hdf5_compat+shared")
    depends_on("hdf5@1.8.19:1.8.999~shared~cxx", when="+hdf5+hdf5_compat~shared")
    depends_on("hdf5~cxx", when="+hdf5~hdf5_compat+shared")
    depends_on("hdf5~shared~cxx", when="+hdf5~hdf5_compat~shared")

    ###############
    # Silo
    ###############
    # we are not using silo's fortran features
    depends_on("silo~fortran", when="+silo+shared")
    depends_on("silo~shared~fortran", when="+silo~shared")

    ###############
    # ADIOS
    ###############
    depends_on("adios+mpi~hdf5+shared",       when="+adios+mpi+shared")
    depends_on("adios+mpi~hdf5~shared~blosc", when="+adios+mpi~shared")
    depends_on("adios~mpi~hdf5+shared",       when="+adios~mpi+shared")
    depends_on("adios~mpi~hdf5~shared~blosc", when="+adios~mpi~shared")

    #######################
    # ZFP
    #######################
    depends_on("zfp  bsws=8", when="+zfp")

    # hdf5 zfp plugin when both hdf5 and zfp are on
    depends_on("h5z-zfp~fortran", when="+hdf5+zfp")

    #######################
    # MPI
    #######################
    depends_on("mpi", when="+mpi")

    #######################
    # Documentation related
    #######################
    depends_on("py-sphinx", when="+python+doc", type='build')
    depends_on("py-sphinx-rtd-theme", when="+python+doc", type='build')
    depends_on("doxygen", when="+doc+doxygen")

    # Tentative patch for fj compiler
    # Cmake will support fj compiler and this patch will be removed
    patch('fj_flags.patch', when='%fj')

    ###################################
    # build phases used by this package
    ###################################
    phases = ['hostconfig', 'cmake', 'build', 'install']

    def flag_handler(self, name, flags):
        if name in ('cflags', 'cxxflags', 'fflags'):
            # the package manages these flags in another way
            return (None, None, None)
        return (flags, None, None)

    def setup_build_environment(self, env):
        env.set('CTEST_OUTPUT_ON_FAILURE', '1')

    def url_for_version(self, version):
        """
        Provide proper url
        """
        v = str(version)
        if v == "0.2.0":
            return "https://github.com/LLNL/conduit/archive/v0.2.0.tar.gz"
        elif v == "0.2.1":
            return "https://github.com/LLNL/conduit/archive/v0.2.1.tar.gz"
        else:
            # starting with v 0.3.0, conduit uses BLT
            # (https://github.com/llnl/blt) as a submodule, since github does
            # not automatically package source from submodules, conduit
            # provides a custom src tarball
            return "https://github.com/LLNL/conduit/releases/download/v{0}/conduit-v{1}-src-with-blt.tar.gz".format(v, v)
        return url

    ####################################################################
    # Note: cmake, build, and install stages are handled by CMakePackage
    ####################################################################

    # provide cmake args (pass host config as cmake cache file)
    def cmake_args(self):
        host_config = self._get_host_config_path(self.spec)
        options = []
        options.extend(['-C', host_config, "../spack-src/src/"])
        return options

    @run_after('build')
    @on_package_attributes(run_tests=True)
    def build_test(self):
        with working_dir('spack-build'):
            print("Running Conduit Unit Tests...")
            make("test")

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):
        """
        Checks the spack install of conduit using conduit's
        using-with-cmake example
        """
        print("Checking Conduit installation...")
        spec = self.spec
        install_prefix = spec.prefix
        example_src_dir = join_path(install_prefix,
                                    "examples",
                                    "conduit",
                                    "using-with-cmake")
        print("Checking using-with-cmake example...")
        with working_dir("check-conduit-using-with-cmake-example",
                         create=True):
            cmake_args = ["-DCONDUIT_DIR={0}".format(install_prefix),
                          example_src_dir]
            cmake(*cmake_args)
            make()
            example = Executable('./conduit_example')
            example()
        print("Checking using-with-make example...")
        example_src_dir = join_path(install_prefix,
                                    "examples",
                                    "conduit",
                                    "using-with-make")
        example_files = glob.glob(join_path(example_src_dir, "*"))
        with working_dir("check-conduit-using-with-make-example",
                         create=True):
            for example_file in example_files:
                shutil.copy(example_file, ".")
            make("CONDUIT_DIR={0}".format(install_prefix))
            example = Executable('./conduit_example')
            example()

    def _get_host_config_path(self, spec):
        sys_type = spec.architecture
        # if on llnl systems, we can use the SYS_TYPE
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        host_config_path = "{0}-{1}-{2}-conduit-{3}.cmake".format(socket.gethostname(),
                                                                  sys_type,
                                                                  spec.compiler,
                                                                  spec.dag_hash())
        dest_dir = spec.prefix
        host_config_path = os.path.abspath(join_path(dest_dir,
                                                     host_config_path))
        return host_config_path

    def hostconfig(self, spec, prefix):
        """
        This method creates a 'host-config' file that specifies
        all of the options used to configure and build conduit.

        For more details about 'host-config' files see:
            http://software.llnl.gov/conduit/building.html
        """
        if not os.path.isdir(spec.prefix):
            os.mkdir(spec.prefix)

        #######################
        # Compiler Info
        #######################
        c_compiler = env["SPACK_CC"]
        cpp_compiler = env["SPACK_CXX"]
        f_compiler = None

        if self.compiler.fc:
            # even if this is set, it may not exist
            # do one more sanity check
            if os.path.isfile(env["SPACK_FC"]):
                f_compiler  = env["SPACK_FC"]

        #######################################################################
        # Directly fetch the names of the actual compilers to create a
        # 'host config' file that works outside of the spack install env.
        #######################################################################

        sys_type = spec.architecture
        # if on llnl systems, we can use the SYS_TYPE
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]

        # are we on a specific machine
        on_blueos = 'blueos' in sys_type

        ##############################################
        # Find and record what CMake is used
        ##############################################

        cmake_exe = spec['cmake'].command.path

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

        cfg.write("# fortran compiler used by spack\n")
        if "+fortran" in spec and f_compiler is not None:
            cfg.write(cmake_cache_entry("ENABLE_FORTRAN", "ON"))
            cfg.write(cmake_cache_entry("CMAKE_Fortran_COMPILER",
                                        f_compiler))
        else:
            cfg.write("# no fortran compiler found\n\n")
            cfg.write(cmake_cache_entry("ENABLE_FORTRAN", "OFF"))

        if "+shared" in spec:
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "ON"))
        else:
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "OFF"))

        # use global spack compiler flags
        cppflags = ' '.join(spec.compiler_flags['cppflags'])
        if cppflags:
            # avoid always ending up with ' ' with no flags defined
            cppflags += ' '
        cflags = cppflags + ' '.join(spec.compiler_flags['cflags'])
        if cflags:
            cfg.write(cmake_cache_entry("CMAKE_C_FLAGS", cflags))
        cxxflags = cppflags + ' '.join(spec.compiler_flags['cxxflags'])
        if cxxflags:
            cfg.write(cmake_cache_entry("CMAKE_CXX_FLAGS", cxxflags))
        fflags = ' '.join(spec.compiler_flags['fflags'])
        if fflags:
            cfg.write(cmake_cache_entry("CMAKE_Fortran_FLAGS", fflags))

        if ((f_compiler is not None)
           and ("gfortran" in f_compiler)
           and ("clang" in cpp_compiler)):
            libdir = os.path.join(os.path.dirname(
                                  os.path.dirname(f_compiler)), "lib")
            flags = ""
            for _libpath in [libdir, libdir + "64"]:
                if os.path.exists(_libpath):
                    flags += " -Wl,-rpath,{0}".format(_libpath)
            description = ("Adds a missing libstdc++ rpath")
            if flags:
                cfg.write(cmake_cache_entry("BLT_EXE_LINKER_FLAGS", flags,
                                            description))

        #######################
        # Unit Tests
        #######################
        if "+test" in spec:
            cfg.write(cmake_cache_entry("ENABLE_TESTS", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_TESTS", "OFF"))

        # extra fun for blueos
        if on_blueos:
            # All of BlueOS compilers report clang due to nvcc,
            # override to proper compiler family
            if "xlc" in c_compiler:
                cfg.write(cmake_cache_entry("CMAKE_C_COMPILER_ID", "XL"))
            if "xlC" in cpp_compiler:
                cfg.write(cmake_cache_entry("CMAKE_CXX_COMPILER_ID", "XL"))

            if "+fortran" in spec:
                if "xlf" in f_compiler:
                    cfg.write(cmake_cache_entry("CMAKE_Fortran_COMPILER_ID",
                                                "XL"))

                if (f_compiler is not None) and ("xlf" in f_compiler):
                    # Fix missing std linker flag in xlc compiler
                    flags = "-WF,-C! -qxlf2003=polymorphic"
                    cfg.write(cmake_cache_entry("BLT_FORTRAN_FLAGS",
                                                flags))
                    # Grab lib directory for the current fortran compiler
                    libdir = os.path.join(os.path.dirname(
                                          os.path.dirname(f_compiler)), "lib")
                    rpaths = "-Wl,-rpath,{0} -Wl,-rpath,{0}64".format(libdir)

                    flags  = "${BLT_EXE_LINKER_FLAGS} -lstdc++ " + rpaths
                    cfg.write(cmake_cache_entry("BLT_EXE_LINKER_FLAGS",
                                                flags))
                    if "+shared" in spec:
                        flags = "${CMAKE_SHARED_LINKER_FLAGS} " + rpaths
                        cfg.write(cmake_cache_entry(
                                  "CMAKE_SHARED_LINKER_FLAGS", flags))

        #######################
        # Python
        #######################

        cfg.write("# Python Support\n")

        if "+python" in spec:
            cfg.write("# Enable python module builds\n")
            cfg.write(cmake_cache_entry("ENABLE_PYTHON", "ON"))
            cfg.write("# python from spack \n")
            cfg.write(cmake_cache_entry("PYTHON_EXECUTABLE",
                      spec['python'].command.path))
            try:
                cfg.write("# python module install dir\n")
                cfg.write(cmake_cache_entry("PYTHON_MODULE_INSTALL_PREFIX",
                          site_packages_dir))
            except NameError:
                # spack's  won't exist in a subclass
                pass
        else:
            cfg.write(cmake_cache_entry("ENABLE_PYTHON", "OFF"))

        if "+doc" in spec:
            if "+python" in spec:
                cfg.write(cmake_cache_entry("ENABLE_DOCS", "ON"))

                cfg.write("# sphinx from spack \n")
                sphinx_build_exe = join_path(spec['py-sphinx'].prefix.bin,
                                             "sphinx-build")
                cfg.write(cmake_cache_entry("SPHINX_EXECUTABLE",
                                            sphinx_build_exe))
            if "+doxygen" in spec:
                cfg.write("# doxygen from uberenv\n")
                doxygen_exe = spec['doxygen'].command.path
                cfg.write(cmake_cache_entry("DOXYGEN_EXECUTABLE", doxygen_exe))
        else:
            cfg.write(cmake_cache_entry("ENABLE_DOCS", "OFF"))

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
            if spec['mpi'].mpicc == spack_cc:
                mpicc_path = c_compiler
                mpicxx_path = cpp_compiler
                mpifc_path = f_compiler
            cfg.write(cmake_cache_entry("ENABLE_MPI", "ON"))
            cfg.write(cmake_cache_entry("MPI_C_COMPILER", mpicc_path))
            cfg.write(cmake_cache_entry("MPI_CXX_COMPILER", mpicxx_path))
            if "+fortran" in spec:
                cfg.write(cmake_cache_entry("MPI_Fortran_COMPILER",
                                            mpifc_path))

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
        # ZFP
        #######################
        cfg.write("# zfp from spack \n")
        if "+zfp" in spec:
            cfg.write(cmake_cache_entry("ZFP_DIR", spec['zfp'].prefix))
        else:
            cfg.write("# zfp not built by spack \n")

        #######################################################################
        # I/O Packages
        #######################################################################

        cfg.write("# I/O Packages\n\n")

        #######################
        # HDF5
        #######################

        cfg.write("# hdf5 from spack \n")

        if "+hdf5" in spec:
            cfg.write(cmake_cache_entry("HDF5_DIR", spec['hdf5'].prefix))
        else:
            cfg.write("# hdf5 not built by spack \n")

        #######################
        # h5z-zfp
        #######################

        cfg.write("# h5z-zfp from spack \n")

        if "+hdf5+zfp" in spec:
            cfg.write(cmake_cache_entry("H5ZZFP_DIR", spec['h5z-zfp'].prefix))
        else:
            cfg.write("# h5z-zfp not built by spack \n")

        #######################
        # Silo
        #######################

        cfg.write("# silo from spack \n")

        if "+silo" in spec:
            cfg.write(cmake_cache_entry("SILO_DIR", spec['silo'].prefix))
        else:
            cfg.write("# silo not built by spack \n")

        #######################
        # ADIOS
        #######################

        cfg.write("# ADIOS from spack \n")

        if "+adios" in spec:
            cfg.write(cmake_cache_entry("ADIOS_DIR", spec['adios'].prefix))
        else:
            cfg.write("# adios not built by spack \n")

        cfg.write("##################################\n")
        cfg.write("# end spack generated host-config\n")
        cfg.write("##################################\n")
        cfg.close()

        host_cfg_fname = os.path.abspath(host_cfg_fname)
        tty.info("spack generated conduit host-config file: " + host_cfg_fname)
