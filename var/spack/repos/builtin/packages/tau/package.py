# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import fnmatch
import glob
import os
import platform
import sys

from spack.package import *


class Tau(Package):
    """A portable profiling and tracing toolkit for performance
    analysis of parallel programs written in Fortran, C, C++, UPC,
    Java, Python.
    """

    maintainers("wspear", "eugeneswalker", "khuck", "sameershende")
    homepage = "https://www.cs.uoregon.edu/research/tau"
    url = "https://www.cs.uoregon.edu/research/tau/tau_releases/tau-2.30.tar.gz"
    git = "https://github.com/UO-OACISS/tau2"

    tags = ["e4s"]

    license("MIT")

    version("master", branch="master")
    version("2.33.2", sha256="8ee81fe75507612379f70033183bed2a90e1245554b2a78196b6c5145da44f27")
    version("2.33.1", sha256="13cc5138e110932f34f02ddf548db91d8219ccb7ff9a84187f0790e40a502403")
    version("2.33", sha256="04d9d67adb495bc1ea56561f33c5ce5ba44f51cc7f64996f65bd446fac5483d9")
    version("2.32.1", sha256="0eec3de46b0873846dfc639270c5e30a226b463dd6cb41aa12e975b7563f0eeb")
    version("2.32", sha256="ee774a06e30ce0ef0f053635a52229152c39aba4f4933bed92da55e5e13466f3")
    version("2.31.1", sha256="bf445b9d4fe40a5672a7b175044d2133791c4dfb36a214c1a55a931aebc06b9d")
    version("2.31", sha256="27e73c395dd2a42b91591ce4a76b88b1f67663ef13aa19ef4297c68f45d946c2")
    version("2.30.2", sha256="43f84a15b71a226f8a64d966f0cb46022bcfbaefb341295ecc6fa80bb82bbfb4")
    version("2.30.1", sha256="9c20ca1b4f4e80d885f24491cee598068871f0e9dd67906a5e47e4b4147d08fc")
    version("2.30", sha256="e581c33e21488d69839a00d97fd4451ea579f47249b2750d5c36bea773041eaf")
    version("2.29.1", sha256="4195a0a236bba510ab50a93e13c7f00d9472e8bc46c91de3f0696112a34e34e2")
    version("2.29", sha256="146be769a23c869a7935e8fa5ba79f40ba36b9057a96dda3be6730fc9ca86086")
    version("2.28.2", sha256="64e129a482056755012b91dae2fb4f728dbf3adbab53d49187eca952891c5457")
    version("2.28.1", sha256="b262e5c9977471e9f5a8d729b3db743012df9b0ab8244da2842039f8a3b98b34")
    version("2.28", sha256="68c6f13ae748d12c921456e494006796ca2b0efebdeef76ee7c898c81592883e")
    version("2.27.2p1", sha256="3256771fb71c2b05932b44d0650e6eadc712f1bdedf4c0fb2781db3b266225dd")
    version("2.27.2", sha256="d319a4588ad303b71082254f4f40aa76f6183a01b5bc4bd987f76e1a6026efa1")
    version("2.27.1", sha256="315babab4da25dd08633ad8dbf33d93db77f57d240bcbd3527ed5b8710cb9d8f")
    version("2.27", sha256="d48fdca49cda2d9f25a0cf5dbd961201c8a2b1f025bcbb121d96ad43f211f1a7")
    version("2.26.3", sha256="bd785ed47f20e6b8b2a1d99ce383d292f70b1fb9e2eaab21f5eaf8e64b28e990")
    version("2.26.2", sha256="92ca68db51fd5bd026187e70b397bcd1db9bfb07008d7e8bc935411a97978834")
    version("2.26.1", sha256="d084ff87e5f9fe640a3fc48aa5c8c52f586e7b739787f2bb9a4249005e459896")
    version("2.26", sha256="458228646a13a228841d4133f24af14cc182f4978eb15ef6244d71735abe8d16")
    version("2.25", sha256="ab8a8c15a075af69aa23b4790b4e2d9dffc3b880fc1ff806c21535ab69b6a088")
    version("2.24.1", sha256="bc27052c36377e4b8fc0bbb4afaa57eaa8bcb3f5e5066e576b0f40d341c28a0e")
    version("2.24", sha256="5d28e8b26561c7cd7d0029b56ec0f95fc26803ac0b100c98e00af0b02e7f55e2")
    version("2.23.1", sha256="31a4d0019cec6ef57459a9cd18a220f0130838a5f1a0b5ea7879853f5a38cf88")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Disable some default dependencies on Darwin/OSX
    darwin_default = False
    if sys.platform != "darwin":
        darwin_default = True

    variant("scorep", default=False, description="Activates SCOREP support")
    variant("openmp", default=False, description="Use OpenMP threads")
    variant("pthreads", default=True, description="Use POSIX threads")
    variant("mpi", default=False, description="Specify use of TAU MPI wrapper library")
    variant("phase", default=False, description="Generate phase based profiles")
    variant("papi", default=darwin_default, description="Activates Performance API")
    variant("binutils", default=True, description="Activates support of BFD GNU Binutils")
    variant("libdwarf", default=darwin_default, description="Activates support of libdwarf")
    variant("elf", default=darwin_default, description="Activates support of elf")
    variant("libunwind", default=darwin_default, description="Activates support of libunwind")
    variant("otf2", default=True, description="Activates support of Open Trace Format (OTF)")
    variant("pdt", default=True, description="Use PDT for source code instrumentation")
    variant("comm", default=False, description=" Generate profiles with MPI communicator info")
    variant("python", default=False, description="Activates Python support")
    variant("likwid", default=False, description="Activates LIKWID support", when="@2.27")
    variant("ompt", default=False, description="Activates OMPT instrumentation")
    variant("opari", default=False, description="Activates Opari2 instrumentation")
    variant("shmem", default=False, description="Activates SHMEM support")
    variant("gasnet", default=False, description="Activates GASNET support")
    variant("cuda", default=False, description="Activates CUDA support")
    variant("rocm", default=False, description="Activates ROCm support", when="@2.28:")
    variant(
        "level_zero",
        default=False,
        description="Activates Intel OneAPI Level Zero support",
        when="@2.30:",
    )
    variant(
        "rocprofiler",
        default=False,
        description="Activates ROCm rocprofiler support",
        when="@2.29.1:",
    )
    variant(
        "roctracer", default=False, description="Activates ROCm roctracer support", when="@2.28.1:"
    )
    variant(
        "rocprofv2", default=False, description="Activates ROCm rocprofiler support", when="@2.34:"
    )
    variant("opencl", default=False, description="Activates OpenCL support")
    variant("fortran", default=darwin_default, description="Activates Fortran support")
    variant("io", default=True, description="Activates POSIX I/O support")
    variant(
        "adios2", default=False, description="Activates ADIOS2 output support", when="@2.26.3:"
    )
    variant("sqlite", default=False, description="Activates SQLite3 output support")
    variant("syscall", default=False, description="Activates syscall wrapper", when="@2.33:")
    variant(
        "profileparam",
        default=False,
        description="Generate profiles with parameter mapped event data",
    )

    # Support cross compiling.
    # This is a _reasonable_ subset of the full set of TAU
    # architectures supported:
    variant("craycnl", default=False, description="Build for Cray compute nodes")
    variant("ppc64le", default=False, description="Build for IBM Power LE nodes")
    variant(
        "x86_64", default=False, description="Force build for x86 Linux instead of auto-detect"
    )
    variant("dyninst", default=False, description="Activates dyninst support")

    variant(
        "disable-no-pie",
        default=False,
        description="Do not add -no-pie while linking with Ubuntu.",
    )

    depends_on("gmake", type="build")
    depends_on("cmake@3.14:", type="build", when="%clang")
    depends_on("cmake@3.14:", type="build", when="%aocc")
    depends_on("zlib-api", type="link")
    depends_on("pdt", when="+pdt")  # Required for TAU instrumentation
    depends_on("scorep", when="+scorep")
    depends_on("otf2@2.1:2.3", when="@:2.33.0 +otf2")
    depends_on("otf2@3:", when="@2.33.1: +otf2")
    depends_on("likwid", when="+likwid")
    depends_on("papi", when="+papi")
    depends_on("libdwarf", when="+libdwarf")
    depends_on("elf", when="+elf")
    # TAU requires the ELF header support, libiberty and demangle.
    depends_on("binutils+libiberty+headers+plugins", when="+binutils")
    with when("+python"):
        depends_on("python@2.7:")
        # Build errors with Python 3.9
        depends_on("python@:3.8", when="@:2.31.0")
        # python 3.11 doesn't work in the 2.32 releases
        depends_on("python@:3.10", when="@:2.32.1")
    depends_on("libunwind", when="+libunwind")
    depends_on("mpi", when="+mpi", type=("build", "run", "link"))
    depends_on("cuda", when="+cuda")
    depends_on("gasnet", when="+gasnet")
    depends_on("adios2", when="+adios2")
    depends_on("sqlite", when="+sqlite")
    depends_on("hwloc")
    depends_on("rocprofiler-dev", when="+rocprofiler")
    depends_on("rocprofiler-dev@6.0.0:", when="@2.34: +rocprofv2")
    depends_on("roctracer-dev", when="+roctracer")
    depends_on("hsa-rocr-dev", when="+rocm")
    depends_on("rocm-smi-lib", when="@2.32.1: +rocm")
    depends_on("rocm-core", when="@2.34: +rocm")
    depends_on("hip", when="@2.34: +roctracer")
    depends_on("java", type="run")  # for paraprof
    depends_on("oneapi-level-zero", when="+level_zero")
    depends_on("dyninst@12.3.0:", when="+dyninst")

    # Elf only required from 2.28.1 on
    conflicts("+elf", when="@:2.28.0")
    conflicts("+libdwarf", when="@:2.28.0")

    # ADIOS2, SQLite only available from 2.29.1 on
    conflicts("+adios2", when="@:2.29.1")
    conflicts("+sqlite", when="@:2.29.1")
    conflicts("+dyninst", when="@:2.32.1")
    conflicts("+disable-no-pie", when="@:2.33.2")
    patch("unwind.patch", when="@2.29.0")

    conflicts("+rocprofiler", when="+roctracer", msg="Use either rocprofiler or roctracer")
    conflicts("+rocprofv2", when="+rocprofiler", msg="Rocprofv2 does not need rocprofiler")
    conflicts("+rocprofv2", when="+roctracer", msg="Rocprofv2 does not need roctracer")
    requires("+rocm", when="+rocprofiler", msg="Rocprofiler requires ROCm")
    requires("+rocm", when="+roctracer", msg="Roctracer requires ROCm")

    requires(
        "+rocprofiler",
        "+roctracer",
        "+rocprofv2",
        policy="one_of",
        when="+rocm",
        msg="Using ROCm, select either +rocprofiler, +roctracer or +rocprofv2",
    )

    # https://github.com/UO-OACISS/tau2/commit/1d2cb6b
    patch("tau-rocm-disable-llvm-plugin.patch", when="@2.33.2 +rocm")

    filter_compiler_wrappers("Makefile", relative_root="include")
    filter_compiler_wrappers("Makefile.tau*", relative_root="lib")
    filter_compiler_wrappers("Makefile.tau*", relative_root="lib64")

    def set_compiler_options(self, spec):
        useropt = ["-O2 -g", self.rpath_args]

        if self.spec.satisfies("%oneapi"):
            useropt.append("-Wno-error=implicit-function-declaration")

        ##########
        # Selecting a compiler with TAU configure is quite tricky:
        # 1 - compilers are mapped to a given set of strings
        #     (and spack cc, cxx, etc. wrappers are not among them)
        # 2 - absolute paths are not allowed
        # 3 - the usual environment variables seems not to be checked
        #     ('CC', 'CXX' and 'FC')
        # 4 - if no -cc=<compiler> -cxx=<compiler> is passed tau is built with
        #     system compiler silently
        compiler_flags: Dict[str, str] = {
            flag: os.path.basename(getattr(self.compiler, compiler))
            for flag, compiler in (("-cc", "cc"), ("-c++", "cxx"), ("-fortran", "fc"))
            if getattr(self.compiler, compiler)
        }

        if "~fortran" in spec:
            compiler_flags.pop("-fortran", None)

        # tau does not understand `craycc`, `crayCC`, `crayftn`, strip off the `cray` prefix
        for flag, value in compiler_flags.items():
            if value.startswith("cray"):
                compiler_flags[flag] = value[4:]

        compiler_options = [f"{flag}={value}" for flag, value in compiler_flags.items()]

        ##########

        # Construct the string of custom compiler flags and append it to
        # compiler related options
        useropt = " ".join(useropt)
        useropt = "-useropt=%s" % useropt
        compiler_options.append(useropt)
        return compiler_options

    def setup_build_environment(self, env):
        env.prepend_path("LIBRARY_PATH", self.spec["zlib-api"].prefix.lib)
        env.prepend_path("LIBRARY_PATH", self.spec["hwloc"].prefix.lib)

    def install(self, spec, prefix):
        # TAU isn't happy with directories that have '@' in the path.  Sigh.
        change_sed_delimiter("@", ";", "configure")
        change_sed_delimiter("@", ";", "utils/FixMakefile")
        change_sed_delimiter("@", ";", "utils/FixMakefile.sed.default")

        # TAU configure, despite the name , seems to be a manually
        # written script (nothing related to autotools).  As such it has
        # a few #peculiarities# that make this build quite hackish.
        options = ["-prefix=%s" % prefix]

        if "+craycnl" in spec:
            options.append("-arch=craycnl")

        if "+ppc64le" in spec:
            options.append("-arch=ibm64linux")

        if "+x86_64" in spec:
            options.append("-arch=x86_64")

        if "+pdt" in spec:
            options.append("-pdt=%s" % spec["pdt"].prefix)
            if spec["pdt"].satisfies("%intel"):
                options.append("-pdt_c++=icpc")

        if "+scorep" in spec:
            options.append("-scorep=%s" % spec["scorep"].prefix)

        if "+pthreads" in spec:
            options.append("-pthread")

        if "+likwid" in spec:
            options.append("-likwid=%s" % spec["likwid"].prefix)

        if "+papi" in spec:
            options.append("-papi=%s" % spec["papi"].prefix)

        if "+openmp" in spec:
            options.append("-openmp")

        if "+opari" in spec:
            options.append("-opari")

        if "+ompt" in spec:
            options.append("-ompt")

        if "+io" in spec:
            options.append("-iowrapper")

        if "+syscall" in spec:
            options.append("-syscall")

        if "+binutils" in spec:
            options.append("-bfd=%s" % spec["binutils"].prefix)

        if "+libdwarf" in spec:
            options.append("-dwarf=%s" % spec["libdwarf"].prefix)

        if "+elf" in spec:
            options.append("-elf=%s" % spec["elf"].prefix)

        if "+libunwind" in spec:
            options.append("-unwind=%s" % spec["libunwind"].prefix)

        if "+otf2" in spec:
            options.append("-otf=%s" % spec["otf2"].prefix)

        if "+mpi" in spec:
            env["CC"] = spec["mpi"].mpicc
            env["CXX"] = spec["mpi"].mpicxx
            if "+fortran" in spec:
                env["F77"] = spec["mpi"].mpif77
                env["FC"] = spec["mpi"].mpifc
            if spec["mpi"].name == "intel-oneapi-mpi":
                options.append("-mpiinc=%s/include" % spec["mpi"].package.component_prefix)
                options.append("-mpilib=%s/lib" % spec["mpi"].package.component_prefix)
            else:
                options.append("-mpiinc=%s" % spec["mpi"].prefix.include)
                options.append("-mpilib=%s" % spec["mpi"].prefix.lib)

            options.append("-mpi")
            if "+comm" in spec:
                options.append("-PROFILECOMMUNICATORS")

        if "+profileparam" in spec:
            options.append("-PROFILEPARAM")

        if "+shmem" in spec:
            options.append("-shmem")

        if "+gasnet" in spec:
            options.append("-gasnet=%s" % spec["gasnet"].prefix)

        if "+cuda" in spec:
            options.append("-cuda=%s" % spec["cuda"].prefix)

        if "+level_zero" in spec:
            options.append("-level_zero=%s" % spec["oneapi-level-zero"].prefix)

        if "+opencl" in spec:
            options.append("-opencl")

        if "+rocm" in spec:
            options.append("-rocm=%s" % spec["hsa-rocr-dev"].prefix)
            if spec.satisfies("@2.32.1"):
                options.append("-rocmsmi=%s" % spec["rocm-smi-lib"].prefix)
            if spec.satisfies("@2.34:"):
                options.append("-rocm-core=%s" % spec["rocm-core"].prefix)

        if "+rocprofiler" in spec:
            options.append("-rocprofiler=%s" % spec["rocprofiler-dev"].prefix)

        if "+roctracer" in spec:
            options.append("-roctracer=%s" % spec["roctracer-dev"].prefix)
            if spec.satisfies("@2.34:"):
                options.append("-hip=%s" % spec["hip"].prefix)

        if "+rocprofv2" in spec:
            options.append("-rocprofiler=%s" % spec["rocprofiler-dev"].prefix)
            options.append("-rocprofv2")

        if "+adios2" in spec:
            options.append("-adios=%s" % spec["adios2"].prefix)

        if "+sqlite" in spec:
            options.append("-sqlite3=%s" % spec["sqlite"].prefix)

        if "+phase" in spec:
            options.append("-PROFILEPHASE")

        if "+python" in spec:
            options.append("-python")
            # find Python.h (i.e. include/python2.7/Python.h)
            include_path = spec["python"].prefix.include
            found = False
            for root, dirs, files in os.walk(spec["python"].prefix.include):
                for filename in fnmatch.filter(files, "Python.h"):
                    include_path = root
                    break
                    found = True
                if found:
                    break
            options.append("-pythoninc=%s" % include_path)
            # find libpython*.* (i.e. lib/python2.7/libpython2.7.so)
            lib_path = spec["python"].prefix.lib
            found = False
            file_to_find = "libpython*.so"
            if platform.system() == "Darwin":
                file_to_find = "libpython*.dylib"
            for root, dirs, files in os.walk(spec["python"].prefix.lib):
                for filename in fnmatch.filter(files, file_to_find):
                    lib_path = root
                    break
                    found = True
                if found:
                    break
            options.append("-pythonlib=%s" % lib_path)
        if "+disable-no-pie" in spec:
            options.append("-disable-no-pie-on-ubuntu")

        if "+dyninst" in spec:
            options.append("-dyninst=%s" % spec["dyninst"].prefix)
            if "+tbb" not in spec:
                options.append("-tbb=%s" % spec["intel-tbb"].prefix)
            if "+boost" not in spec:
                options.append("-boost=%s" % spec["boost"].prefix)
            if "+elf" not in spec:
                options.append("-elf=%s" % spec["elfutils"].prefix)

        compiler_specific_options = self.set_compiler_options(spec)
        options.extend(compiler_specific_options)
        configure(*options)

        make("install")

        # Link arch-specific directories into prefix since there is
        # only one arch per prefix the way spack installs.
        self.link_tau_arch_dirs()
        # TAU may capture Spack's internal compiler wrapper. Replace
        # it with the correct compiler.

    def link_tau_arch_dirs(self):
        for subdir in os.listdir(self.prefix):
            for d in ("bin", "lib"):
                src = join_path(self.prefix, subdir, d)
                dest = join_path(self.prefix, d)
                if os.path.isdir(src) and not os.path.exists(dest):
                    os.symlink(join_path(subdir, d), dest)

    def setup_run_environment(self, env):
        pattern = join_path(self.prefix.lib, "Makefile.*")
        files = glob.glob(pattern)

        # This function is called both at install time to set up
        # the build environment and after install to generate the associated
        # module file. In the former case there is no `self.prefix.lib`
        # directory to inspect. The conditional below will set `TAU_MAKEFILE`
        # in the latter case.
        if files:
            env.set("TAU_MAKEFILE", files[0])
        if "+dyninst" in self.spec:
            path_to_dyn_lib = self.spec["dyninst"].prefix.lib
            dyninst_apirt = join_path(path_to_dyn_lib, "libdyninstAPI_RT.so")
            env.set("DYNINSTAPI_RT_LIB", dyninst_apirt)
            env.append_path("LD_LIBRARY_PATH", path_to_dyn_lib)
            env.append_path("LD_LIBRARY_PATH", self.prefix.lib)
        if "+cuda" in self.spec:
            env.append_path("PATH", self.spec["cuda"].prefix.bin)

    matmult_test = join_path("examples", "mm")
    dyninst_test = join_path("examples", "dyninst")
    makefile_test = join_path("examples", "Makefile")
    makefile_inc_test = join_path("include", "Makefile")
    cuda_test = join_path("examples", "gpu", "cuda", "dataElem_um")
    level_zero_test = join_path("examples", "gpu", "oneapi", "complex_mult")
    rocm_test = join_path("examples", "gpu", "hip", "vectorAdd")
    syscall_test = join_path("examples", "syscall")
    ompt_test = join_path("examples", "openmp", "c++")
    python_test = join_path("examples", "python")
    disable_tests = False

    @run_after("install")
    def setup_build_tests(self):
        """Copy the build test files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, self.matmult_test)
        cache_extra_test_sources(self, self.makefile_test)
        cache_extra_test_sources(self, self.makefile_inc_test)
        if "+dyninst" in self.spec:
            cache_extra_test_sources(self, self.dyninst_test)
        if "+cuda" in self.spec:
            cache_extra_test_sources(self, self.cuda_test)
        if "+level_zero" in self.spec:
            cache_extra_test_sources(self, self.level_zero_test)
        if "+rocm" in self.spec:
            cache_extra_test_sources(self, self.rocm_test)
        if "+syscall" in self.spec:
            cache_extra_test_sources(self, self.syscall_test)
        if "+ompt" in self.spec:
            cache_extra_test_sources(self, self.ompt_test)
        if "+python" in self.spec:
            cache_extra_test_sources(self, self.python_test)

    def _run_python_test(self, test_name, purpose, work_dir):
        tau_python = which(self.prefix.bin.tau_python)
        tau_py_inter = "-tau-python-interpreter=" + self.spec["python"].prefix.bin.python
        pprof = which(self.prefix.bin.pprof)
        with test_part(self, f"{test_name}", purpose, work_dir):
            if "+mpi" in self.spec:
                flag = "mpi"
                mpirun = which(self.spec["mpi"].prefix.bin.mpirun)
                mpirun(
                    "-np",
                    "4",
                    self.prefix.bin.tau_python,
                    tau_py_inter,
                    "-T",
                    flag,
                    "firstprime.py",
                )
            else:
                flag = "serial"
                tau_python(tau_py_inter, "-T", flag, "firstprime.py")
            pprof()

    def _run_default_test(self, test_name, purpose, work_dir):
        tau_exec = which(self.prefix.bin.tau_exec)
        pprof = which(self.prefix.bin.pprof)
        with test_part(self, f"{test_name}", purpose, work_dir):
            make("all")
            if "+mpi" in self.spec:
                flags = ["-T", "mpi"]
                mpirun = which(self.spec["mpi"].prefix.bin.mpirun)
                mpirun("-np", "4", self.prefix.bin.tau_exec, *flags, "./matmult")
            else:
                flags = ["-T", "serial"]
                tau_exec(*flags, "./matmult")
            pprof()

    def _run_ompt_test(self, test_name, purpose, work_dir):
        tau_exec = which(self.prefix.bin.tau_exec)
        pprof = which(self.prefix.bin.pprof)
        with test_part(self, f"{test_name}", purpose, work_dir):
            make("all")
            if "+mpi" in self.spec:
                flags = ["-T", "mpi", "-ompt"]
                mpirun = which(self.spec["mpi"].prefix.bin.mpirun)
                mpirun("-np", "4", self.prefix.bin.tau_exec, *flags, "./mandel")
            else:
                flags = ["-T", "serial", "-ompt"]
                tau_exec(*flags, "./mandel")
            pprof()

    def _run_rocm_test(self, test_name, purpose, work_dir):
        tau_exec = which(self.prefix.bin.tau_exec)
        pprof = which(self.prefix.bin.pprof)
        with test_part(self, f"{test_name}", purpose, work_dir):
            make("all")
            if "+mpi" in self.spec:
                flags = ["-T", "mpi", "-rocm"]
                mpirun = which(self.spec["mpi"].prefix.bin.mpirun)
                mpirun("-np", "4", self.prefix.bin.tau_exec, *flags, "./gpu-stream-hip")
            else:
                flags = ["-T", "serial", "-rocm"]
                tau_exec(*flags, "./gpu-stream-hip")
            pprof()

    def test_python(self):
        """test python variant"""
        if self.disable_tests:
            return
        if "+python" in self.spec:
            # current_test_cache_dir.examples.python
            python_test_dir = join_path(self.test_suite.current_test_cache_dir, self.python_test)
            self._run_python_test("test_tau_python", "Testing tau_python", python_test_dir)

    def test_default(self):
        """default matmult test"""
        if self.disable_tests:
            return
        if "+ompt" in self.spec:
            return
        default_test_dir = join_path(self.test_suite.current_test_cache_dir, self.matmult_test)
        self._run_default_test("test_default", "Testing TAU", default_test_dir)

    def test_ompt(self):
        """ompt test"""
        if self.disable_tests:
            return
        if "+ompt" in self.spec:
            ompt_test_dir = join_path(self.test_suite.current_test_cache_dir, self.ompt_test)
            self._run_ompt_test("test_ompt", "Testing ompt", ompt_test_dir)

    def test_rocm(self):
        """rocm test"""
        # Disabled, see PR#43682
        # make is unable to find rocm_agent_enumerator
        # when testing, with spack load, there is no issue
        return
        if self.disable_tests:
            return
        if "+rocm" in self.spec and (
            "+rocprofiler" in self.spec or "+roctracer" in self.spec or "+rocprofv2" in self.spec
        ):
            rocm_test_dir = join_path(self.test_suite.current_test_cache_dir, self.rocm_test)
            self._run_rocm_test("test_rocm", "Testing rocm", rocm_test_dir)
