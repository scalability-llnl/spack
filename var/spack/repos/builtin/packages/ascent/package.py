# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

import sys
import os
import socket
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


class Ascent(Package, CudaPackage):
    """Ascent is an open source many-core capable lightweight in situ
    visualization and analysis infrastructure for multi-physics HPC
    simulations."""

    homepage = "https://github.com/Alpine-DAV/ascent"
    git      = "https://github.com/Alpine-DAV/ascent.git"
    url      = "https://github.com/Alpine-DAV/ascent/releases/download/v0.5.1/ascent-v0.5.1-src-with-blt.tar.gz"

    maintainers = ['cyrush']

    version('develop',
            branch='develop',
            submodules=True)

    version('0.7.0',
            tag='v0.7.0',
            submodules=True,
            preferred=True)

    version('0.6.0',
            tag='v0.6.0',
            submodules=True)

    ###########################################################################
    # package variants
    ###########################################################################

    variant("shared", default=True, description="Build Ascent as shared libs")
    variant('test', default=True, description='Enable Ascent unit tests')

    variant("mpi", default=True, description="Build Ascent MPI Support")
    variant("serial", default=True, description="build serial (non-mpi) libraries")

    # variants for language support
    variant("python", default=False, description="Build Ascent Python support")
    variant("fortran", default=True, description="Build Ascent Fortran support")

    # variants for runtime features
    variant("vtkh", default=True,
            description="Build VTK-h filter and rendering support")

    variant("openmp", default=(sys.platform != 'darwin'),
            description="build openmp support")
    variant("cuda", default=False, description="Build cuda support")
    variant("mfem", default=False, description="Build MFEM filter support")
    variant("adios", default=False, description="Build Adios filter support")
    variant("dray", default=False, description="Build with Devil Ray support")

    # variants for dev-tools (docs, etc)
    variant("doc", default=False, description="Build Ascent's documentation")

    # variant for BabelFlow runtime
    variant("babelflow", default=False, description="Build with BabelFlow")

    ##########################################################################
    # package dependencies
    ###########################################################################

    # Certain CMake versions have been found to break for our use cases
    depends_on("cmake@3.14.1:3.14.99,3.18.2:", type='build')
    depends_on("conduit~python", when="~python")
    depends_on("conduit+python", when="+python+shared")
    depends_on("conduit~shared~python", when="~shared")
    depends_on("conduit~python~mpi", when="~python~mpi")
    depends_on("conduit+python~mpi", when="+python+shared~mpi")
    depends_on("conduit~shared~python~mpi", when="~shared~mpi")

    #######################
    # Python
    #######################
    # we need a shared version of python b/c linking with static python lib
    # causes duplicate state issues when running compiled python modules.
    depends_on("python+shared", when="+python+shared")
    extends("python", when="+python+shared")
    depends_on("py-numpy", when="+python+shared", type=('build', 'run'))
    depends_on("py-pip", when="+python+shared", type=('build', 'run'))

    #######################
    # MPI
    #######################
    depends_on("mpi", when="+mpi")
    depends_on("py-mpi4py", when="+mpi+python+shared")

    #######################
    # BabelFlow
    #######################
    depends_on('babelflow', when='+babelflow+mpi')
    depends_on('parallelmergetree', when='+babelflow+mpi')

    #############################
    # TPLs for Runtime Features
    #############################

    depends_on("vtk-h",             when="+vtkh")
    depends_on("vtk-h~openmp",      when="+vtkh~openmp")
    depends_on("vtk-h+cuda+openmp", when="+vtkh+cuda+openmp")
    depends_on("vtk-h+cuda~openmp", when="+vtkh+cuda~openmp")

    depends_on("vtk-h~shared",             when="~shared+vtkh")
    depends_on("vtk-h~shared~openmp",      when="~shared+vtkh~openmp")
    depends_on("vtk-h~shared+cuda",        when="~shared+vtkh+cuda")
    depends_on("vtk-h~shared+cuda~openmp", when="~shared+vtkh+cuda~openmp")

    # mfem
    depends_on("mfem~threadsafe~openmp+shared+mpi+conduit", when="+shared+mfem+mpi")
    depends_on("mfem~threadsafe~openmp~shared+mpi+conduit", when="~shared+mfem+mpi")

    depends_on("mfem~threadsafe~openmp+shared~mpi+conduit", when="+shared+mfem~mpi")
    depends_on("mfem~threadsafe~openmp~shared~mpi+conduit", when="~shared+mfem~mpi")

    depends_on("adios", when="+adios")

    # devil ray variants with mpi
    # we have to specify both because mfem makes us
    depends_on("dray+mpi~test~utils+shared+cuda",        when="+dray+mpi+cuda+shared")
    depends_on("dray+mpi~test~utils+shared+openmp",      when="+dray+mpi+openmp+shared")
    depends_on("dray+mpi~test~utils+shared~openmp~cuda", when="+dray+mpi~openmp~cuda+shared")

    depends_on("dray+mpi~test~utils~shared+cuda",        when="+dray+mpi+cuda~shared")
    depends_on("dray+mpi~test~utils~shared+openmp",      when="+dray+mpi+openmp~shared")
    depends_on("dray+mpi~test~utils~shared~openmp~cuda", when="+dray+mpi~openmp~cuda~shared")

    # devil ray variants without mpi
    depends_on("dray~mpi~test~utils+shared+cuda",        when="+dray~mpi+cuda+shared")
    depends_on("dray~mpi~test~utils+shared+openmp",      when="+dray~mpi+openmp+shared")
    depends_on("dray~mpi~test~utils+shared~openmp~cuda", when="+dray~mpi~openmp~cuda+shared")

    depends_on("dray~mpi~test~utils~shared+cuda",        when="+dray~mpi+cuda~shared")
    depends_on("dray~mpi~test~utils~shared+openmp",      when="+dray~mpi+openmp~shared")
    depends_on("dray~mpi~test~utils~shared~openmp~cuda", when="+dray~mpi~openmp~cuda~shared")

    #######################
    # Documentation related
    #######################
    depends_on("py-sphinx", when="+python+doc", type='build')
    depends_on("py-sphinx-rtd-theme", when="+python+doc", type='build')

    ###########
    # Conflicts
    ###########
    conflicts("+shared", when="+cuda",
              msg="Ascent needs to be built with ~shared for CUDA builds.")

    def setup_build_environment(self, env):
        env.set('CTEST_OUTPUT_ON_FAILURE', '1')

    def install(self, spec, prefix):
        """
        Build and install Ascent.
        """
        with working_dir('spack-build', create=True):
            py_site_pkgs_dir = None
            if "+python" in spec:
                py_site_pkgs_dir = site_packages_dir

            host_cfg_fname = self.create_host_config(spec,
                                                     prefix,
                                                     py_site_pkgs_dir)
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
            print("Configuring Ascent...")
            cmake(*cmake_args)
            print("Building Ascent...")
            make()
            # run unit tests if requested
            if "+test" in spec and self.run_tests:
                print("Running Ascent Unit Tests...")
                make("test")
            print("Installing Ascent...")
            make("install")
            # install copy of host config for provenance
            install(host_cfg_fname, prefix)

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

    def create_host_config(self, spec, prefix, py_site_pkgs_dir=None):
        """
        This method creates a 'host-config' file that specifies
        all of the options used to configure and build ascent.

        For more details about 'host-config' files see:
            http://ascent.readthedocs.io/en/latest/BuildingAscent.html

        Note:
          The `py_site_pkgs_dir` arg exists to allow a package that
          subclasses this package provide a specific site packages
          dir when calling this function. `py_site_pkgs_dir` should
          be an absolute path or `None`.

          This is necessary because the spack `site_packages_dir`
          var will not exist in the base class. For more details
          on this issue see: https://github.com/spack/spack/issues/6261
        """

        #######################
        # Compiler Info
        #######################
        c_compiler = env["SPACK_CC"]
        cpp_compiler = env["SPACK_CXX"]
        f_compiler = None

        if self.compiler.fc:
            # even if this is set, it may not exist so do one more sanity check
            f_compiler = env["SPACK_FC"]

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

        host_cfg_fname = "%s-%s-%s-ascent.cmake" % (socket.gethostname(),
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

        cfg.write("# fortran compiler used by spack\n")
        if "+fortran" in spec and f_compiler is not None:
            cfg.write(cmake_cache_entry("ENABLE_FORTRAN", "ON"))
            cfg.write(cmake_cache_entry("CMAKE_Fortran_COMPILER",
                                        f_compiler))
        else:
            cfg.write("# no fortran compiler found\n\n")
            cfg.write(cmake_cache_entry("ENABLE_FORTRAN", "OFF"))

        # shared vs static libs
        if "+shared" in spec:
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "ON"))
        else:
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "OFF"))

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
            # only set dest python site packages dir if passed
            if py_site_pkgs_dir:
                cfg.write(cmake_cache_entry("PYTHON_MODULE_INSTALL_PREFIX",
                                            py_site_pkgs_dir))
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
        # Adios
        #######################

        cfg.write("# adios support\n")

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
        return host_cfg_fname
