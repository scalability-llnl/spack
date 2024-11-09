# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import shutil
import socket
from os import environ as env

import llnl.util.tty as tty

from spack.package import *


def cmake_cache_entry(name, value, vtype=None, force=False):
    """
    Helper that creates CMake cache entry strings used in
    'host-config' files.
    """
    if vtype is None:
        if value == "ON" or value == "OFF":
            vtype = "BOOL"
        else:
            vtype = "PATH"
    force_str = " FORCE" if force else ""
    return 'set({0} "{1}" CACHE {2} ""{3})\n\n'.format(name, value, vtype, force_str)


class Conduit(CMakePackage):
    """Conduit is an open source project from Lawrence Livermore National
    Laboratory that provides an intuitive model for describing hierarchical
    scientific data in C++, C, Fortran, and Python. It is used for data
    coupling between packages in-core, serialization, and I/O tasks."""

    homepage = "https://software.llnl.gov/conduit"
    url = "https://github.com/LLNL/conduit/releases/download/v0.3.0/conduit-v0.3.0-src-with-blt.tar.gz"
    git = "https://github.com/LLNL/conduit.git"
    tags = ["radiuss", "e4s"]

    license("Apache-2.0")

    version("develop", branch="develop", submodules=True)
    # note: the main branch in conduit was renamed to develop, this next entry
    # is to bridge any spack dependencies that are still using the name master
    version("master", branch="develop", submodules=True)
    # note: 2021-05-05 latest tagged release is now preferred instead of develop
    version("0.9.2", sha256="45d5a4eccd0fc978d153d29c440c53c483b8f29dfcf78ddcc9aa15c59b257177")
    version("0.9.1", sha256="a3f1168738dcf72f8ebf83299850301aaf56e803f40618fc1230a755d0d05363")
    version("0.9.0", sha256="844e012400ab820967eef6cec15e1aa9a68cb05119d0c1f292d3c01630111a58")
    version("0.8.8", sha256="99811e9c464b6f841f52fcd47e982ae47cbb01cba334cff43eabe13eea58c0df")
    version("0.8.7", sha256="f3bf44d860783f4e0d61517c5e280c88144af37414569f4cf86e2d29b3ba5293")
    version("0.8.6", sha256="8ca5d37033143ed7181c7286dd25a3f6126ba0358889066f13a2b32f68fc647e")
    version("0.8.5", sha256="b4a6f269a81570a4597e2565927fd0ed2ac45da0a2500ce5a71c26f7c92c5483")
    version("0.8.4", sha256="55c37ddc668dbc45d43b60c440192f76e688a530d64f9fe1a9c7fdad8cd525fd")
    version("0.8.3", sha256="a9e60945366f3b8c37ee6a19f62d79a8d5888be7e230eabc31af2f837283ed1a")
    version("0.8.2", sha256="928eb8496bc50f6d8404f5bfa70220250876645d68d4f35ce0b99ecb85546284")
    version("0.8.1", sha256="488f22135a35136de592173131d123f7813818b7336c3b18e04646318ad3cbee")
    version("0.8.0", sha256="0607dcf9ced44f95e0b9549f5bbf7a332afd84597c52e293d7ca8d83117b5119")
    version("0.7.2", sha256="359fd176297700cdaed2c63e3b72d236ff3feec21a655c7c8292033d21d5228a")
    version("0.7.1", sha256="460a480cf08fedbf5b38f707f94f20828798327adadb077f80dbab048fd0a07d")
    version("0.7.0", sha256="ecaa9668ebec5d4efad19b104d654a587c0adbd5f502128f89601408cb4d7d0c")
    version("0.6.0", sha256="078f086a13b67a97e4ab6fe1063f2fef2356df297e45b43bb43d74635f80475d")
    version("0.5.1", sha256="68a3696d1ec6d3a4402b44a464d723e6529ec41016f9b44c053676affe516d44")
    version("0.5.0", sha256="7efac668763d02bd0a2c0c1b134d9f5ee27e99008183905bb0512e5502b8b4fe")
    version("0.4.0", sha256="c228e6f0ce5a9c0ffb98e0b3d886f2758ace1a4b40d00f3f118542c0747c1f52")
    version("0.3.1", sha256="7b358ca03bb179876291d4a55d6a1c944b7407a80a588795b9e47940b1990521")
    version("0.3.0", sha256="52e9cf5720560e5f7492876c39ef2ea20ae73187338361d2744bdf67567da155")
    # note: checksums on github automatic release source tars changed ~9/17
    version("0.2.1", sha256="796576b9c69717c52f0035542c260eb7567aa351ee892d3fbe3521c38f1520c4")
    version("0.2.0", sha256="31eff8dbc654a4b235cfcbc326a319e1752728684296721535c7ca1c9b463061")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    maintainers("cyrush")

    root_cmakelists_dir = "src"

    ###########################################################################
    # package variants
    ###########################################################################

    variant("examples", default=True, description="Build Conduit examples")
    variant("shared", default=True, description="Build Conduit as shared libs")
    variant("test", default=True, description="Enable Conduit unit tests")
    variant("utilities", default=True, description="Build Conduit utilities")

    # variants for python support
    variant("python", default=False, description="Build Conduit Python support")
    variant("fortran", default=True, description="Build Conduit Fortran support")

    # variants for comm and i/o
    variant("mpi", default=True, description="Build Conduit MPI Support")
    # set to false for systems that implicitly link mpi
    variant("blt_find_mpi", default=True, description="Use BLT CMake Find MPI logic")
    variant("hdf5", default=True, description="Build Conduit HDF5 support")
    # TODO: remove 'compat' variant when VisIt starts distributing HDF5
    # binaries
    variant(
        "hdf5_compat",
        default=True,
        when="+hdf5",
        description="Build Conduit with HDF5 1.8.x (compatibility mode)",
    )
    variant("silo", default=False, description="Build Conduit Silo support")
    variant("adios", default=False, description="Build Conduit ADIOS support")
    variant("parmetis", default=True, description="Build Conduit Parmetis support")

    # zfp compression
    variant("zfp", default=False, description="Build Conduit ZFP support")

    # variants for dev-tools (docs, etc)
    variant("doc", default=False, description="Build Conduit's documentation")
    # doxygen support is wip, since doxygen has several dependencies
    # we want folks to explicitly opt in to building doxygen
    variant("doxygen", default=False, description="Build Conduit's Doxygen documentation")
    # caliper
    variant("caliper", default=False, description="Build Conduit Caliper support")

    ###########################################################################
    # package dependencies
    ###########################################################################

    #######################
    # BLT
    #######################
    depends_on("blt", type="build")
    depends_on("blt@0.6.2:", type="build", when="@0.9:")

    #######################
    # CMake
    #######################
    # cmake 3.14.1 or newer basic requirement
    depends_on("cmake@3.14.1:", type="build")
    # cmake 3.21.0 or newer for conduit 0.9.0
    depends_on("cmake@3.21.0:", type="build", when="@0.9.0:")

    #######################
    # Python
    #######################
    depends_on("python", when="+python")
    extends("python", when="+python")
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("py-mpi4py", when="+python+mpi", type=("build", "run"))
    depends_on("py-pip", when="+python", type="build")

    #######################
    # I/O Packages
    #######################

    ###############
    # HDF5
    ###############
    depends_on("hdf5", when="+hdf5")
    depends_on("hdf5~shared", when="+hdf5~shared")
    # Require older HDF5 to ensure compatibility with VisIt: see #29132
    depends_on("hdf5@1.8.0:1.8", when="+hdf5+hdf5_compat")

    ###############
    # Silo
    ###############
    # we are not using silo's fortran features
    depends_on("silo+shared", when="+silo+shared")
    depends_on("silo~shared", when="+silo~shared")

    ###############
    # ADIOS
    ###############
    depends_on("adios+mpi~hdf5+shared", when="+adios+mpi+shared")
    depends_on("adios+mpi~hdf5~shared~blosc", when="+adios+mpi~shared")
    depends_on("adios~mpi~hdf5+shared", when="+adios~mpi+shared")
    depends_on("adios~mpi~hdf5~shared~blosc", when="+adios~mpi~shared")

    #######################
    # ZFP
    #######################
    depends_on("zfp  bsws=8", when="+zfp")

    # hdf5 zfp plugin when both hdf5 and zfp are on
    depends_on("h5z-zfp~fortran", when="+hdf5+zfp")

    #######################
    # Parmetis
    #######################
    depends_on("parmetis", when="+parmetis")
    depends_on("metis", when="+parmetis")

    #######################
    # MPI
    #######################
    depends_on("mpi", when="+mpi")

    #######################
    # Caliper
    #######################
    depends_on("caliper", when="+caliper")

    #######################
    # Documentation related
    #######################
    depends_on("py-sphinx", when="+python+doc", type="build")
    depends_on("py-sphinx-rtd-theme", when="+python+doc", type="build")
    depends_on("doxygen", when="+doc+doxygen")

    conflicts("+parmetis", when="~mpi", msg="Parmetis support requires MPI")

    # Tentative patch for fj compiler
    # Cmake will support fj compiler and this patch will be removed
    patch("fj_flags.patch", when="%fj")
    patch("bpparametis.patch", when="@0.8.1")

    # Add missing include for numeric_limits
    # https://github.com/LLNL/conduit/pull/773
    patch(
        "https://github.com/LLNL/conduit/pull/773.patch?full_index=1",
        when="@:0.7.2",
        sha256="784d74942a63acf698c31b39848b46b4b755bf06faa6aa6fb81be61783ec0c30",
    )

    def setup_build_environment(self, env):
        env.set("CTEST_OUTPUT_ON_FAILURE", "1")
        # conduit uses a <=1.10 api version before 0.8
        if "@:0.7 +hdf5" in self.spec and "@1.10:" in self.spec["hdf5"]:
            env.append_flags("CFLAGS", "-DH5_USE_110_API")
            env.append_flags("CXXFLAGS", "-DH5_USE_110_API")

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
            return "https://github.com/LLNL/conduit/releases/download/v{0}/conduit-v{1}-src-with-blt.tar.gz".format(
                v, v
            )
        return url

    ####################################################################
    # Note: cmake, build, and install stages are handled by CMakePackage
    ####################################################################

    # provide cmake args (pass host config as cmake cache file)
    def cmake_args(self):
        host_config = self._get_host_config_path(self.spec)
        options = []
        options.extend(["-C", host_config])
        return options

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        with working_dir("spack-build"):
            print("Running Conduit Unit Tests...")
            make("test")

    # Copy the generated host-config to install directory for downstream use
    @run_before("install")
    def copy_host_config(self):
        src = self._get_host_config_path(self.spec)
        dst = join_path(self.spec.prefix, os.path.basename(src))
        copy(src, dst)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        """
        Checks the spack install of conduit using conduit's
        using-with-cmake example
        """
        print("Checking Conduit installation...")
        spec = self.spec
        install_prefix = spec.prefix
        example_src_dir = join_path(install_prefix, "examples", "conduit", "using-with-cmake")
        print("Checking using-with-cmake example...")
        with working_dir("check-conduit-using-with-cmake-example", create=True):
            cmake_args = ["-DCONDUIT_DIR={0}".format(install_prefix), example_src_dir]
            cmake(*cmake_args)
            make()
            example = Executable("./conduit_example")
            example()
        print("Checking using-with-make example...")
        example_src_dir = join_path(install_prefix, "examples", "conduit", "using-with-make")
        example_files = glob.glob(join_path(example_src_dir, "*"))
        with working_dir("check-conduit-using-with-make-example", create=True):
            for example_file in example_files:
                shutil.copy(example_file, ".")
            make("CONDUIT_DIR={0}".format(install_prefix))
            example = Executable("./conduit_example")
            example()

    def _get_host_config_path(self, spec):
        sys_type = spec.architecture
        # if on llnl systems, we can use the SYS_TYPE
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        host_config_path = "{0}-{1}-{2}-conduit-{3}.cmake".format(
            socket.gethostname(), sys_type, spec.compiler, spec.dag_hash()
        )

        dest_dir = self.stage.source_path
        host_config_path = os.path.abspath(join_path(dest_dir, host_config_path))
        return host_config_path

    @run_before("cmake")
    def hostconfig(self):
        """
        This method creates a 'host-config' file that specifies
        all of the options used to configure and build conduit.

        For more details about 'host-config' files see:
            http://software.llnl.gov/conduit/building.html
        """
        spec = self.spec
        if not os.path.isdir(spec.prefix):
            os.mkdir(spec.prefix)

        #######################
        # Compiler Info
        #######################
        c_compiler = env["SPACK_CC"]
        cpp_compiler = env["SPACK_CXX"]
        if spec.satisfies("+fortran"):
            f_compiler = env["SPACK_FC"]
        else:
            f_compiler = None

        #######################################################################
        # Directly fetch the names of the actual compilers to create a
        # 'host config' file that works outside of the spack install env.
        #######################################################################

        sys_type = spec.architecture
        # if on llnl systems, we can use the SYS_TYPE
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]

        # are we on a specific machine
        on_blueos = "blueos" in sys_type

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

        cfg.write("# fortran compiler used by spack\n")
        if spec.satisfies("+fortran"):
            cfg.write(cmake_cache_entry("ENABLE_FORTRAN", "ON"))
            cfg.write(cmake_cache_entry("CMAKE_Fortran_COMPILER", f_compiler))
        else:
            cfg.write(cmake_cache_entry("ENABLE_FORTRAN", "OFF"))

        if spec.satisfies("+shared"):
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "ON"))
        else:
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "OFF"))

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

        # Add various rpath linker flags
        rpaths = []
        if self.compiler.extra_rpaths:
            rpaths += self.compiler.extra_rpaths

        # Note: This is not needed if we add `extra_rpaths` to this compiler spec case
        if (f_compiler is not None) and ("gfortran" in f_compiler) and ("clang" in cpp_compiler):
            libdir = os.path.join(os.path.dirname(os.path.dirname(f_compiler)), "lib")
            for _libpath in [libdir, libdir + "64"]:
                if os.path.exists(_libpath):
                    rpaths.append(_libpath)

        linkerflags = ""
        for rpath in rpaths:
            linkerflags += "-Wl,-rpath,{} ".format(rpath)
        cfg.write(cmake_cache_entry("CMAKE_EXE_LINKER_FLAGS", linkerflags))
        if spec.satisfies("+shared"):
            cfg.write(cmake_cache_entry("CMAKE_SHARED_LINKER_FLAGS", linkerflags))
        else:
            cfg.write(cmake_cache_entry("CMAKE_STATIC_LINKER_FLAGS", linkerflags))

        #######################
        # BLT
        #######################
        cfg.write(cmake_cache_entry("BLT_SOURCE_DIR", spec["blt"].prefix))

        #######################
        # Examples/Utilities
        #######################
        if spec.satisfies("+examples"):
            cfg.write(cmake_cache_entry("ENABLE_EXAMPLES", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_EXAMPLES", "OFF"))

        if spec.satisfies("+utilities"):
            cfg.write(cmake_cache_entry("ENABLE_UTILS", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_UTILS", "OFF"))

        #######################
        # Unit Tests
        #######################
        if spec.satisfies("+test"):
            cfg.write(cmake_cache_entry("ENABLE_TESTS", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_TESTS", "OFF"))

        # extra fun for blueos
        if on_blueos and "+fortran" in spec and (f_compiler is not None) and ("xlf" in f_compiler):
            # Fix missing std linker flag in xlc compiler
            flags = "-WF,-C! -qxlf2003=polymorphic"
            cfg.write(cmake_cache_entry("BLT_FORTRAN_FLAGS", flags))
            # Grab lib directory for the current fortran compiler
            libdir = os.path.join(os.path.dirname(os.path.dirname(f_compiler)), "lib")
            rpaths = "-Wl,-rpath,{0} -Wl,-rpath,{0}64".format(libdir)

            flags = "${BLT_EXE_LINKER_FLAGS} -lstdc++ " + rpaths
            cfg.write(cmake_cache_entry("BLT_EXE_LINKER_FLAGS", flags))
            if spec.satisfies("+shared"):
                flags = "${CMAKE_SHARED_LINKER_FLAGS} " + rpaths
                cfg.write(cmake_cache_entry("CMAKE_SHARED_LINKER_FLAGS", flags, force=True))

        #######################
        # Python
        #######################

        cfg.write("# Python Support\n")

        if spec.satisfies("+python"):
            cfg.write("# Enable python module builds\n")
            cfg.write(cmake_cache_entry("ENABLE_PYTHON", "ON"))
            cfg.write("# python from spack \n")
            cfg.write(cmake_cache_entry("PYTHON_EXECUTABLE", python.path))
            try:
                cfg.write("# python module install dir\n")
                cfg.write(cmake_cache_entry("PYTHON_MODULE_INSTALL_PREFIX", python_platlib))
            except NameError:
                # spack's  won't exist in a subclass
                pass
        else:
            cfg.write(cmake_cache_entry("ENABLE_PYTHON", "OFF"))

        if spec.satisfies("+doc"):
            if spec.satisfies("+python"):
                cfg.write(cmake_cache_entry("ENABLE_DOCS", "ON"))

                cfg.write("# sphinx from spack \n")
                sphinx_build_exe = join_path(spec["py-sphinx"].prefix.bin, "sphinx-build")
                cfg.write(cmake_cache_entry("SPHINX_EXECUTABLE", sphinx_build_exe))
            if spec.satisfies("+doxygen"):
                cfg.write("# doxygen from uberenv\n")
                doxygen_exe = spec["doxygen"].command.path
                cfg.write(cmake_cache_entry("DOXYGEN_EXECUTABLE", doxygen_exe))
        else:
            cfg.write(cmake_cache_entry("ENABLE_DOCS", "OFF"))

        #######################
        # MPI
        #######################

        cfg.write("# MPI Support\n")

        if spec.satisfies("+mpi"):
            mpicc_path = spec["mpi"].mpicc
            mpicxx_path = spec["mpi"].mpicxx
            mpifc_path = spec["mpi"].mpifc if "+fortran" in spec else None
            # if we are using compiler wrappers on cray systems
            # use those for mpi wrappers, b/c  spec['mpi'].mpicxx
            # etc make return the spack compiler wrappers
            # which can trip up mpi detection in CMake 3.14
            if spec["mpi"].mpicc == spack_cc:
                mpicc_path = c_compiler
                mpicxx_path = cpp_compiler
                mpifc_path = f_compiler
            cfg.write(cmake_cache_entry("ENABLE_MPI", "ON"))
            cfg.write(cmake_cache_entry("MPI_C_COMPILER", mpicc_path))
            cfg.write(cmake_cache_entry("MPI_CXX_COMPILER", mpicxx_path))
            if spec.satisfies("+blt_find_mpi"):
                cfg.write(cmake_cache_entry("ENABLE_FIND_MPI", "ON"))
            else:
                cfg.write(cmake_cache_entry("ENABLE_FIND_MPI", "OFF"))
            if spec.satisfies("+fortran"):
                cfg.write(cmake_cache_entry("MPI_Fortran_COMPILER", mpifc_path))

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

        #######################
        # ZFP
        #######################
        cfg.write("# zfp from spack \n")
        if spec.satisfies("+zfp"):
            cfg.write(cmake_cache_entry("ZFP_DIR", spec["zfp"].prefix))
        else:
            cfg.write("# zfp not built by spack \n")

        #######################
        # Caliper
        #######################
        cfg.write("# caliper from spack \n")
        if spec.satisfies("+caliper"):
            cfg.write(cmake_cache_entry("CALIPER_DIR", spec["caliper"].prefix))
            cfg.write(cmake_cache_entry("ADIAK_DIR", spec["adiak"].prefix))
        else:
            cfg.write("# caliper not built by spack \n")

        #######################################################################
        # I/O Packages
        #######################################################################

        cfg.write("# I/O Packages\n\n")

        #######################
        # HDF5
        #######################

        cfg.write("# hdf5 from spack \n")

        if spec.satisfies("+hdf5"):
            cfg.write(cmake_cache_entry("HDF5_DIR", spec["hdf5"].prefix))
            if spec.satisfies("^zlib-api"):
                # HDF5 depends on zlib
                cfg.write(cmake_cache_entry("ZLIB_DIR", spec["zlib-api"].prefix))
        else:
            cfg.write("# hdf5 not built by spack \n")

        #######################
        # h5z-zfp
        #######################

        cfg.write("# h5z-zfp from spack \n")

        if spec.satisfies("+hdf5+zfp"):
            cfg.write(cmake_cache_entry("H5ZZFP_DIR", spec["h5z-zfp"].prefix))
        else:
            cfg.write("# h5z-zfp not built by spack \n")

        #######################
        # Silo
        #######################

        cfg.write("# silo from spack \n")

        if spec.satisfies("+silo"):
            cfg.write(cmake_cache_entry("SILO_DIR", spec["silo"].prefix))
        else:
            cfg.write("# silo not built by spack \n")

        #######################
        # ADIOS
        #######################

        cfg.write("# ADIOS from spack \n")

        if spec.satisfies("+adios"):
            cfg.write(cmake_cache_entry("ADIOS_DIR", spec["adios"].prefix))
        else:
            cfg.write("# adios not built by spack \n")

        #######################
        # Parmetis
        #######################

        cfg.write("# parmetis from spack \n")

        if spec.satisfies("+parmetis"):
            cfg.write(cmake_cache_entry("METIS_DIR", spec["metis"].prefix))
            cfg.write(cmake_cache_entry("PARMETIS_DIR", spec["parmetis"].prefix))
        else:
            cfg.write("# parmetis not built by spack \n")

        #######################
        # Finish host-config
        #######################
        cfg.write("##################################\n")
        cfg.write("# end spack generated host-config\n")
        cfg.write("##################################\n")
        cfg.close()

        host_cfg_fname = os.path.abspath(host_cfg_fname)
        tty.info("spack generated conduit host-config file: " + host_cfg_fname)
