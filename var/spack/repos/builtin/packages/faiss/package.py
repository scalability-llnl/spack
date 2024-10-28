# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Faiss(AutotoolsPackage, CMakePackage, CudaPackage):
    """Faiss is a library for efficient similarity search and clustering of
     dense vectors.

    Faiss contains algorithms that search in sets of vectors of any size, up
    to ones that possibly do not fit in RAM. It also contains supporting code
    for evaluation and parameter tuning. Faiss is written in C++ with
    complete wrappers for Python/numpy. Some of the most useful algorithms
    are implemented on the GPU. It is developed by Facebook AI Research.
    """

    homepage = "https://github.com/facebookresearch/faiss"
    url = "https://github.com/facebookresearch/faiss/archive/v1.6.3.tar.gz"

    maintainers("bhatiaharsh", "rblake-llnl", "lpottier")

    build_system(
        conditional("cmake", when="@1.7:"), conditional("autotools", when="@:1.6"), default="cmake"
    )

    license("MIT")

    version("1.8.0", sha256="56ece0a419d62eaa11e39022fa27c8ed6d5a9b9eb7416cc5a0fdbeab07ec2f0c")
    version("1.7.4", sha256="d9a7b31bf7fd6eb32c10b7ea7ff918160eed5be04fe63bb7b4b4b5f2bbde01ad")
    version("1.7.2", sha256="d49b4afd6a7a5b64f260a236ee9b2efb760edb08c33d5ea5610c2f078a5995ec")
    version("1.6.3", sha256="e1a41c159f0b896975fbb133e0240a233af5c9286c09a28fde6aefff5336e542")
    version("1.5.3", sha256="b24d347b0285d01c2ed663ccc7596cd0ea95071f3dd5ebb573ccfc28f15f043b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("python", default=False, description="Build Python bindings")
    variant("shared", default=False, description="Build shared library")
    variant("tests", default=False, description="Build Tests")

    conflicts("+tests", when="~python", msg="+tests must be accompanied by +python")

    depends_on("cmake@3.17:", when="build_system=cmake", type="build")
    depends_on("cmake@3.23.1:", when="build_system=cmake @1.7.4:", type="build")

    extends("python", when="+python")
    depends_on("python@3.7:", when="+python", type=("build", "run"))
    depends_on("py-pip", when="+python", type="build")
    depends_on("py-wheel", when="+python", type="build")
    depends_on("py-setuptools", when="+python", type="build")
    depends_on("py-numpy", when="+python", type=("build", "run"))
    depends_on("swig@4", when="+python", type="build")
    depends_on("py-scipy", when="+python+tests", type=("build", "run"))

    depends_on("blas")

    # patch for v1.5.3
    # faiss assumes that the "source directory" will always
    # be called "faiss" (not spack-src or faiss-1.5.3)
    # so, we will have to create a symlink to self (faiss did that in 1.6.3)
    # and add an include path
    patch("fixes-in-v1.5.3.patch", when="@1.5.3")

    # patch for v1.6.3
    # for v1.6.3, GPU build has a bug (two files need to be deleted)
    # https://github.com/facebookresearch/faiss/issues/1159
    # also, some include paths in gpu/tests/Makefile are missing
    patch("fixes-in-v1.6.3.patch", when="@1.6.3")

    # patch for v1.7.2
    # a shared object is missing in the python/setup.py
    #   https://github.com/facebookresearch/faiss/issues/2063
    #   https://github.com/facebookresearch/faiss/pull/2062
    # a header is missing in a test file
    #   https://github.com/facebookresearch/faiss/issues/2300
    patch("fixes-in-v1.7.2.patch", when="@1.7.2")

    def setup_run_environment(self, env):
        if self.spec.satisfies("+python"):
            env.prepend_path("PYTHONPATH", python_platlib)
            if self.spec.satisfies("platform=darwin"):
                env.append_path(
                    "DYLD_FALLBACK_LIBRARY_PATH", os.path.join(python_platlib, "faiss")
                )
            else:
                env.append_path("LD_LIBRARY_PATH", os.path.join(python_platlib, "faiss"))


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        spec = self.spec
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("FAISS_ENABLE_PYTHON", "python"),
            self.define_from_variant("FAISS_ENABLE_GPU", "cuda"),
            self.define_from_variant("BUILD_TESTING", "tests"),
            self.define("FAISS_OPT_LEVEL", "generic"),
        ]

        if spec.satisfies("+cuda"):
            key = "CMAKE_CUDA_ARCHITECTURES"
            args.append(self.define_from_variant(key, "cuda_arch"))
            # args.append(self.define_from_variant(
            # 'CMAKE_CUDA_STANDARD', 'cudastd'))
        return args

    def install(self, pkg, spec, prefix):
        super().install(pkg, spec, prefix)
        if spec.satisfies("+python"):

            class CustomPythonPipBuilder(spack.build_systems.python.PythonPipBuilder):
                def __init__(self, pkg, build_dirname):
                    spack.build_systems.python.PythonPipBuilder.__init__(self, pkg)
                    self.build_dirname = build_dirname

                @property
                def build_directory(self):
                    return os.path.join(self.pkg.stage.path, self.build_dirname, "faiss", "python")

            customPip = CustomPythonPipBuilder(pkg, self.build_dirname)
            customPip.install(pkg, spec, prefix)


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    def configure_args(self):
        args = []
        args.extend(self.with_or_without("cuda", activation_value="prefix"))
        return args

    def build(self, pkg, spec, prefix):
        make()

        if self.spec.satisfies("+python"):
            make("-C", "python")

        # CPU tests
        if self.spec.satisfies("+tests"):
            with working_dir("tests"):
                make("gtest")
                make("tests")

        # GPU tests
        if self.spec.satisfies("+tests+cuda"):
            with working_dir(os.path.join("gpu", "test")):
                make("gtest")
                make("build")  # target added by the patch
                make("demo_ivfpq_indexing_gpu")

    def install(self, pkg, spec, prefix):
        make("install")

        if self.spec.satisfies("+python"):
            with working_dir("python"):
                args = std_pip_args + ["--prefix=" + prefix, "."]
                pip(*args)

        if "+tests" not in self.spec:
            return

        if not os.path.isdir(self.prefix.bin):
            os.makedirs(self.prefix.bin)

        def _prefix_and_install(file):
            os.rename(file, "faiss_" + file)
            install("faiss_" + file, self.prefix.bin)

        # CPU tests
        with working_dir("tests"):
            # rename the exec to keep consistent with gpu tests
            os.rename("tests", "TestCpu")
            _prefix_and_install("TestCpu")

        # GPU tests
        if self.spec.satisfies("+cuda"):
            with working_dir(os.path.join("gpu", "test")):
                _prefix_and_install("TestGpuIndexFlat")
                _prefix_and_install("TestGpuIndexBinaryFlat")
                _prefix_and_install("TestGpuIndexIVFFlat")
                _prefix_and_install("TestGpuIndexIVFPQ")
                _prefix_and_install("TestGpuMemoryException")
                _prefix_and_install("TestGpuSelect")
                _prefix_and_install("demo_ivfpq_indexing_gpu")

    @run_after("configure")
    def _fix_makefile(self):
        # spack injects its own optimization flags
        makefile = FileFilter("makefile.inc")
        makefile.filter("CPUFLAGS     = -mavx2 -mf16c", "#CPUFLAGS     = -mavx2 -mf16c")
