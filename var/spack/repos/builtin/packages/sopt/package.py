# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sopt(CMakePackage):
    """SOPT is an open-source C++ package available under the license below. It performs
    Sparse OPTimisation using state-of-the-art convex optimisation algorithms. It solves a
    variety of sparse regularisation problems, including the Sparsity Averaging Reweighted
    Analysis (SARA) algorithm.
    """

    homepage = "https://astro-informatics.github.io/sopt/"
    url = "https://github.com/astro-informatics/sopt/archive/refs/tags/v4.2.0.tar.gz"
    git = "https://github.com/astro-informatics/sopt"

    maintainers("tkoskela", "mmcleod89", "20DM")
    license("GPL-2.0")

    version("4.2.0", sha256="25e579722f8e049d37c9155affa57ec2f38a2f8414c9cf430da2b7bafc86907b")

    variant("tests", default=False, description="Build tests")
    variant("examples", default=False, description="Build examples")
    variant("benchmarks", default=False, description="Build benchmarks")
    variant("openmp", default=False, description="Enable multithreading with OpenMP")
    variant("mpi", default=False, description="Enable parallelisation with MPI")
    variant("docs", default=False, description="Enable multithreading with OpenMP")
    variant("coverage", default=False, description="Enable code coverage")
    variant("onnxrt", default=False, description="Build with Tensorflow support using onnx")

    depends_on("cmake@3")
    depends_on("eigen@3.4")
    depends_on("libtiff@4.7:")
    depends_on("mpi", when="+mpi")
    depends_on("catch2@3.4:3", when="+tests")
    depends_on("benchmark@1.8~performance_counters", when="+benchmarks")
    depends_on("onnx@1.16:", when="+onnxrt")
    depends_on("py-onnxruntime@1.17.1:", when="+onnxrt")
    depends_on("doxygen@1.8:1.12+graphviz", when="+docs")

    patch(
        "https://github.com/astro-informatics/sopt/commit/836171f32d39a3fbc1147d6c302a08a61f842fee.patch?full_index=1",
        sha256="00729db4695712c3fb38aeb9e23a17107a7c8504c3a8249d9d4ddd2782d29661",
        when="@4.2.0",
    )

    def cmake_args(self):
        args = [
            self.define_from_variant("tests", "tests"),
            self.define_from_variant("examples", "examples"),
            self.define_from_variant("benchmarks", "benchmarks"),
            self.define_from_variant("openmp", "openmp"),
            self.define_from_variant("dompi", "mpi"),
            self.define_from_variant("docs", "docs"),
            self.define_from_variant("coverage", "coverage"),
            self.define_from_variant("onnxrt", "onnxrt"),
        ]
        return args

    def setup_run_environment(self, env):
        if "+tests" in self.spec:
            env.prepend_path("PATH", self.spec.prefix.tests)
        if "+examples" in self.spec:
            env.prepend_path("PATH", join_path(self.spec.prefix, "examples"))
        if "+benchmarks" in self.spec:
            env.prepend_path("PATH", join_path(self.spec.prefix, "benchmarks"))

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make("install")
            if "+tests" in spec:
                install_tree("cpp/tests", spec.prefix.tests)
            if "+examples" in spec:
                install_tree("cpp/examples", join_path(spec.prefix, "examples"))
            if "+benchmarks" in spec:
                install_tree("cpp/benchmarks", join_path(spec.prefix, "benchmarks"))
