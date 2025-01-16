# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCtranslate2(CMakePackage, PythonExtension, CudaPackage):
    """CTranslate2 is a C++ and Python library for efficient inference with
    Transformer models."""

    homepage = "https://github.com/OpenNMT/CTranslate2"
    git = "https://github.com/OpenNMT/CTranslate2.git"

    maintainers("meyersbs", "aweits")

    version("3.12.0", tag="v3.12.0", submodules=True)

    extends("python")

    # From setup.py, CMakeLists.txt, requirements.txt
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("cmake@3.7:", type="build")
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-pybind11", type=("build", "run"))
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pyyaml@5.3:6", type=("build", "run"))

    # From build errors
    depends_on("py-intel-openmp", type=("build", "run"))
    # From https://opennmt.net/CTranslate2/installation.html#build-options
    variant("mkl", default=True, description="Build with mkl")
    variant("cuda", default=False, description="Build with cuda")
    variant("cudnn", default=False, description="Build with cudnn")
    depends_on("mkl@2019.5:", when="+mkl", type=("build", "run"))
    depends_on("cuda@11.0:", when="+cuda", type=("build", "run"))
    depends_on("cudnn@8:", when="+cudnn", type=("build", "run"))

    def setup_build_environment(self, env):
        # https://opennmt.net/CTranslate2/installation.html#compile-the-python-wrapper
        env.append_path("SPACK_INCLUDE_DIRS", self.prefix.include)
        env.append_path("SPACK_LINK_DIRS", self.prefix.lib)
        env.append_path("SPACK_LINK_DIRS", self.prefix.lib64)
        env.set("CTRANSLATE2_ROOT", self.spec.prefix)

    @run_after("install")
    def install_python(self):
        args = std_pip_args + ["--prefix=" + prefix, "."]
        with working_dir("python"):
            pip(*args)

    def cmake_args(self):
        args = []
        # Disabling to avoid "multiple definition of" errors from cmake
        args.append("-DENABLE_CPU_DISPATCH=OFF")
        if "+mkl" in self.spec:
            args.append("-DWITH_MKL=ON")
        else:
            args.append("-DWITH_MKL=OFF")
        if "+cuda" in self.spec:
            args.append("-DWITH_CUDA=ON")
            cuda_arch_list = list(self.spec.variants["cuda_arch"].value)
            cuda_arch_list = " ".join([a[0] + "." + a[1] for a in cuda_arch_list])
            args.append("-DCUDA_ARCH_LIST={0}".format(cuda_arch_list))
        else:
            args.append("-DWITH_CUDA=OFF")
        if "+cudnn" in self.spec:
            args.append("-DWITH_CUDNN=ON")
        else:
            args.append("-DWITH_CUDNN=OFF")

        return args
