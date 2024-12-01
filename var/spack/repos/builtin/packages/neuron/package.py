# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_environment import optimization_flags
from spack.package import *


class Neuron(CMakePackage):
    """NEURON is a simulation environment for single and networks of neurons.

    NEURON is a simulation environment for modeling individual and networks of
    neurons. NEURON models individual neurons via the use of sections that are
    automatically subdivided into individual compartments, instead of
    requiring the user to manually create compartments.
    """

    homepage = "https://www.neuron.yale.edu/"
    url = "https://github.com/neuronsimulator/nrn/releases/download/8.2.3/nrn-full-src-package-8.2.3.tar.gz"
    git = "https://github.com/neuronsimulator/nrn"
    maintainers("pramodk", "nrnhines", "iomaganaris", "ohm314", "matz-e")

    license("BSD-3-Clause")

    version("develop", branch="master", submodules="True")

    version(
        "8.2.3", tag="8.2.3", commit="f0ed3701059aa53ce93387f3d73d13c45de6d87f", submodules="True"
    )
    version(
        "8.1.0", tag="8.1.0", commit="047dd8240c2badadf5ea154b563b29369db1303f", submodules="True"
    )
    version(
        "8.0.0", tag="8.0.0", commit="429d11ef34b1d860b3ddbfffc9f7960acb399b0c", submodules="True"
    )
    version(
        "7.8.2", tag="7.8.2", commit="09b151ecb2b3984335c265932dc6ba3e4fcb318e", submodules="True"
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("backtrace", default=False, description="Enable printing backtraces on failure")
    variant("interviews", default=False, description="Enable GUI with INTERVIEWS")
    variant("legacy-unit", default=False, description="Enable legacy units")
    variant("mpi", default=True, description="Enable MPI parallelism")
    variant("python", default=True, description="Enable python")
    variant("shared", default=True, description="Build shared library (CoreNEURON)")
    variant("tests", default=False, description="Enable building tests")
    variant("rx3d", default=False, description="Enable cython translated 3-d rxd.", when="+python")

    # variants from coreneuron support
    variant("coreneuron", default=True, description="Enable CoreNEURON support")
    variant(
        "gpu", default=False, description="Enable GPU build (with NVHPC)", when="@9:+coreneuron"
    )
    variant(
        "openmp", default=False, description="Enable CoreNEURON OpenMP support", when="+coreneuron"
    )
    variant(
        "sympy",
        default=False,
        description="Use NMODL with SymPy to solve ODEs",
        when="@9:+coreneuron",
    )
    variant("caliper", default=False, description="Add Caliper support")

    generator("ninja")

    depends_on("bison@3:", type="build")
    depends_on("flex@2.6:", type="build")
    depends_on("ninja", type="build")

    depends_on("gettext")
    depends_on("libdwarf", when="+backtrace")
    depends_on("mpi", when="+mpi")
    depends_on("ncurses")
    depends_on("readline")

    depends_on("python", when="+python")
    depends_on("py-pytest", when="+python+tests")
    depends_on("py-mpi4py", when="+mpi+python+tests")
    depends_on("py-numpy", when="+python")
    depends_on("py-cython", when="+rx3d", type="build")
    depends_on("py-pytest-cov", when="+tests")

    # next two needed after neuronsimulator/nrn#2235.
    depends_on("py-pip", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-packaging", type="run")

    depends_on("boost", when="+coreneuron+tests")
    depends_on("cuda", when="+coreneuron+gpu")
    depends_on("py-sympy@1.3:", when="+coreneuron")

    depends_on("caliper", when="+caliper")

    gpu_compiler_message = "neuron+gpu needs %nvhpc"
    requires("%nvhpc", when="+gpu", msg=gpu_compiler_message)

    patch("patch-v782-git-cmake-avx512.patch", when="@7.8.2")

    def cmake_args(self):
        spec = self.spec
        args = []
        for variant in ["backtrace", "coreneuron", "interviews", "mpi", "python", "rx3d", "tests"]:
            args.append(self.define_from_variant("NRN_ENABLE_" + variant.upper(), variant))

        args.append(self.define_from_variant("CORENRN_ENABLE_SHARED", "shared"))

        if spec.satisfies("@:8"):
            args.append(self.define("NRN_ENABLE_BINARY_SPECIAL", "ON"))

        if "+python" in spec:
            args.append(self.define("PYTHON_EXECUTABLE", spec["python"].command.path))

        if "+legacy-unit" in spec and spec.satisfies("@:8"):
            args.append(self.define("NRN_DYNAMIC_UNITS_USE_LEGACY", "ON"))

        if "+caliper" in spec:
            args.append(self.define("NRN_ENABLE_PROFILING", "ON"))
            args.append(self.define("NRN_PROFILER", "caliper"))

        if spec.satisfies("+coreneuron"):
            options = [
                self.define("CORENRN_ENABLE_SPLAYTREE_QUEUING", "ON"),
                self.define("CORENRN_ENABLE_TIMEOUT", "OFF"),
                self.define_from_variant("CORENRN_ENABLE_OPENMP", "openmp"),
                self.define_from_variant("CORENRN_ENABLE_LEGACY_UNITS", "legacy-unit"),
                self.define_from_variant("CORENRN_ENABLE_UNIT_TESTS", "tests"),
            ]

            nmodl_options = "codegen --force"
            if spec.satisfies("+sympy"):
                nmodl_options += " sympy --analytic"
            options.append(self.define("CORENRN_NMODL_FLAGS", nmodl_options))

            if spec.satisfies("+gpu"):
                nvcc = spec["cuda"].prefix.bin.nvcc
                options.append(self.define("CMAKE_CUDA_COMPILER", nvcc))
                options.append(self.define("CORENRN_ENABLE_GPU", True))

            args.extend(options)

        # Enable math optimisations to enable SIMD/vectorisation in release modes
        if spec.satisfies("build_type=Release") or spec.satisfies("build_type=RelWithDebInfo"):
            args.append(self.define("NRN_ENABLE_MATH_OPT", "ON"))

        # add cpu arch specific optimisation flags to CMake so that they are passed
        # to embedded Makefile that neuron has for compiling MOD files
        compilation_flags = optimization_flags(self.compiler, self.spec.target)
        args.append(self.define("CMAKE_CXX_FLAGS", compilation_flags))

        return args

    @run_after("install")
    def filter_compilers(self):
        """run after install to avoid spack compiler wrappers
        getting embded into nrnivmodl script"""

        spec = self.spec

        if spec.satisfies("+mpi"):
            cc_compiler = spec["mpi"].mpicc
            cxx_compiler = spec["mpi"].mpicxx
        else:
            cc_compiler = self.compiler.cc
            cxx_compiler = self.compiler.cxx

        kwargs = {"backup": False, "string": True}
        nrnmech_makefile = join_path(self.prefix, "bin/nrnmech_makefile")

        # assign_operator is changed to fix wheel support
        assign_operator = "?=" if spec.satisfies("@:7") else "="

        # replace compilers from makefile
        compilers = [("CC", "cc_compiler"), ("CXX", "cxx_compiler")]
        for compiler_var, compiler_env in compilers:
            pattern = "(?:^|\\s){0}\\s*{1}.+".format(compiler_var, assign_operator)
            replacement = "{0} = {1}".format(compiler_var, locals()[compiler_env])
            filter_file(pattern, replacement, nrnmech_makefile)

        if spec.satisfies("@8:+coreneuron"):
            nrnmakefile = join_path(self.prefix, "share/coreneuron/nrnivmodl_core_makefile")
            filter_file("(?:^|\\s)CXX\\s*=.+", "CXX = {0}".format(cxx_compiler), nrnmakefile)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", join_path(self.prefix, "bin"))
        env.prepend_path("LD_LIBRARY_PATH", join_path(self.prefix, "lib"))
        if self.spec.satisfies("+python"):
            env.prepend_path("PYTHONPATH", self.spec.prefix.lib.python)
