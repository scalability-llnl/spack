# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
        spec = ""
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on(
            "{0} +cuda cuda_arch={1}".format(package, cuda_arch),
            when="{0} +cuda cuda_arch={1}".format(spec, cuda_arch),
        )


class Ascent(CMakePackage, CudaPackage):
    """Ascent is an open source many-core capable lightweight in situ
    visualization and analysis infrastructure for multi-physics HPC
    simulations."""

    homepage = "https://github.com/Alpine-DAV/ascent"
    git = "https://github.com/Alpine-DAV/ascent.git"
    url = "https://github.com/Alpine-DAV/ascent/releases/download/v0.5.1/ascent-v0.5.1-src-with-blt.tar.gz"
    tags = ["radiuss", "e4s"]

    maintainers("cyrush")

    license("BSD-3-Clause")

    version("develop", branch="develop", submodules=True)

    version(
        "0.9.3",
        tag="v0.9.3",
        commit="e69d6ec77938846caae8fea7ed988b1151ac9b81",
        submodules=True,
        preferred=True,
    )

    version(
        "0.9.2", tag="v0.9.2", commit="b842516d12640e4a0d9433a18c7249440ef6fc3d", submodules=True
    )

    version(
        "0.9.1", tag="v0.9.1", commit="027a2fe184f65a4923817a8cdfed0b0c61c2c75a", submodules=True
    )

    version(
        "0.9.0", tag="v0.9.0", commit="a31c88c579c8d0026e0025de8bace0cf22f6305b", submodules=True
    )

    version(
        "0.8.0", tag="v0.8.0", commit="08504374908518e013d7fe8d8882cfb1c2378e3b", submodules=True
    )

    version(
        "0.7.1", tag="v0.7.1", commit="79d35b2f48e92eb151313f0217e9bd7c15779582", submodules=True
    )

    version(
        "0.7.0", tag="v0.7.0", commit="cfed1b0a469e4dcc970fd7e0bcd78b522d97ea53", submodules=True
    )

    version(
        "0.6.0", tag="v0.6.0", commit="9ade37b0a9ea495e45adb25cda7498c0bf9465c5", submodules=True
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    ###########################################################################
    # package variants
    ###########################################################################

    variant("shared", default=True, description="Build Ascent as shared libs")
    variant("test", default=True, description="Enable Ascent unit tests")

    variant("mpi", default=True, description="Build Ascent MPI Support")
    # set to false for systems that implicitly link mpi
    variant("blt_find_mpi", default=True, description="Use BLT CMake Find MPI logic")
    variant("serial", default=True, description="build serial (non-mpi) libraries")

    # variants for language support
    variant("python", default=False, description="Build Ascent Python support")
    variant("fortran", default=True, description="Build Ascent Fortran support")

    # variants for runtime features
    variant("vtkh", default=True, description="Build VTK-h filter and rendering support")

    variant("openmp", default=(sys.platform != "darwin"), description="build openmp support")
    variant("raja", default=True, description="Build with RAJA support")
    variant("umpire", default=True, description="Build with Umpire support")
    variant("mfem", default=False, description="Build MFEM filter support")
    variant("dray", default=False, description="Build with Devil Ray support")
    variant("adios2", default=False, description="Build Adios2 filter support")
    variant("fides", default=False, description="Build Fides filter support")
    variant("occa", default=False, description="Build with OCCA support")

    # caliper
    variant("caliper", default=False, description="Build Caliper support")

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
    patch("ascent-shared-cuda-pr903.patch", when="@0.8.0")
    # patch for finding ADIOS2 more reliably
    # https://github.com/Alpine-DAV/ascent/pull/922
    patch("ascent-find-adios2-pr922.patch", when="@0.8.0")
    # patch for finding Conduit python more reliably
    # https://github.com/Alpine-DAV/ascent/pull/935
    patch("ascent-find-conduit-python-pr935.patch", when="@0.8.0")
    # patch for finding RAJA more reliably
    # https://github.com/Alpine-DAV/ascent/pull/1123
    patch("ascent-find-raja-pr1123.patch", when="@0.9.0")

    ##########################################################################
    # package dependencies
    ###########################################################################
    # Certain CMake versions have been found to break for our use cases
    depends_on("cmake@3.14.1:3.14,3.18.2:", type="build")

    #######################
    # Conduit
    #######################
    depends_on("conduit@:0.7.2", when="@:0.7.1")
    depends_on("conduit@0.8.2:", when="@0.8:")
    depends_on("conduit@0.8.6:", when="@0.9:")
    depends_on("conduit@0.9.1:", when="@0.9.3:")
    depends_on("conduit+python", when="+python")
    depends_on("conduit~python", when="~python")
    depends_on("conduit+mpi", when="+mpi")
    depends_on("conduit~mpi", when="~mpi")

    #######################
    # Python
    #######################
    # we need a shared version of python b/c linking with static python lib
    # causes duplicate state issues when running compiled python modules.
    with when("+python"):
        depends_on("python+shared")
        extends("python")
        depends_on("py-numpy", type=("build", "run"))
        depends_on("py-pip", type=("build", "run"))

    #######################
    # MPI
    #######################
    depends_on("mpi", when="+mpi")
    depends_on("py-mpi4py", when="+mpi+python")

    #############################
    # TPLs for Runtime Features
    #############################

    #######################
    # RAJA and Umpire
    # Note: Let RAJA/Umpire handle the Camp version constraints
    #######################
    with when("+raja"):
        depends_on("raja")
        depends_on("raja@2024.02.1:2024.02.99", when="@0.9.3:")
        depends_on("raja+openmp", when="+openmp")
        depends_on("raja~openmp", when="~openmp")

    with when("+umpire"):
        depends_on("umpire")
        depends_on("umpire@:2023.06.0", when="@:0.9.2")
        depends_on("umpire@2024.02.1:2024.02.99", when="@0.9.3:")

    #######################
    # BabelFlow
    #######################
    depends_on("babelflow", when="+babelflow+mpi")
    depends_on("parallelmergetree", when="+babelflow+mpi")

    #######################
    # VTK-m
    #######################
    with when("+vtkh"):
        depends_on("vtk-m +doubleprecision ~64bitids")
        depends_on("vtk-m@2.1:", when="@0.9.3:")
        depends_on("vtk-m@2.0:", when="@0.9.2:")
        # 2.1 support needs commit e52b7bb8c9fd131f2fd49edf58037cc5ef77a166
        depends_on("vtk-m@:2.0", when="@:0.9.2")
        depends_on("vtk-m@1.9", when="@0.9.0:0.9.1")

        depends_on("vtk-m~tbb", when="@0.9.0:")
        depends_on("vtk-m+openmp", when="@0.9.0: +openmp")
        depends_on("vtk-m~openmp", when="@0.9.0: ~openmp")
        depends_on("vtk-m~cuda", when="@0.9.0: ~cuda")
        depends_on("vtk-m+cuda", when="@0.9.0: +cuda")
        depends_on("vtk-m+fpic", when="@0.8.0:")
        depends_on("vtk-m~shared+fpic", when="@0.8.0: ~shared")
        # Ascent defaults to C++11
        depends_on("kokkos cxxstd=11", when="+vtkh ^vtk-m +kokkos")
        depends_on("kokkos@3.7.02", when="@0.9.3: +vtkh ^vtk-m +kokkos")

        #######################
        # VTK-h
        #######################
        # Ascent 0.9.0 includes VTK-h, prior to 0.9.0
        # VTK-h was developed externally
        depends_on("vtk-h@:0.7", when="@:0.7")
        depends_on("vtk-h@0.8.1:", when="@0.8:0.8")
        # propagate relevant variants to vtk-h
        depends_on("vtk-h+openmp", when="@:0.8.0 +openmp")
        depends_on("vtk-h~openmp", when="@:0.8.0 ~openmp")
        depends_on("vtk-h+cuda", when="@:0.8.0 +cuda")
        depends_on("vtk-h~cuda", when="@:0.8.0 ~cuda")
        depends_on("vtk-h+shared", when="@:0.8.0 +shared")
        depends_on("vtk-h~shared", when="@:0.8.0 ~shared")
        # When using VTK-h ascent also needs VTK-m
        depends_on("vtk-m@:1.7", when="@:0.8.0")
        depends_on("vtk-m+testlib", when="@:0.8.0 +test")

    propagate_cuda_arch("vtk-h", "@:0.8.0 +vtkh")

    # mfem
    depends_on("mfem~threadsafe~openmp+conduit", when="+mfem")
    # propagate relevent variants to mfem
    depends_on("mfem+mpi", when="+mfem+mpi")
    depends_on("mfem~mpi", when="+mfem~mpi")
    depends_on("mfem+shared", when="+mfem+shared")
    depends_on("mfem~shared", when="+mfem~shared")

    # occa
    depends_on("occa", when="+occa")

    # fides
    depends_on("fides", when="+fides")

    #######################
    # Devil Ray
    #######################
    # Ascent 0.9.0 includes Devil Ray, prior to 0.9.0
    # Devil Ray was developed externally
    # devil ray variants with mpi
    # we have to specify both because mfem makes us
    depends_on("dray~test~utils", when="@:0.8.0  +dray")
    depends_on("dray@0.1.8:", when="@:0.8.0 +dray")
    # propagate relevent variants to dray
    depends_on("dray+cuda", when="@:0.8.0 +dray+cuda")
    depends_on("dray~cuda", when="@:0.8.0 +dray~cuda")
    propagate_cuda_arch("dray", "@:0.8.0 +dray")
    depends_on("dray+mpi", when="@:0.8.0 +dray+mpi")
    depends_on("dray~mpi", when="@:0.8.0 +dray~mpi")
    depends_on("dray+shared", when="@:0.8.0 +dray+shared")
    depends_on("dray~shared", when="@:0.8.0 +dray~shared")
    depends_on("dray+openmp", when="@:0.8.0 +dray+openmp")
    depends_on("dray~openmp", when="@:0.8.0 +dray~openmp")

    # Adios2
    depends_on("adios2", when="+adios2")
    # propagate relevent variants to adios2
    depends_on("adios2+mpi", when="+adios2+mpi")
    depends_on("adios2~mpi", when="+adios2~mpi")
    depends_on("adios2+shared", when="+adios2+shared")
    depends_on("adios2~shared", when="+adios2~shared")

    #######################
    # Caliper
    #######################
    depends_on("caliper", when="+caliper")

    #######################
    # Documentation related
    #######################
    depends_on("py-sphinx", when="+python+doc", type="build")
    depends_on("py-sphinx-rtd-theme", when="+python+doc", type="build")

    ###########
    # Conflicts
    ###########
    conflicts(
        "+shared", when="@:0.7 +cuda", msg="Ascent needs to be built with ~shared for CUDA builds."
    )
    conflicts(
        "~fides", when="@0.9: +adios2", msg="Ascent >= 0.9 assumes FIDES when building ADIOS2"
    )

    def setup_build_environment(self, env):
        env.set("CTEST_OUTPUT_ON_FAILURE", "1")

    ####################################################################
    # Note: cmake, build, and install stages are handled by CMakePackage
    ####################################################################

    # provide cmake args (pass host config as cmake cache file)
    def cmake_args(self):
        host_config = self._get_host_config_path(self.spec)
        options = []
        options.extend(["-C", host_config, "../spack-src/src/"])
        if self.spec.satisfies("%oneapi"):
            options.extend(["-D", "CMAKE_Fortran_FLAGS=-nofor-main"])
        return options

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        """
        Checks the spack install of ascent using ascents's
        using-with-cmake example
        """
        print("Checking Ascent installation...")
        spec = self.spec
        install_prefix = spec.prefix
        example_src_dir = join_path(install_prefix, "examples", "ascent", "using-with-cmake")
        print("Checking using-with-cmake example...")
        with working_dir("check-ascent-using-with-cmake-example", create=True):
            cmake_args = [
                "-DASCENT_DIR={0}".format(install_prefix),
                "-DCONDUIT_DIR={0}".format(spec["conduit"].prefix),
                "-DVTKM_DIR={0}".format(spec["vtk-m"].prefix),
                "-DVTKH_DIR={0}".format(spec["vtk-h"].prefix),
                example_src_dir,
            ]
            cmake(*cmake_args)
            make()
            example = Executable("./ascent_render_example")
            example()
        print("Checking using-with-make example...")
        example_src_dir = join_path(install_prefix, "examples", "ascent", "using-with-make")
        example_files = glob.glob(join_path(example_src_dir, "*"))
        with working_dir("check-ascent-using-with-make-example", create=True):
            for example_file in example_files:
                shutil.copy(example_file, ".")
            make("ASCENT_DIR={0}".format(install_prefix))
            example = Executable("./ascent_render_example")
            example()

    def _get_host_config_path(self, spec):
        sys_type = spec.architecture
        # if on llnl systems, we can use the SYS_TYPE
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        host_config_path = "{0}-{1}-{2}-ascent-{3}.cmake".format(
            socket.gethostname(), sys_type, spec.compiler, spec.dag_hash()
        )
        dest_dir = spec.prefix
        host_config_path = os.path.abspath(join_path(dest_dir, host_config_path))
        return host_config_path

    @run_before("cmake")
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

        # shared vs static libs
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

        #######################
        # Unit Tests
        #######################
        if spec.satisfies("+test"):
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
        cfg.write(cmake_cache_entry("CONDUIT_DIR", spec["conduit"].prefix))

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
            cfg.write(cmake_cache_entry("PYTHON_EXECUTABLE", python.path))
            try:
                cfg.write("# python module install dir\n")
                cfg.write(cmake_cache_entry("PYTHON_MODULE_INSTALL_PREFIX", python_platlib))
            except NameError:
                # spack's  won't exist in a subclass
                pass
        else:
            cfg.write(cmake_cache_entry("ENABLE_PYTHON", "OFF"))

        if "+doc" in spec and "+python" in spec:
            cfg.write(cmake_cache_entry("ENABLE_DOCS", "ON"))

            cfg.write("# sphinx from spack \n")
            sphinx_build_exe = join_path(spec["py-sphinx"].prefix.bin, "sphinx-build")
            cfg.write(cmake_cache_entry("SPHINX_EXECUTABLE", sphinx_build_exe))
        else:
            cfg.write(cmake_cache_entry("ENABLE_DOCS", "OFF"))

        #######################
        # Serial
        #######################

        if spec.satisfies("+serial"):
            cfg.write(cmake_cache_entry("ENABLE_SERIAL", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_SERIAL", "OFF"))

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
            if cpp_compiler == "CC":
                mpicc_path = "cc"
                mpicxx_path = "CC"
                mpifc_path = "ftn"
            cfg.write(cmake_cache_entry("ENABLE_MPI", "ON"))
            cfg.write(cmake_cache_entry("MPI_C_COMPILER", mpicc_path))
            cfg.write(cmake_cache_entry("MPI_CXX_COMPILER", mpicxx_path))
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

            if spec.satisfies("+blt_find_mpi"):
                cfg.write(cmake_cache_entry("ENABLE_FIND_MPI", "ON"))
            else:
                cfg.write(cmake_cache_entry("ENABLE_FIND_MPI", "OFF"))
            ###################################
            # BABELFLOW (also depends on mpi)
            ###################################
            if spec.satisfies("+babelflow"):
                cfg.write(cmake_cache_entry("ENABLE_BABELFLOW", "ON"))
                cfg.write(cmake_cache_entry("BabelFlow_DIR", spec["babelflow"].prefix))
                cfg.write(cmake_cache_entry("PMT_DIR", spec["parallelmergetree"].prefix))
        else:
            cfg.write(cmake_cache_entry("ENABLE_MPI", "OFF"))

        #######################
        # CUDA
        #######################

        cfg.write("# CUDA Support\n")

        if spec.satisfies("+cuda"):
            cfg.write(cmake_cache_entry("ENABLE_CUDA", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_CUDA", "OFF"))

        if spec.satisfies("+openmp"):
            cfg.write(cmake_cache_entry("ENABLE_OPENMP", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_OPENMP", "OFF"))

        #######################
        # VTK-h (and deps)
        #######################
        cfg.write("# vtk-h support \n")

        if spec.satisfies("+vtkh"):
            cfg.write("# vtk-h\n")
            if self.spec.satisfies("@0.8.1:"):
                cfg.write(cmake_cache_entry("ENABLE_VTKH", "ON"))
            else:
                cfg.write(cmake_cache_entry("VTKH_DIR", spec["vtk-h"].prefix))

            cfg.write("# vtk-m from spack\n")
            cfg.write(cmake_cache_entry("VTKM_DIR", spec["vtk-m"].prefix))

            if spec.satisfies("+cuda"):
                cfg.write(cmake_cache_entry("VTKm_ENABLE_CUDA", "ON"))
                cfg.write(cmake_cache_entry("CMAKE_CUDA_HOST_COMPILER", env["SPACK_CXX"]))
            else:
                cfg.write(cmake_cache_entry("VTKm_ENABLE_CUDA", "OFF"))

        else:
            if self.spec.satisfies("@0.8.1:"):
                cfg.write("# vtk-h\n")
                cfg.write(cmake_cache_entry("ENABLE_VTKH", "OFF"))
            else:
                cfg.write("# vtk-h not build by spack\n")

        #######################
        # RAJA
        #######################
        if spec.satisfies("+raja"):
            cfg.write("# RAJA from spack \n")
            cfg.write(cmake_cache_entry("RAJA_DIR", spec["raja"].prefix))
        else:
            cfg.write("# RAJA not built by spack \n")

        #######################
        # Umpire
        #######################
        if spec.satisfies("+umpire"):
            cfg.write("# umpire from spack \n")
            cfg.write(cmake_cache_entry("UMPIRE_DIR", spec["umpire"].prefix))
        else:
            cfg.write("# umpire not built by spack \n")

        #######################
        # Camp
        #######################
        if "+umpire" in spec or "+raja" in spec:
            cfg.write("# camp from spack \n")
            cfg.write(cmake_cache_entry("CAMP_DIR", spec["camp"].prefix))
        else:
            cfg.write("# camp not built by spack \n")

        #######################
        # MFEM
        #######################
        if spec.satisfies("+mfem"):
            cfg.write("# mfem from spack \n")
            cfg.write(cmake_cache_entry("MFEM_DIR", spec["mfem"].prefix))
        else:
            cfg.write("# mfem not built by spack \n")

        #######################
        # OCCA
        #######################
        if spec.satisfies("+occa"):
            cfg.write("# occa from spack \n")
            cfg.write(cmake_cache_entry("OCCA_DIR", spec["occa"].prefix))
        else:
            cfg.write("# occa not built by spack \n")

        #######################
        # Devil Ray
        #######################
        if spec.satisfies("+dray"):
            cfg.write("# devil ray\n")
            if self.spec.satisfies("@0.8.1:"):
                cfg.write(cmake_cache_entry("ENABLE_DRAY", "ON"))
                cfg.write(cmake_cache_entry("ENABLE_APCOMP", "ON"))
            else:
                cfg.write("# devil ray from spack \n")
                cfg.write(cmake_cache_entry("DRAY_DIR", spec["dray"].prefix))
        else:
            if self.spec.satisfies("@0.8.1:"):
                cfg.write("# devil ray\n")
                cfg.write(cmake_cache_entry("ENABLE_DRAY", "OFF"))
                cfg.write(cmake_cache_entry("ENABLE_APCOMP", "OFF"))
            else:
                cfg.write("# devil ray not build by spack\n")

        #######################
        # Adios2
        #######################
        cfg.write("# adios2 support\n")

        if spec.satisfies("+adios2"):
            cfg.write(cmake_cache_entry("ADIOS2_DIR", spec["adios2"].prefix))
        else:
            cfg.write("# adios2 not built by spack \n")

        #######################
        # Fides
        #######################
        cfg.write("# Fides support\n")

        if spec.satisfies("+fides"):
            cfg.write(cmake_cache_entry("FIDES_DIR", spec["fides"].prefix))
        else:
            cfg.write("# fides not built by spack \n")

        #######################
        # Caliper
        #######################
        cfg.write("# caliper from spack \n")
        if spec.satisfies("+caliper"):
            cfg.write(cmake_cache_entry("CALIPER_DIR", spec["caliper"].prefix))
            cfg.write(cmake_cache_entry("ADIAK_DIR", spec["adiak"].prefix))
        else:
            cfg.write("# caliper not built by spack \n")

        #######################
        # Finish host-config
        #######################

        cfg.write("##################################\n")
        cfg.write("# end spack generated host-config\n")
        cfg.write("##################################\n")
        cfg.close()

        host_cfg_fname = os.path.abspath(host_cfg_fname)
        tty.info("spack generated ascent host-config file: " + host_cfg_fname)
