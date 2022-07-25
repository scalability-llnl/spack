# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import shutil
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


def propagate_cuda_arch(package, spec=None):
    if not spec:
        spec = ''
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on('{0} +cuda cuda_arch={1}'
                   .format(package, cuda_arch),
                   when='{0} +cuda cuda_arch={1}'
                        .format(spec, cuda_arch))


class Ascent(CMakePackage, CudaPackage):
    """Ascent is an open source many-core capable lightweight in situ
    visualization and analysis infrastructure for multi-physics HPC
    simulations."""

    homepage = "https://github.com/Alpine-DAV/ascent"
    git      = "https://github.com/Alpine-DAV/ascent.git"
    url      = "https://github.com/Alpine-DAV/ascent/releases/download/v0.5.1/ascent-v0.5.1-src-with-blt.tar.gz"
    tags     = ['radiuss', 'e4s']

    maintainers = ['cyrush']

    version('develop',
            branch='develop',
            submodules=True)

    version('0.8.0',
            tag='v0.8.0',
            submodules=True,
            preferred=True)

    version('0.7.1',
            tag='v0.7.1',
            submodules=True)

    version('0.7.0',
            tag='v0.7.0',
            submodules=True)

    version('0.6.0',
            tag='v0.6.0',
            submodules=True)

    ###########################################################################
    # package variants
    ###########################################################################

    variant("shared", default=True, description="Build Ascent as shared libs")
    variant('test', default=True, description='Enable Ascent unit tests')

    variant("mpi", default=True, description="Build Ascent MPI Support")
    # set to false for systems that implicitly link mpi
    variant('blt_find_mpi', default=True, description='Use BLT CMake Find MPI logic')
    variant("serial", default=True, description="build serial (non-mpi) libraries")

    # variants for language support
    variant("python", default=False, description="Build Ascent Python support")
    variant("fortran", default=True, description="Build Ascent Fortran support")

    # variants for runtime features
    variant("vtkh", default=True,
            description="Build VTK-h filter and rendering support")

    variant("openmp", default=(sys.platform != 'darwin'),
            description="build openmp support")
    variant("mfem", default=False, description="Build MFEM filter support")
    variant("dray", default=False, description="Build with Devil Ray support")
    variant("adios2", default=False, description="Build Adios2 filter support")
    variant("fides", default=False, description="Build Fides filter support")

    # variants for dev-tools (docs, etc)
    variant("doc", default=False, description="Build Ascent's documentation")

    # variant for BabelFlow runtime
    variant("babelflow", default=False, description="Build with BabelFlow")

    ##########################################################################
    # patches
    ###########################################################################
    # patch for gcc 10 and 11, changes already on develop, here
    # so folks can build 0.7.1 with those compilers
    patch("ascent-gcc-11-pr753.patch", when="@0.7.1")

    # patch for allowing +shared+cuda
    # https://github.com/Alpine-DAV/ascent/pull/903
    patch('ascent-shared-cuda-pr903.patch', when='@0.8.0')
    # patch for finding ADIOS2 more reliably
    # https://github.com/Alpine-DAV/ascent/pull/922
    patch('ascent-find-adios2-pr922.patch', when='@0.8.0')
    # patch for finding Conduit python more reliably
    # https://github.com/Alpine-DAV/ascent/pull/935
    patch('ascent-find-conduit-python-pr935.patch', when='@0.8.0')

    ##########################################################################
    # package dependencies
    ###########################################################################
    # Certain CMake versions have been found to break for our use cases
    depends_on("cmake@3.14.1:3.14,3.18.2:", type='build')

    #######################
    # Conduit
    #######################
    depends_on("conduit@:0.7.2", when="@:0.7.1")
    depends_on("conduit@0.8.2:", when="@0.8:")
    depends_on("conduit+python", when="+python")
    depends_on("conduit~python", when="~python")
    depends_on("conduit+mpi", when="+mpi")
    depends_on("conduit~mpi", when="~mpi")

    #######################
    # Python
    #######################
    # we need a shared version of python b/c linking with static python lib
    # causes duplicate state issues when running compiled python modules.
    with when('+python'):
        depends_on("python+shared")
        extends("python")
        depends_on("py-numpy", type=('build', 'run'))
        depends_on("py-pip", type=('build', 'run'))

    #######################
    # MPI
    #######################
    depends_on("mpi", when="+mpi")
    depends_on("py-mpi4py", when="+mpi+python")

    #######################
    # BabelFlow
    #######################
    depends_on('babelflow', when='+babelflow+mpi')
    depends_on('parallelmergetree', when='+babelflow+mpi')

    #############################
    # TPLs for Runtime Features
    #############################

    depends_on("vtk-h", when="+vtkh")
    depends_on("vtk-h@:0.7", when="@:0.7 +vtkh")
    depends_on("vtk-h@0.8.1:", when="@0.8: +vtkh")
    # propagate relevent variants to vtk-h
    depends_on("vtk-h+openmp", when="+vtkh+openmp")
    depends_on("vtk-h~openmp", when="+vtkh~openmp")
    depends_on("vtk-h+cuda", when="+vtkh+cuda")
    depends_on("vtk-h~cuda", when="+vtkh~cuda")
    propagate_cuda_arch('vtk-h', '+vtkh')
    depends_on("vtk-h+shared", when="+vtkh+shared")
    depends_on("vtk-h~shared", when="+vtkh~shared")
    # When using VTK-h ascent also needs VTK-m
    depends_on("vtk-m@:1.7", when="+vtkh")
    depends_on("vtk-m+testlib", when="+vtkh+test^vtk-m")

    # mfem
    depends_on("mfem~threadsafe~openmp+conduit", when="+mfem")
    # propagate relevent variants to mfem
    depends_on("mfem+mpi", when="+mfem+mpi")
    depends_on("mfem~mpi", when="+mfem~mpi")
    depends_on("mfem+shared", when="+mfem+shared")
    depends_on("mfem~shared", when="+mfem~shared")

    # fides
    depends_on("fides", when="+fides")

    # devil ray variants with mpi
    # we have to specify both because mfem makes us
    depends_on('dray~test~utils', when='+dray')
    depends_on('dray@0.1.8:', when='@0.8: +dray')
    # propagate relevent variants to dray
    depends_on('dray+cuda', when='+dray+cuda')
    depends_on('dray~cuda', when='+dray~cuda')
    propagate_cuda_arch('dray', '+dray')
    depends_on('dray+mpi', when='+dray+mpi')
    depends_on('dray~mpi', when='+dray~mpi')
    depends_on('dray+shared', when='+dray+shared')
    depends_on('dray~shared', when='+dray~shared')
    depends_on('dray+openmp', when='+dray+openmp')
    depends_on('dray~openmp', when='+dray~openmp')

    # Adios2
    depends_on('adios2', when='+adios2')
    # propagate relevent variants to adios2
    depends_on('adios2+mpi', when='+adios2+mpi')
    depends_on('adios2~mpi', when='+adios2~mpi')
    depends_on('adios2+shared', when='+adios2+shared')
    depends_on('adios2~shared', when='+adios2~shared')

    #######################
    # Documentation related
    #######################
    depends_on("py-sphinx", when="+python+doc", type='build')
    depends_on("py-sphinx-rtd-theme", when="+python+doc", type='build')

    ###########
    # Conflicts
    ###########
    conflicts("+shared", when="@:0.7 +cuda",
              msg="Ascent needs to be built with ~shared for CUDA builds.")

    def setup_build_environment(self, env):
        env.set('CTEST_OUTPUT_ON_FAILURE', '1')

    ####################################################################
    # Note: cmake, build, and install stages are handled by CMakePackage
    ####################################################################

    # provide cmake args (pass host config as cmake cache file)
    def cmake_args(self):
        host_config = self._get_host_config_path(self.spec)
        options = []
        options.extend(['-C', host_config, "../spack-src/src/"])
        return options

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):
        """
        Checks the spack install of ascent using ascents's
        using-with-cmake example
        """
        print("Checking Ascent installation...")
        spec = self.spec
        install_prefix = spec.prefix
        example_src_dir = join_path(install_prefix,
                                    "examples",
                                    "ascent",
                                    "using-with-cmake")
        print("Checking using-with-cmake example...")
        with working_dir("check-ascent-using-with-cmake-example",
                         create=True):
            cmake_args = ["-DASCENT_DIR={0}".format(install_prefix),
                          "-DCONDUIT_DIR={0}".format(spec['conduit'].prefix),
                          "-DVTKM_DIR={0}".format(spec['vtk-m'].prefix),
                          "-DVTKH_DIR={0}".format(spec['vtk-h'].prefix),
                          example_src_dir]
            cmake(*cmake_args)
            make()
            example = Executable('./ascent_render_example')
            example()
        print("Checking using-with-make example...")
        example_src_dir = join_path(install_prefix,
                                    "examples",
                                    "ascent",
                                    "using-with-make")
        example_files = glob.glob(join_path(example_src_dir, "*"))
        with working_dir("check-ascent-using-with-make-example",
                         create=True):
            for example_file in example_files:
                shutil.copy(example_file, ".")
            make("ASCENT_DIR={0}".format(install_prefix))
            example = Executable('./ascent_render_example')
            example()

    def _get_host_config_path(self, spec):
        sys_type = spec.architecture
        # if on llnl systems, we can use the SYS_TYPE
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        host_config_path = "{0}-{1}-{2}-ascent-{3}.cmake".format(socket.gethostname(),
                                                                 sys_type,
                                                                 spec.compiler,
                                                                 spec.dag_hash())
        dest_dir = spec.prefix
        host_config_path = os.path.abspath(join_path(dest_dir,
                                                     host_config_path))
        return host_config_path

    @run_before('cmake')
    def hostconfig(self):
        """
        This method creates a 'host-config' file that specifies
        all of the options used to configure and build ascent.

        For more details about 'host-config' files see:
            https://ascent.readthedocs.io/en/latest/BuildingAscent.html

        """
        spec = self.spec
        if not os.path.isdir(spec.prefix):
            os.mkdir(spec.prefix)

        #######################
        # Compiler Info
        #######################
        c_compiler = env["SPACK_CC"]
        cpp_compiler = env["SPACK_CXX"]
        if "+fortran" in spec:
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
        if "+fortran" in spec:
            cfg.write(cmake_cache_entry("ENABLE_FORTRAN", "ON"))
            cfg.write(cmake_cache_entry("CMAKE_Fortran_COMPILER",
                                        f_compiler))
        else:
            cfg.write(cmake_cache_entry("ENABLE_FORTRAN", "OFF"))

        # shared vs static libs
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
        if self.spec.satisfies('%cce'):
            fflags += " -ef"
        if fflags:
            cfg.write(cmake_cache_entry("CMAKE_Fortran_FLAGS", fflags))

        #######################
        # Unit Tests
        #######################
        if "+test" in spec:
            cfg.write(cmake_cache_entry("ENABLE_TESTS", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_TESTS", "OFF"))

        #######################################################################
        # Core Dependencies
        #######################################################################

        #######################
        # Conduit
        #######################

        cfg.write("# conduit from spack \n")
        cfg.write(cmake_cache_entry("CONDUIT_DIR", spec['conduit'].prefix))

        #######################################################################
        # Optional Dependencies
        #######################################################################

        #######################
        # Python
        #######################

        cfg.write("# Python Support\n")

        if "+python" in spec and "+shared" in spec:
            cfg.write("# Enable python module builds\n")
            cfg.write(cmake_cache_entry("ENABLE_PYTHON", "ON"))
            cfg.write("# python from spack \n")
            cfg.write(cmake_cache_entry("PYTHON_EXECUTABLE",
                      spec['python'].command.path))
            try:
                cfg.write("# python module install dir\n")
                cfg.write(cmake_cache_entry("PYTHON_MODULE_INSTALL_PREFIX",
                          python_platlib))
            except NameError:
                # spack's  won't exist in a subclass
                pass
        else:
            cfg.write(cmake_cache_entry("ENABLE_PYTHON", "OFF"))

        if "+doc" in spec and "+python" in spec:
            cfg.write(cmake_cache_entry("ENABLE_DOCS", "ON"))

            cfg.write("# sphinx from spack \n")
            sphinx_build_exe = join_path(spec['py-sphinx'].prefix.bin,
                                         "sphinx-build")
            cfg.write(cmake_cache_entry("SPHINX_EXECUTABLE", sphinx_build_exe))
        else:
            cfg.write(cmake_cache_entry("ENABLE_DOCS", "OFF"))

        #######################
        # Serial
        #######################

        if "+serial" in spec:
            cfg.write(cmake_cache_entry("ENABLE_SERIAL", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_SERIAL", "OFF"))

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

            if "+blt_find_mpi" in spec:
                cfg.write(cmake_cache_entry("ENABLE_FIND_MPI", "ON"))
            else:
                cfg.write(cmake_cache_entry("ENABLE_FIND_MPI", "OFF"))
            ###################################
            # BABELFLOW (also depends on mpi)
            ###################################
            if "+babelflow" in spec:
                cfg.write(cmake_cache_entry("ENABLE_BABELFLOW", "ON"))
                cfg.write(cmake_cache_entry("BabelFlow_DIR",
                                            spec['babelflow'].prefix))
                cfg.write(cmake_cache_entry("PMT_DIR",
                                            spec['parallelmergetree'].prefix))
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

        if "+openmp" in spec:
            cfg.write(cmake_cache_entry("ENABLE_OPENMP", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_OPENMP", "OFF"))

        #######################
        # VTK-h (and deps)
        #######################

        cfg.write("# vtk-h support \n")

        if "+vtkh" in spec:
            cfg.write("# vtk-m from spack\n")
            cfg.write(cmake_cache_entry("VTKM_DIR", spec['vtk-m'].prefix))

            cfg.write("# vtk-h from spack\n")
            cfg.write(cmake_cache_entry("VTKH_DIR", spec['vtk-h'].prefix))

            if "+cuda" in spec:
                cfg.write(cmake_cache_entry("VTKm_ENABLE_CUDA", "ON"))
                cfg.write(cmake_cache_entry("CMAKE_CUDA_HOST_COMPILER",
                          env["SPACK_CXX"]))
            else:
                cfg.write(cmake_cache_entry("VTKm_ENABLE_CUDA", "OFF"))

        else:
            cfg.write("# vtk-h not built by spack \n")

        #######################
        # MFEM
        #######################
        if "+mfem" in spec:
            cfg.write("# mfem from spack \n")
            cfg.write(cmake_cache_entry("MFEM_DIR", spec['mfem'].prefix))
        else:
            cfg.write("# mfem not built by spack \n")

        #######################
        # Devil Ray
        #######################
        if "+dray" in spec:
            cfg.write("# devil ray from spack \n")
            cfg.write(cmake_cache_entry("DRAY_DIR", spec['dray'].prefix))
        else:
            cfg.write("# devil ray not built by spack \n")

        #######################
        # Adios2
        #######################
        cfg.write("# adios2 support\n")

        if "+adios2" in spec:
            cfg.write(cmake_cache_entry("ADIOS2_DIR", spec['adios2'].prefix))
        else:
            cfg.write("# adios2 not built by spack \n")

        #######################
        # Fides
        #######################
        cfg.write("# Fides support\n")

        if "+fides" in spec:
            cfg.write(cmake_cache_entry("FIDES_DIR", spec['fides'].prefix))
        else:
            cfg.write("# fides not built by spack \n")

        #######################
        # Finish host-config
        #######################

        cfg.write("##################################\n")
        cfg.write("# end spack generated host-config\n")
        cfg.write("##################################\n")
        cfg.close()

        host_cfg_fname = os.path.abspath(host_cfg_fname)
        tty.info("spack generated ascent host-config file: " + host_cfg_fname)
