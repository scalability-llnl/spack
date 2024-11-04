# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import socket
from os.path import join as pjoin

from spack.package import *
from spack.util.executable import which_string


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


class Axom(CachedCMakePackage, CudaPackage, ROCmPackage):
    """Axom provides a robust, flexible software infrastructure for the development
    of multi-physics applications and computational tools."""

    maintainers("white238")

    homepage = "https://github.com/LLNL/axom"
    git = "https://github.com/LLNL/axom.git"
    tags = ["radiuss"]

    test_requires_compiler = True

    license("BSD-3-Clause")

    version("main", branch="main")
    version("develop", branch="develop")
    version("0.9.0", tag="v0.9.0", commit="5f531595d941d16fa3b8583bfc347a845d9feb6d")
    version("0.8.1", tag="v0.8.1", commit="0da8a5b1be596887158ac2fcd321524ba5259e15")
    version("0.8.0", tag="v0.8.0", commit="71fab3262eb7e1aa44a04c21d072b77f06362f7b")
    version("0.7.0", tag="v0.7.0", commit="ea5158191181c137117ae37959879bdc8b107f35")
    version("0.6.1", tag="v0.6.1", commit="ee240d3963d7879ae0e9c392902195bd7b04e37d")
    version("0.6.0", tag="v0.6.0", commit="65287dc00bc7c271a08cb86c632f5909c30e3506")
    version("0.5.0", tag="v0.5.0", commit="db137349b3e28617c3e0570dbd18e4a91654da98")
    version("0.4.0", tag="v0.4.0", commit="38c0d7495ece35a30fca5f5b578b8f9d54346bd2")
    version("0.3.3", tag="v0.3.3", commit="f0539ef0525469ffda054d86144f310c15b4f9e0")
    version("0.3.2", tag="v0.3.2", commit="c446b496e20e6118b8cba7e80f1f84c76a49e463")
    version("0.3.1", tag="v0.3.1", commit="cbefc0457a229d8acfb70622360d0667e90e50a2")
    version("0.3.0", tag="v0.3.0", commit="20068ccab4b4f70055918b4f17960ec3ed6dbce8")
    version("0.2.9", tag="v0.2.9", commit="9e9a54ede3326817c05f35922738516e43b5ec3d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # https://github.com/spack/spack/issues/31829
    patch("examples-oneapi.patch", when="@0.6.1 +examples %oneapi")

    patch("scr_examples_gtest.patch", when="@0.6.0:0.6.1")
    patch("umpire_camp_blt_targets.patch", when="@=0.8.0 ^umpire@2023.06.0")

    root_cmakelists_dir = "src"

    # -----------------------------------------------------------------------
    # Variants
    # -----------------------------------------------------------------------
    variant("shared", default=True, description="Enable build of shared libraries")

    variant("examples", default=True, description="Build examples")
    variant("tools", default=True, description="Build tools")

    # Hard requirement after Axom 0.6.1
    variant("cpp14", default=True, description="Build with C++14 support")

    variant("fortran", default=True, description="Build with Fortran support")

    variant("python", default=False, description="Build python support")

    variant("mpi", default=True, description="Build MPI support")
    variant("openmp", default=True, description="Turn on OpenMP support.")

    variant(
        "profiling",
        default=False,
        when="@develop",
        description="Build with hooks for Adiak/Caliper performance analysis",
    )

    variant("mfem", default=False, description="Build with mfem")
    variant("hdf5", default=True, description="Build with hdf5")
    variant("lua", default=True, description="Build with Lua")
    variant("scr", default=False, description="Build with SCR")
    variant("umpire", default=True, description="Build with umpire")

    variant("raja", default=True, description="Build with raja")

    varmsg = "Build development tools (such as Sphinx, Doxygen, etc...)"
    variant("devtools", default=False, description=varmsg)

    # -----------------------------------------------------------------------
    # Dependencies
    # -----------------------------------------------------------------------
    # Basics
    depends_on("cmake@3.14:", type="build")
    depends_on("cmake@3.18:", type="build", when="@0.7.0:")
    depends_on("cmake@3.21:", type="build", when="+rocm")

    depends_on("blt", type="build")
    depends_on("blt@0.5.1:0.5.3", type="build", when="@0.6.1:0.8")
    depends_on("blt@0.6.2:", type="build", when="@0.9:")

    depends_on("mpi", when="+mpi")

    # Libraries
    # Forward variants to Conduit
    for _var in ["fortran", "hdf5", "mpi", "python"]:
        depends_on("conduit+{0}".format(_var), when="+{0}".format(_var))
        depends_on("conduit~{0}".format(_var), when="~{0}".format(_var))

    depends_on("hdf5", when="+hdf5")

    depends_on("lua", when="+lua")

    depends_on("scr", when="+scr")
    depends_on("scr~fortran", when="+scr~fortran")

    with when("+umpire"):
        depends_on("umpire")
        depends_on("umpire@2024.02.0:", when="@0.9:")
        depends_on("umpire@2022.03.0:2023.06", when="@0.7.0:0.8")
        depends_on("umpire@6.0.0", when="@0.6.0")
        depends_on("umpire@5:5.0.1", when="@:0.5.0")
        depends_on("umpire+openmp", when="+openmp")

    with when("+raja"):
        depends_on("raja")
        depends_on("raja@2024.02.0:", when="@0.9:")
        depends_on("raja@2022.03.0:2023.06", when="@0.7.0:0.8")
        depends_on("raja@0.14.0", when="@0.6.0")
        depends_on("raja@:0.13.0", when="@:0.5.0")
        depends_on("raja~openmp", when="~openmp")
        depends_on("raja+openmp", when="+openmp")

    with when("+profiling"):
        depends_on("adiak")
        depends_on("caliper+adiak~papi")

        depends_on("caliper+cuda", when="+cuda")
        depends_on("caliper~cuda", when="~cuda")

        depends_on("caliper+rocm", when="+rocm")
        depends_on("caliper~rocm", when="~rocm")

        for dep in ["adiak", "caliper"]:
            depends_on(f"{dep}+mpi", when="+mpi")
            depends_on(f"{dep}~mpi", when="~mpi")
            depends_on(f"{dep}+shared", when="+shared")
            depends_on(f"{dep}~shared", when="~shared")

    for val in CudaPackage.cuda_arch_values:
        ext_cuda_dep = f"+cuda cuda_arch={val}"
        depends_on(f"raja {ext_cuda_dep}", when=f"+raja {ext_cuda_dep}")
        depends_on(f"umpire {ext_cuda_dep}", when=f"+umpire {ext_cuda_dep}")
        depends_on(f"caliper {ext_cuda_dep}", when=f"+profiling {ext_cuda_dep}")

    for val in ROCmPackage.amdgpu_targets:
        ext_rocm_dep = f"+rocm amdgpu_target={val}"
        depends_on(f"raja {ext_rocm_dep}", when=f"+raja {ext_rocm_dep}")
        depends_on(f"umpire {ext_rocm_dep}", when=f"+umpire {ext_rocm_dep}")
        depends_on(f"caliper {ext_rocm_dep}", when=f"+profiling {ext_rocm_dep}")

    depends_on("rocprim", when="+rocm")

    with when("+mfem"):
        depends_on("mfem+mpi", when="+mpi")
        depends_on("mfem~mpi", when="~mpi")
        depends_on("mfem@4.5.0:", when="@0.7.0:")

    depends_on("python", when="+python")

    # Devtools
    with when("+devtools"):
        depends_on("cppcheck")
        depends_on("doxygen")
        depends_on("graphviz")
        depends_on("python")
        depends_on("py-sphinx")
        depends_on("py-shroud")
        depends_on("py-jsonschema")
        depends_on("llvm+clang@10.0.0", type="build")

    # -----------------------------------------------------------------------
    # Conflicts
    # -----------------------------------------------------------------------
    # Hard requirement after Axom 0.6.1
    conflicts("~cpp14", when="@0.6.2:")

    # Conduit's cmake config files moved and < 0.4.0 can't find it
    conflicts("^conduit@0.7.2:", when="@:0.4.0")

    # Sidre requires conduit_blueprint_mpi.hpp
    conflicts("^conduit@:0.6.0", when="@0.5.0:")

    conflicts("+openmp", when="+rocm")
    conflicts("+cuda", when="+rocm")

    conflicts("^blt@:0.3.6", when="+rocm")

    def flag_handler(self, name, flags):
        if self.spec.satisfies("%cce") and name == "fflags":
            flags.append("-ef")

        if name in ("cflags", "cxxflags", "cppflags", "fflags"):
            return (None, None, None)  # handled in the cmake cache
        return (flags, None, None)

    def _get_sys_type(self, spec):
        sys_type = spec.architecture
        # if on llnl systems, we can use the SYS_TYPE
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        return sys_type

    def is_fortran_compiler(self, compiler):
        if self.compiler.fc is not None and compiler in self.compiler.fc:
            return True
        return False

    @property
    def cache_name(self):
        hostname = socket.gethostname()
        if "SYS_TYPE" in env:
            # Are we on a LLNL system then strip node number
            hostname = hostname.rstrip("1234567890")
        special_case = ""
        if self.spec.satisfies("+cuda"):
            special_case += "_cuda"
        if self.spec.satisfies("~fortran"):
            special_case += "_nofortran"
        if self.spec.satisfies("+rocm"):
            special_case += "_hip"
        return "{0}-{1}-{2}@{3}{4}.cmake".format(
            hostname,
            self._get_sys_type(self.spec),
            self.spec.compiler.name,
            self.spec.compiler.version,
            special_case,
        )

    def initconfig_compiler_entries(self):
        spec = self.spec
        entries = super().initconfig_compiler_entries()

        if spec.satisfies("+fortran"):
            entries.append(cmake_cache_option("ENABLE_FORTRAN", True))
            if self.is_fortran_compiler("gfortran") and "clang" in self.compiler.cxx:
                libdir = pjoin(os.path.dirname(os.path.dirname(self.compiler.cxx)), "lib")
                flags = ""
                for _libpath in [libdir, libdir + "64"]:
                    if os.path.exists(_libpath):
                        if spec.satisfies("^cuda"):
                            flags += " -Xlinker -rpath -Xlinker {0}".format(_libpath)
                        else:
                            flags += " -Wl,-rpath,{0}".format(_libpath)
                description = "Adds a missing libstdc++ rpath"
                if flags:
                    entries.append(cmake_cache_string("BLT_EXE_LINKER_FLAGS", flags, description))
        else:
            entries.append(cmake_cache_option("ENABLE_FORTRAN", False))

        if "+cpp14" in spec and spec.satisfies("@:0.6.1"):
            entries.append(cmake_cache_string("BLT_CXX_STD", "c++14", ""))

        # Add optimization flag workaround for Debug builds with cray compiler or newer HIP
        if spec.satisfies("+rocm"):
            entries.append(cmake_cache_string("CMAKE_CXX_FLAGS_DEBUG", "-O1 -g -DNDEBUG"))

        return entries

    def initconfig_hardware_entries(self):
        spec = self.spec
        entries = super().initconfig_hardware_entries()

        if spec.satisfies("+cuda"):
            entries.append(cmake_cache_option("ENABLE_CUDA", True))
            entries.append(cmake_cache_option("CMAKE_CUDA_SEPARABLE_COMPILATION", True))

            # CUDA_FLAGS
            cudaflags = "${CMAKE_CUDA_FLAGS} -restrict --expt-extended-lambda "

            # Pass through any cxxflags to the host compiler via nvcc's Xcompiler flag
            host_cxx_flags = spec.compiler_flags["cxxflags"]
            cudaflags += " ".join(["-Xcompiler=%s " % flag for flag in host_cxx_flags])

            if spec.satisfies("^blt@:0.5.1"):
                # This is handled internally by BLT now
                if spec.satisfies("+cpp14"):
                    cudaflags += " -std=c++14"
                else:
                    cudaflags += " -std=c++11"
            entries.append(cmake_cache_string("CMAKE_CUDA_FLAGS", cudaflags, force=True))

            entries.append("# nvcc does not like gtest's 'pthreads' flag\n")
            entries.append(cmake_cache_option("gtest_disable_pthreads", True))

        if spec.satisfies("+rocm"):
            entries.append("#------------------{0}\n".format("-" * 60))
            entries.append("# Axom ROCm specifics\n")
            entries.append("#------------------{0}\n\n".format("-" * 60))

            entries.append(cmake_cache_option("ENABLE_HIP", True))

            hip_root = spec["hip"].prefix
            rocm_root = hip_root + "/.."

            # Fix blt_hip getting HIP_CLANG_INCLUDE_PATH-NOTFOUND bad include directory
            # TODO: verify that this is still needed and is indeed specific to LC
            if (
                self.spec.satisfies("%cce") or self.spec.satisfies("%clang")
            ) and "toss_4" in self._get_sys_type(spec):
                # Set the patch version to 0 if not already
                clang_version = str(self.compiler.version)[:-1] + "0"
                hip_clang_include_path = (
                    rocm_root + "/llvm/lib/clang/" + clang_version + "/include"
                )
                if os.path.isdir(hip_clang_include_path):
                    entries.append(
                        cmake_cache_path("HIP_CLANG_INCLUDE_PATH", hip_clang_include_path)
                    )

            # Fixes for mpi for rocm until wrapper paths are fixed
            # These flags are already part of the wrapped compilers on TOSS4 systems
            hip_link_flags = ""
            if "+fortran" in spec and self.is_fortran_compiler("amdflang"):
                hip_link_flags += "-Wl,--disable-new-dtags "
                hip_link_flags += "-L{0}/../llvm/lib -L{0}/lib ".format(hip_root)
                hip_link_flags += "-Wl,-rpath,{0}/../llvm/lib:{0}/lib ".format(hip_root)
                hip_link_flags += "-lpgmath -lflang -lflangrti -lompstub -lamdhip64 "

            # Remove extra link library for crayftn
            if "+fortran" in spec and self.is_fortran_compiler("crayftn"):
                entries.append(
                    cmake_cache_string("BLT_CMAKE_IMPLICIT_LINK_LIBRARIES_EXCLUDE", "unwind")
                )

            # Additional libraries for TOSS4
            hip_link_flags += " -L{0}/../lib64 -Wl,-rpath,{0}/../lib64 ".format(hip_root)
            hip_link_flags += " -L{0}/../lib -Wl,-rpath,{0}/../lib ".format(hip_root)
            hip_link_flags += "-lamd_comgr -lhsa-runtime64 "

            entries.append(cmake_cache_string("CMAKE_EXE_LINKER_FLAGS", hip_link_flags))

        entries.append("#------------------{0}".format("-" * 30))
        entries.append("# Hardware Specifics")
        entries.append("#------------------{0}\n".format("-" * 30))

        # OpenMP
        entries.append(cmake_cache_option("ENABLE_OPENMP", spec.satisfies("+openmp")))

        # Enable death tests
        entries.append(
            cmake_cache_option(
                "ENABLE_GTEST_DEATH_TESTS", not spec.satisfies("+cuda target=ppc64le:")
            )
        )

        if "+fortran" in spec and self.is_fortran_compiler("xlf"):
            # Grab lib directory for the current fortran compiler
            libdir = pjoin(os.path.dirname(os.path.dirname(self.compiler.fc)), "lib")
            description = (
                "Adds a missing rpath for libraries " "associated with the fortran compiler"
            )

            linker_flags = "${BLT_EXE_LINKER_FLAGS} -Wl,-rpath," + libdir

            entries.append(cmake_cache_string("BLT_EXE_LINKER_FLAGS", linker_flags, description))

            if spec.satisfies("+shared"):
                linker_flags = "${CMAKE_SHARED_LINKER_FLAGS} -Wl,-rpath," + libdir
                entries.append(
                    cmake_cache_string("CMAKE_SHARED_LINKER_FLAGS", linker_flags, description)
                )

            description = "Converts C-style comments to Fortran style in preprocessed files"
            entries.append(
                cmake_cache_string(
                    "BLT_FORTRAN_FLAGS", "-WF,-C!  -qxlf2003=polymorphic", description
                )
            )

        if (
            "+openmp" in spec
            and "clang" in self.compiler.cxx
            and "+fortran" in spec
            and self.is_fortran_compiler("xlf")
        ):
            openmp_gen_exp = (
                "$<$<NOT:$<COMPILE_LANGUAGE:Fortran>>:"
                "-fopenmp=libomp>;$<$<COMPILE_LANGUAGE:"
                "Fortran>:-qsmp=omp>"
            )

            description = "Different OpenMP linker flag between CXX and Fortran"
            entries.append(
                cmake_cache_string("BLT_OPENMP_LINK_FLAGS", openmp_gen_exp, description)
            )

        if spec.satisfies("target=ppc64le:"):
            # Fix for working around CMake adding implicit link directories
            # returned by the BlueOS compilers to link executables with
            # non-system default stdlib
            _roots = ["/usr/tce/packages/gcc/gcc-4.9.3", "/usr/tce/packages/gcc/gcc-4.9.3/gnu"]
            _subdirs = ["lib64", "lib64/gcc/powerpc64le-unknown-linux-gnu/4.9.3"]
            _existing_paths = []
            for root in _roots:
                for subdir in _subdirs:
                    _curr_path = pjoin(root, subdir)
                    if os.path.exists(_curr_path):
                        _existing_paths.append(_curr_path)
            if _existing_paths:
                entries.append(
                    cmake_cache_string(
                        "BLT_CMAKE_IMPLICIT_LINK_DIRECTORIES_EXCLUDE", ";".join(_existing_paths)
                    )
                )

        return entries

    def initconfig_mpi_entries(self):
        spec = self.spec
        entries = super().initconfig_mpi_entries()

        if spec.satisfies("+mpi"):
            entries.append(cmake_cache_option("ENABLE_MPI", True))
            if spec["mpi"].name == "spectrum-mpi":
                entries.append(cmake_cache_string("BLT_MPI_COMMAND_APPEND", "mpibind"))

            # Replace /usr/bin/srun path with srun flux wrapper path on TOSS 4
            # TODO: Remove this logic by adding `using_flux` case in
            #  spack/lib/spack/spack/build_systems/cached_cmake.py:196 and remove hard-coded
            #  path to srun in same file.
            if "toss_4" in self._get_sys_type(spec):
                srun_wrapper = which_string("srun")
                mpi_exec_index = [
                    index for index, entry in enumerate(entries) if "MPIEXEC_EXECUTABLE" in entry
                ]
                del entries[mpi_exec_index[0]]
                entries.append(cmake_cache_path("MPIEXEC_EXECUTABLE", srun_wrapper))
        else:
            entries.append(cmake_cache_option("ENABLE_MPI", False))

        return entries

    def find_path_replacement(self, path1, path2, path_replacements, name, entries):
        root = os.path.commonprefix([path1, path2])
        if root.endswith(os.path.sep):
            root = root[: -len(os.path.sep)]
        if root:
            path_replacements[root] = "${" + name + "}"
            entries.append(cmake_cache_path(name, root))

    def initconfig_package_entries(self):
        spec = self.spec
        entries = []
        path_replacements = {}

        # TPL locations
        entries.append("#------------------{0}".format("-" * 60))
        entries.append("# TPLs")
        entries.append("#------------------{0}\n".format("-" * 60))

        # Try to find the common prefix of the TPL directory.
        # If found, we will use this in the TPL paths
        path1 = os.path.realpath(spec["conduit"].prefix)
        path2 = os.path.realpath(self.prefix)
        self.find_path_replacement(path1, path2, path_replacements, "TPL_ROOT", entries)

        conduit_dir = get_spec_path(spec, "conduit", path_replacements)
        entries.append(cmake_cache_path("CONDUIT_DIR", conduit_dir))

        # optional tpls
        for dep in ("mfem", "hdf5", "lua", "raja", "umpire"):
            if "+%s" % dep in spec:
                dep_dir = get_spec_path(spec, dep, path_replacements)
                entries.append(cmake_cache_path("%s_DIR" % dep.upper(), dep_dir))
            else:
                entries.append("# %s not built\n" % dep.upper())

        if spec.satisfies("+profiling"):
            dep_dir = get_spec_path(spec, "adiak", path_replacements)
            entries.append(cmake_cache_path("ADIAK_DIR", dep_dir))

            dep_dir = get_spec_path(spec, "caliper", path_replacements)
            entries.append(cmake_cache_path("CALIPER_DIR", dep_dir))

        if "+umpire" in spec and spec.satisfies("^camp"):
            dep_dir = get_spec_path(spec, "camp", path_replacements)
            entries.append(cmake_cache_path("CAMP_DIR", dep_dir))

        # SCR does not export it's targets so we need to pull in its dependencies
        if spec.satisfies("+scr"):
            dep_dir = get_spec_path(spec, "scr", path_replacements)
            entries.append(cmake_cache_path("SCR_DIR", dep_dir))

            # scr's dependencies
            scr_deps = (
                "kvtree",
                "dtcmp",
                "spath",
                "axl",
                "lwgrp",
                "er",
                "rankstr",
                "redset",
                "shuffile",
                "libyogrt",
            )
            for dep in scr_deps:
                if spec.satisfies("^{0}".format(dep)):
                    dep_dir = get_spec_path(spec, dep, path_replacements)
                    entries.append(cmake_cache_path("%s_DIR" % dep.upper(), dep_dir))
        else:
            entries.append("# scr not built\n")

        ##################################
        # Devtools
        ##################################

        entries.append("#------------------{0}".format("-" * 60))
        entries.append("# Devtools")
        entries.append("#------------------{0}\n".format("-" * 60))

        # Add common prefix to path replacement list
        if spec.satisfies("+devtools"):
            # Grab common devtools root and strip the trailing slash
            path1 = os.path.realpath(spec["cppcheck"].prefix)
            path2 = os.path.realpath(spec["doxygen"].prefix)
            self.find_path_replacement(path1, path2, path_replacements, "DEVTOOLS_ROOT", entries)

        if "+devtools" in spec and spec.satisfies("^llvm"):
            clang_fmt_path = spec["llvm"].prefix.bin.join("clang-format")
            entries.append(cmake_cache_path("CLANGFORMAT_EXECUTABLE", clang_fmt_path))
        else:
            entries.append("# ClangFormat disabled due to llvm and devtools not in spec\n")
            entries.append(cmake_cache_option("ENABLE_CLANGFORMAT", False))

        if "+python" in spec or "+devtools" in spec:
            python_path = os.path.realpath(spec["python"].command.path)
            for key in path_replacements:
                python_path = python_path.replace(key, path_replacements[key])
            entries.append(cmake_cache_path("PYTHON_EXECUTABLE", python_path))

        if spec.satisfies("^py-jsonschema"):
            jsonschema_dir = get_spec_path(spec, "py-jsonschema", path_replacements, use_bin=True)
            jsonschema_path = os.path.join(jsonschema_dir, "jsonschema")
            entries.append(cmake_cache_path("JSONSCHEMA_EXECUTABLE", jsonschema_path))

        enable_docs = spec.satisfies("^doxygen") or spec.satisfies("^py-sphinx")
        entries.append(cmake_cache_option("ENABLE_DOCS", enable_docs))

        if spec.satisfies("^py-sphinx"):
            sphinx_bin_dir = get_spec_path(spec, "py-sphinx", path_replacements, use_bin=True)
            entries.append(
                cmake_cache_path("SPHINX_EXECUTABLE", pjoin(sphinx_bin_dir, "sphinx-build"))
            )

        if spec.satisfies("^py-shroud"):
            shroud_bin_dir = get_spec_path(spec, "py-shroud", path_replacements, use_bin=True)
            entries.append(cmake_cache_path("SHROUD_EXECUTABLE", pjoin(shroud_bin_dir, "shroud")))

        for dep in ("cppcheck", "doxygen"):
            if spec.satisfies("^%s" % dep):
                dep_bin_dir = get_spec_path(spec, dep, path_replacements, use_bin=True)
                entries.append(
                    cmake_cache_path("%s_EXECUTABLE" % dep.upper(), pjoin(dep_bin_dir, dep))
                )

        return entries

    def cmake_args(self):
        options = []

        options.append("-DBLT_SOURCE_DIR:PATH={0}".format(self.spec["blt"].prefix))

        if self.run_tests is False:
            options.append("-DENABLE_TESTS=OFF")
        else:
            options.append("-DENABLE_TESTS=ON")

        options.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))
        options.append(self.define_from_variant("AXOM_ENABLE_EXAMPLES", "examples"))
        options.append(self.define_from_variant("AXOM_ENABLE_TOOLS", "tools"))

        return options

    def patch(self):
        if self.spec.satisfies("%cce"):
            filter_file(
                "PROPERTIES LINKER_LANGUAGE CXX",
                'PROPERTIES LINKER_LANGUAGE CXX \n LINK_FLAGS "-fopenmp"',
                "src/axom/quest/examples/CMakeLists.txt",
            )

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        with working_dir(self.build_directory):
            print("Running Axom Unit Tests...")
            make("test")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install_using_cmake(self):
        """build example with cmake and run"""
        example_src_dir = join_path(self.prefix.examples.axom, "using-with-cmake")
        example_stage_dir = "./cmake"
        shutil.copytree(example_src_dir, example_stage_dir)
        with working_dir(join_path(example_stage_dir, "build"), create=True):
            cmake_args = ["-C ../host-config.cmake", example_src_dir]
            cmake = self.spec["cmake"].command
            cmake(*cmake_args)
            make()
            example = Executable("./example")
            example()
            make("clean")

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def test_install_using_make(self):
        """build example with make and run"""
        example_src_dir = join_path(self.prefix.examples.axom, "using-with-make")
        example_stage_dir = "./make"
        shutil.copytree(example_src_dir, example_stage_dir)
        with working_dir(example_stage_dir, create=True):
            make(f"AXOM_DIR={self.prefix}")
            example = Executable("./example")
            example()
            make("clean")
