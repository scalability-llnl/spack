# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import socket
from os.path import join as pjoin

import llnl.util.tty as tty
from spack.package import *


def cmake_cache_entry(name, value, comment=""):
    """Generate a string for a cmake cache variable"""
    return 'set({0} "{1}" CACHE PATH "{2}")\n\n'.format(name, value, comment)


def cmake_cache_option(name, boolean_value, comment=""):
    """Generate a string for a cmake configuration option"""

    value = "ON" if boolean_value else "OFF"
    return 'set({0} {1} CACHE BOOL "{2}")\n\n'.format(name, value, comment)


def get_spec_path(spec, package_name, path_replacements={}, use_bin=False):
    """Extracts the prefix path for the given spack package
       path_replacements is a dictionary with string replacements for the path.
    """

    if not use_bin:
        path = spec[package_name].prefix
    else:
        path = spec[package_name].prefix.bin

    path = os.path.realpath(path)

    for key in path_replacements:
        path = path.replace(key, path_replacements[key])

    return path


class Axom(CMakePackage, CudaPackage):
    """Axom provides a robust, flexible software infrastructure for the development
       of multi-physics applications and computational tools."""

    maintainers = ['white238']

    homepage = "https://github.com/LLNL/axom"
    git      = "https://github.com/LLNL/axom.git"

    version('main', branch='main', submodules=True)
    version('develop', branch='develop', submodules=True)
    version('0.4.0', tag='v0.4.0', submodules=True)
    version('0.3.3', tag='v0.3.3', submodules=True)
    version('0.3.2', tag='v0.3.2', submodules=True)
    version('0.3.1', tag='v0.3.1', submodules=True)
    version('0.3.0', tag='v0.3.0', submodules=True)
    version('0.2.9', tag='v0.2.9', submodules=True)

    phases = ["hostconfig", "cmake", "build", "install"]
    root_cmakelists_dir = 'src'

    # -----------------------------------------------------------------------
    # Variants
    # -----------------------------------------------------------------------
    variant('shared',   default=True,
            description='Enable build of shared libraries')
    variant('debug',    default=False,
            description='Build debug instead of optimized version')

    variant('cpp14',  default=True, description="Build with C++14 support")

    variant('fortran',  default=True, description="Build with Fortran support")

    variant("python",   default=False, description="Build python support")

    variant("mpi",      default=True, description="Build MPI support")
    variant('openmp',   default=True, description='Turn on OpenMP support.')

    variant("mfem",     default=False, description="Build with mfem")
    variant("hdf5",     default=True, description="Build with hdf5")
    variant("lua",      default=True, description="Build with Lua")
    variant("scr",      default=False, description="Build with SCR")
    variant("umpire",   default=True, description="Build with umpire")

    variant("raja",     default=True, description="Build with raja")

    varmsg = "Build development tools (such as Sphinx, Doxygen, etc...)"
    variant("devtools", default=False, description=varmsg)

    # -----------------------------------------------------------------------
    # Dependencies
    # -----------------------------------------------------------------------
    # Basics
    depends_on("cmake@3.8.2:", type='build')
    depends_on("mpi", when="+mpi")

    # Libraries
    depends_on("conduit+python", when="+python")
    depends_on("conduit~python", when="~python")
    depends_on("conduit+hdf5", when="+hdf5")
    depends_on("conduit~hdf5", when="~hdf5")

    # HDF5 needs to be the same as Conduit's
    depends_on("hdf5@1.8.19:1.8.999~cxx~shared~fortran", when="+hdf5")

    depends_on("lua", when="+lua")

    depends_on("scr", when="+scr")

    depends_on("raja~openmp", when="+raja~openmp")
    depends_on("raja+openmp", when="+raja+openmp")
    depends_on("raja+cuda", when="+raja+cuda")

    depends_on("umpire~openmp", when="+umpire~openmp")
    depends_on("umpire+openmp", when="+umpire+openmp")
    depends_on("umpire+cuda+deviceconst", when="+umpire+cuda")

    for sm_ in CudaPackage.cuda_arch_values:
        depends_on('raja cuda_arch={0}'.format(sm_),
                   when='+raja cuda_arch={0}'.format(sm_))
        depends_on('umpire cuda_arch={0}'.format(sm_),
                   when='+umpire cuda_arch={0}'.format(sm_))

    depends_on("mfem", when="+mfem")
    depends_on("mfem~mpi", when="+mfem~mpi")

    depends_on("python", when="+python")

    # Devtools
    depends_on("cppcheck", when="+devtools")
    depends_on("doxygen", when="+devtools")
    depends_on("graphviz", when="+devtools")
    depends_on("python", when="+devtools")
    depends_on("py-sphinx", when="+devtools")
    depends_on("py-shroud", when="+devtools")
    depends_on("llvm+clang@10.0.0", when="+devtools", type='build')

    def flag_handler(self, name, flags):
        if name in ('cflags', 'cxxflags', 'fflags'):
            # the package manages these flags in another way
            return (None, None, None)
        return (flags, None, None)

    def _get_sys_type(self, spec):
        sys_type = spec.architecture
        # if on llnl systems, we can use the SYS_TYPE
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        return sys_type

    def _get_host_config_path(self, spec):
        hostname = socket.gethostname()
        if "SYS_TYPE" in env:
            # Are we on a LLNL system then strip node number
            hostname = hostname.rstrip('1234567890')
        filename = "{0}-{1}-{2}.cmake".format(hostname,
                                              self._get_sys_type(spec),
                                              spec.compiler)
        dest_dir = self.stage.source_path
        fullpath = os.path.abspath(pjoin(dest_dir, filename))
        return fullpath

    def hostconfig(self, spec, prefix):
        """
        This method creates a 'host-config' file that specifies
        all of the options used to configure and build Axom.
        """

        c_compiler   = env["SPACK_CC"]
        cpp_compiler = env["SPACK_CXX"]
        f_compiler   = None

        # see if we should enable fortran support
        if "SPACK_FC" in env.keys():
            # even if this is set, it may not exist
            # do one more sanity check
            if os.path.isfile(env["SPACK_FC"]):
                f_compiler  = env["SPACK_FC"]

        # cmake
        if "+cmake" in spec:
            cmake_exe = pjoin(spec['cmake'].prefix.bin, "cmake")
        else:
            cmake_exe = which("cmake")
            if cmake_exe is None:
                # error could not find cmake!
                crash()
            cmake_exe = cmake_exe.command
        cmake_exe = os.path.realpath(cmake_exe)

        host_config_path = self._get_host_config_path(spec)
        cfg = open(host_config_path, "w")
        cfg.write("#------------------{0}\n".format("-" * 60))
        cfg.write("# !!!! This is a generated file, edit at own risk !!!!\n")
        cfg.write("#------------------{0}\n".format("-" * 60))
        cfg.write("# SYS_TYPE: {0}\n".format(self._get_sys_type(spec)))
        cfg.write("# Compiler Spec: {0}\n".format(spec.compiler))
        cfg.write("#------------------{0}\n".format("-" * 60))
        # show path to cmake for reference and to be used by config-build.py
        cfg.write("# CMake executable path: {0}\n".format(cmake_exe))
        cfg.write("#------------------{0}\n\n".format("-" * 60))

        # compiler settings
        cfg.write("#------------------{0}\n".format("-" * 60))
        cfg.write("# Compilers\n")
        cfg.write("#------------------{0}\n\n".format("-" * 60))

        cfg.write(cmake_cache_entry("CMAKE_C_COMPILER", c_compiler))
        cfg.write(cmake_cache_entry("CMAKE_CXX_COMPILER", cpp_compiler))

        if "+fortran" in spec or f_compiler is not None:
            cfg.write(cmake_cache_option("ENABLE_FORTRAN", True))
            cfg.write(cmake_cache_entry("CMAKE_Fortran_COMPILER", f_compiler))
        else:
            cfg.write(cmake_cache_option("ENABLE_FORTRAN", False))

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
            libdir = pjoin(os.path.dirname(
                           os.path.dirname(cpp_compiler)), "lib")
            flags = ""
            for _libpath in [libdir, libdir + "64"]:
                if os.path.exists(_libpath):
                    flags += " -Wl,-rpath,{0}".format(_libpath)
            description = ("Adds a missing libstdc++ rpath")
            if flags:
                cfg.write(cmake_cache_entry("BLT_EXE_LINKER_FLAGS", flags,
                                            description))

        if "+cpp14" in spec:
            cfg.write(cmake_cache_entry("BLT_CXX_STD", "c++14", ""))

        # TPL locations
        cfg.write("#------------------{0}\n".format("-" * 60))
        cfg.write("# TPLs\n")
        cfg.write("#------------------{0}\n\n".format("-" * 60))

        # Try to find the common prefix of the TPL directory, including the
        # compiler. If found, we will use this in the TPL paths
        compiler_str = str(spec.compiler).replace('@', '-')
        prefix_paths = prefix.split(compiler_str)
        path_replacements = {}

        if len(prefix_paths) == 2:
            tpl_root = os.path.realpath(pjoin(prefix_paths[0], compiler_str))
            path_replacements[tpl_root] = "${TPL_ROOT}"
            cfg.write("# Root directory for generated TPLs\n")
            cfg.write(cmake_cache_entry("TPL_ROOT", tpl_root))

        conduit_dir = get_spec_path(spec, "conduit", path_replacements)
        cfg.write(cmake_cache_entry("CONDUIT_DIR", conduit_dir))

        # optional tpls

        if "+mfem" in spec:
            mfem_dir = get_spec_path(spec, "mfem", path_replacements)
            cfg.write(cmake_cache_entry("MFEM_DIR", mfem_dir))
        else:
            cfg.write("# MFEM not built\n\n")

        if "+hdf5" in spec:
            hdf5_dir = get_spec_path(spec, "hdf5", path_replacements)
            cfg.write(cmake_cache_entry("HDF5_DIR", hdf5_dir))
        else:
            cfg.write("# HDF5 not built\n\n")

        if "+lua" in spec:
            lua_dir = get_spec_path(spec, "lua", path_replacements)
            cfg.write(cmake_cache_entry("LUA_DIR", lua_dir))
        else:
            cfg.write("# Lua not built\n\n")

        if "+scr" in spec:
            scr_dir = get_spec_path(spec, "scr", path_replacements)
            cfg.write(cmake_cache_entry("SCR_DIR", scr_dir))
        else:
            cfg.write("# SCR not built\n\n")

        if "+raja" in spec:
            raja_dir = get_spec_path(spec, "raja", path_replacements)
            cfg.write(cmake_cache_entry("RAJA_DIR", raja_dir))
        else:
            cfg.write("# RAJA not built\n\n")

        if "+umpire" in spec:
            umpire_dir = get_spec_path(spec, "umpire", path_replacements)
            cfg.write(cmake_cache_entry("UMPIRE_DIR", umpire_dir))
        else:
            cfg.write("# Umpire not built\n\n")

        cfg.write("#------------------{0}\n".format("-" * 60))
        cfg.write("# MPI\n")
        cfg.write("#------------------{0}\n\n".format("-" * 60))

        if "+mpi" in spec:
            cfg.write(cmake_cache_option("ENABLE_MPI", True))
            cfg.write(cmake_cache_entry("MPI_C_COMPILER", spec['mpi'].mpicc))
            cfg.write(cmake_cache_entry("MPI_CXX_COMPILER",
                                        spec['mpi'].mpicxx))
            if "+fortran" in spec or f_compiler is not None:
                cfg.write(cmake_cache_entry("MPI_Fortran_COMPILER",
                                            spec['mpi'].mpifc))

            # Check for slurm
            using_slurm = False
            slurm_checks = ['+slurm',
                            'schedulers=slurm',
                            'process_managers=slurm']
            if any(spec['mpi'].satisfies(variant) for variant in slurm_checks):
                using_slurm = True

            # Determine MPIEXEC
            if using_slurm:
                if spec['mpi'].external:
                    mpiexec = '/usr/bin/srun'
                else:
                    mpiexec = os.path.join(spec['slurm'].prefix.bin, 'srun')
            else:
                mpiexec = os.path.join(spec['mpi'].prefix.bin, 'mpirun')
                if not os.path.exists(mpiexec):
                    mpiexec = os.path.join(spec['mpi'].prefix.bin, 'mpiexec')

            if not os.path.exists(mpiexec):
                msg = "Unable to determine MPIEXEC, Axom tests may fail"
                cfg.write("# {0}\n\n".format(msg))
                tty.msg(msg)
            else:
                # starting with cmake 3.10, FindMPI expects MPIEXEC_EXECUTABLE
                # vs the older versions which expect MPIEXEC
                if self.spec["cmake"].satisfies('@3.10:'):
                    cfg.write(cmake_cache_entry("MPIEXEC_EXECUTABLE", mpiexec))
                else:
                    cfg.write(cmake_cache_entry("MPIEXEC", mpiexec))

            # Determine MPIEXEC_NUMPROC_FLAG
            if using_slurm:
                cfg.write(cmake_cache_entry("MPIEXEC_NUMPROC_FLAG", "-n"))
            else:
                cfg.write(cmake_cache_entry("MPIEXEC_NUMPROC_FLAG", "-np"))

            if spec['mpi'].name == 'spectrum-mpi':
                cfg.write(cmake_cache_entry("BLT_MPI_COMMAND_APPEND",
                                            "mpibind"))
        else:
            cfg.write(cmake_cache_option("ENABLE_MPI", False))

        ##################################
        # Devtools
        ##################################

        cfg.write("#------------------{0}\n".format("-" * 60))
        cfg.write("# Devtools\n")
        cfg.write("#------------------{0}\n\n".format("-" * 60))

        # Add common prefix to path replacement list
        if "+devtools" in spec:
            # Grab common devtools root and strip the trailing slash
            path1 = os.path.realpath(spec["cppcheck"].prefix)
            path2 = os.path.realpath(spec["doxygen"].prefix)
            devtools_root = os.path.commonprefix([path1, path2])[:-1]
            path_replacements[devtools_root] = "${DEVTOOLS_ROOT}"
            cfg.write("# Root directory for generated developer tools\n")
            cfg.write(cmake_cache_entry("DEVTOOLS_ROOT", devtools_root))

        if "+python" in spec or "+devtools" in spec:
            python_path = os.path.realpath(spec['python'].command.path)
            for key in path_replacements:
                python_path = python_path.replace(key, path_replacements[key])
            cfg.write(cmake_cache_entry("PYTHON_EXECUTABLE", python_path))

        if "doxygen" in spec or "py-sphinx" in spec:
            cfg.write(cmake_cache_option("ENABLE_DOCS", True))

            if "doxygen" in spec:
                doxygen_bin_dir = get_spec_path(spec, "doxygen",
                                                path_replacements,
                                                use_bin=True)
                cfg.write(cmake_cache_entry("DOXYGEN_EXECUTABLE",
                                            pjoin(doxygen_bin_dir,
                                                  "doxygen")))

            if "py-sphinx" in spec:
                python_bin_dir = get_spec_path(spec, "python",
                                               path_replacements,
                                               use_bin=True)
                cfg.write(cmake_cache_entry("SPHINX_EXECUTABLE",
                                            pjoin(python_bin_dir,
                                                  "sphinx-build")))
        else:
            cfg.write(cmake_cache_option("ENABLE_DOCS", False))

        if "py-shroud" in spec:
            shroud_bin_dir = get_spec_path(spec, "py-shroud",
                                           path_replacements, use_bin=True)
            cfg.write(cmake_cache_entry("SHROUD_EXECUTABLE",
                                        pjoin(shroud_bin_dir, "shroud")))

        if "cppcheck" in spec:
            cppcheck_bin_dir = get_spec_path(spec, "cppcheck",
                                             path_replacements, use_bin=True)
            cfg.write(cmake_cache_entry("CPPCHECK_EXECUTABLE",
                                        pjoin(cppcheck_bin_dir, "cppcheck")))

        # Only turn on clangformat support if devtools is on
        if "+devtools" in spec:
            clang_fmt_path = spec['llvm'].prefix.bin.join('clang-format')
            cfg.write(cmake_cache_entry("CLANGFORMAT_EXECUTABLE",
                                        clang_fmt_path))
        else:
            cfg.write("# ClangFormat disabled due to disabled devtools\n")
            cfg.write(cmake_cache_option("ENABLE_CLANGFORMAT", False))

        ##################################
        # Other machine specifics
        ##################################

        cfg.write("#------------------{0}\n".format("-" * 60))
        cfg.write("# Other machine specifics\n")
        cfg.write("#------------------{0}\n\n".format("-" * 60))

        # OpenMP
        if "+openmp" in spec:
            cfg.write(cmake_cache_option("ENABLE_OPENMP", True))
        else:
            cfg.write(cmake_cache_option("ENABLE_OPENMP", False))

        # Enable death tests
        if spec.satisfies('target=ppc64le:') and "+cuda" in spec:
            cfg.write(cmake_cache_option("ENABLE_GTEST_DEATH_TESTS", False))
        else:
            cfg.write(cmake_cache_option("ENABLE_GTEST_DEATH_TESTS", True))

        # Override XL compiler family
        familymsg = ("Override to proper compiler family for XL")
        if (f_compiler is not None) and ("xlf" in f_compiler):
            cfg.write(cmake_cache_entry("CMAKE_Fortran_COMPILER_ID", "XL",
                                        familymsg))
        if "xlc" in c_compiler:
            cfg.write(cmake_cache_entry("CMAKE_C_COMPILER_ID", "XL",
                                        familymsg))
        if "xlC" in cpp_compiler:
            cfg.write(cmake_cache_entry("CMAKE_CXX_COMPILER_ID", "XL",
                                        familymsg))

        if spec.satisfies('target=ppc64le:'):
            if (f_compiler is not None) and ("xlf" in f_compiler):
                description = ("Converts C-style comments to Fortran style "
                               "in preprocessed files")
                cfg.write(cmake_cache_entry("BLT_FORTRAN_FLAGS",
                                            "-WF,-C!  -qxlf2003=polymorphic",
                                            description))
                # Grab lib directory for the current fortran compiler
                libdir = os.path.join(os.path.dirname(
                                      os.path.dirname(f_compiler)), "lib")
                description = ("Adds a missing rpath for libraries "
                               "associated with the fortran compiler")
                linker_flags = "${BLT_EXE_LINKER_FLAGS} -Wl,-rpath," + libdir
                cfg.write(cmake_cache_entry("BLT_EXE_LINKER_FLAGS",
                                            linker_flags, description))
                if "+shared" in spec:
                    linker_flags = "${CMAKE_SHARED_LINKER_FLAGS} -Wl,-rpath," \
                                   + libdir
                    cfg.write(cmake_cache_entry("CMAKE_SHARED_LINKER_FLAGS",
                                                linker_flags, description))

            if "+cuda" in spec:
                cfg.write("#------------------{0}\n".format("-" * 60))
                cfg.write("# Cuda\n")
                cfg.write("#------------------{0}\n\n".format("-" * 60))

                cfg.write(cmake_cache_option("ENABLE_CUDA", True))

                cudatoolkitdir = spec['cuda'].prefix
                cfg.write(cmake_cache_entry("CUDA_TOOLKIT_ROOT_DIR",
                                            cudatoolkitdir))
                cudacompiler = "${CUDA_TOOLKIT_ROOT_DIR}/bin/nvcc"
                cfg.write(cmake_cache_entry("CMAKE_CUDA_COMPILER",
                                            cudacompiler))

                cfg.write(cmake_cache_option("CUDA_SEPARABLE_COMPILATION",
                                             True))

                cfg.write(cmake_cache_option("AXOM_ENABLE_ANNOTATIONS", True))

                # CUDA_FLAGS
                cudaflags  = "-restrict "

                if not spec.satisfies('cuda_arch=none'):
                    cuda_arch = spec.variants['cuda_arch'].value
                    axom_arch = 'sm_{0}'.format(cuda_arch[0])
                    cfg.write(cmake_cache_entry("AXOM_CUDA_ARCH", axom_arch))
                    cudaflags += "-arch ${AXOM_CUDA_ARCH} "
                else:
                    cfg.write("# cuda_arch could not be determined\n\n")

                cudaflags += "-std=c++11 --expt-extended-lambda -G "
                cfg.write(cmake_cache_entry("CMAKE_CUDA_FLAGS", cudaflags))

                if "+mpi" in spec:
                    cfg.write(cmake_cache_entry("CMAKE_CUDA_HOST_COMPILER",
                                                "${MPI_CXX_COMPILER}"))
                else:
                    cfg.write(cmake_cache_entry("CMAKE_CUDA_HOST_COMPILER",
                                                "${CMAKE_CXX_COMPILER}"))

                cfg.write("# nvcc does not like gtest's 'pthreads' flag\n")
                cfg.write(cmake_cache_option("gtest_disable_pthreads", True))

        cfg.write("\n")
        cfg.close()
        tty.info("Spack generated Axom host-config file: " + host_config_path)

    def cmake_args(self):
        spec = self.spec
        host_config_path = self._get_host_config_path(spec)

        options = []
        options.extend(['-C', host_config_path])

        if self.run_tests is False:
            options.append('-DENABLE_TESTS=OFF')
        else:
            options.append('-DENABLE_TESTS=ON')

        if "+shared" in spec:
            options.append('-DBUILD_SHARED_LIBS=ON')
        else:
            options.append('-DBUILD_SHARED_LIBS=OFF')

        return options

    @run_after('install')
    def install_cmake_cache(self):
        install(self._get_host_config_path(self.spec), prefix)
