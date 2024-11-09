# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class ApacheTvm(CMakePackage, CudaPackage):
    """Apache TVM is an open source machine learning compiler framework for
    CPUs, GPUs, and machine learning accelerators. It aims to enable machine
    learning engineers to optimize and run computations efficiently on any
    hardware backend."""

    homepage = "https://tvm.apache.org/"
    url = "https://dlcdn.apache.org/tvm/tvm-v0.16.0/apache-tvm-src-v0.16.0.tar.gz"

    license("Apache-2.0", checked_by="alex391")

    version("0.16.0", sha256="55e2629c39248ef3b1ee280e34a960182bd17bea7ae0d0fa132bbdaaf5aba1ac")

    variant("llvm", default=True, description="Build with llvm for CPU codegen")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("cmake@3.18:", type="build")
    depends_on("python@3.7:3.8", type=("build", "run"))
    depends_on("zlib-api", type=("link", "run"))
    depends_on("ncurses", type=("link", "run"))
    depends_on("llvm@4:18.1.8", type="build", when="+llvm")
    depends_on("cuda@8:", when="+cuda")

    def cmake_args(self):
        return [
            self.define_from_variant("USE_CUDA", "cuda"),
            self.define_from_variant("USE_LLVM", "llvm"),
        ]
