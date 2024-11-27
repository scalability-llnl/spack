# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyCupy(PythonPackage, CudaPackage, ROCmPackage):
    """CuPy is an open-source array library accelerated with
    NVIDIA CUDA. CuPy provides GPU accelerated computing with
    Python. CuPy uses CUDA-related libraries including cuBLAS,
    cuDNN, cuRand, cuSolver, cuSPARSE, cuFFT and NCCL to make
    full use of the GPU architecture."""

    homepage = "https://cupy.dev/"
    pypi = "cupy/cupy-8.0.0.tar.gz"

    version("13.1.0", sha256="5caf62288481a27713384523623045380ff42e618be4245f478238ed1786f32d")
    version("12.1.0", sha256="f6d31989cdb2d96581da12822e28b102f29e254427195c2017eac327869b7320")
    version("12.0.0", sha256="61ddbbef73d50d606bd5087570645f3c91ec9176c2566784c1d486d6a3404545")
    version("11.6.0", sha256="53dbb840072bb32d4bfbaa6bfa072365a30c98b1fcd1f43e48969071ad98f1a7")
    version("11.5.0", sha256="4bc8565bded22cc89b210fd9fb48a5d5316f30701e12bb23852a60314e1f9f6e")
    version("11.4.0", sha256="03d52b2626e02a3a2b46d714c1cd03e702c8fe33915fcca6ed8de5c539964f49")
    version("11.3.0", sha256="d057cc2f73ecca06fae8b9c270d9e14116203abfd211a704810cc50a453b4c9e")
    version("11.2.0", sha256="c33361f117a347a63f6996ea97446d17f1c038f1a1f533e502464235076923e2")

    depends_on("cxx", type="build")  # generated

    variant("all", default=False, description="Enable optional py-scipy, optuna, and cython")

    depends_on("python@3.7:", when="@:11", type=("build", "run"))
    depends_on("python@3.8:", when="@12:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.29.22:2", type="build")
    depends_on("py-fastrlock@0.5:", type=("build", "run"))
    depends_on("py-numpy@1.20:1.25", when="@:11", type=("build", "run"))
    depends_on("py-numpy@1.20:1.26", when="@12:", type=("build", "run"))
    depends_on("py-numpy@1.22:1.28", when="@13:", type=("build", "run"))

    depends_on("py-scipy@1.6:1.12", when="@:12+all", type=("build", "run"))
    depends_on("py-scipy@1.7:1.13", when="@13:+all", type=("build", "run"))
    depends_on("py-cython@0.29.22:2", when="+all", type=("build", "run"))
    depends_on("py-optuna@2:", when="+all", type=("build", "run"))

    # Based on https://github.com/cupy/cupy/releases
    depends_on("cuda@:11.9", when="@:11 +cuda")
    depends_on("cuda@:12.1", when="@12:12.1.0 +cuda")
    depends_on("cuda@:12.4", when="@13: +cuda")

    for a in CudaPackage.cuda_arch_values:
        depends_on("nccl +cuda cuda_arch={0}".format(a), when="+cuda cuda_arch={0}".format(a))

    depends_on("cudnn@8.8", when="@12.0.0: +cuda")
    depends_on("cudnn@8.5", when="@11.2.0:11.6.0 +cuda")
    depends_on("cutensor", when="@:12.1.0 +cuda")
    depends_on("cutensor@2.0.1.2", when="@13.1: +cuda")

    for _arch in ROCmPackage.amdgpu_targets:
        arch_str = "amdgpu_target={0}".format(_arch)
        rocm_str = "+rocm {0}".format(arch_str)
        depends_on("rocprim {0}".format(arch_str), when=rocm_str, type=("link"))
        depends_on("rocsolver {0}".format(arch_str), when=rocm_str, type=("link"))
        depends_on("rocthrust {0}".format(arch_str), when=rocm_str, type=("link"))
        depends_on("rocrand {0}".format(arch_str), when=rocm_str, type=("link"))
        depends_on("hipcub {0}".format(rocm_str), when=rocm_str, type=("link"))
        depends_on("hipblas {0}".format(rocm_str), when=rocm_str, type=("link"))
        depends_on("hiprand {0}".format(rocm_str), when=rocm_str, type=("link"))
        depends_on("hipsparse {0}".format(rocm_str), when=rocm_str, type=("link"))
        depends_on("hipfft {0}".format(rocm_str), when=rocm_str, type=("link"))

    depends_on("rccl", when="+rocm", type=("link"))
    depends_on("roctracer-dev", when="+rocm", type=("link"))
    depends_on("rocprofiler-dev", when="+rocm", type=("link"))

    conflicts("~cuda ~rocm")
    conflicts("+cuda +rocm")
    conflicts("+cuda cuda_arch=none")

    def setup_build_environment(self, env):
        env.set("CUPY_NUM_BUILD_JOBS", make_jobs)
        if self.spec.satisfies("+cuda"):
            cuda_arch = self.spec.variants["cuda_arch"].value
            arch_str = ";".join("arch=compute_{0},code=sm_{0}".format(i) for i in cuda_arch)
            env.set("CUPY_NVCC_GENERATE_CODE", arch_str)
        elif self.spec.satisfies("+rocm"):
            spec = self.spec

            incs = {
                "roctracer-dev": ["include/roctracer"],
                "hiprand": ["include"],
                "rocrand": ["include"],
                "rocthrust": ["include"],
                "rocprim": ["include"],
                "hip": ["include", "include/hip"],
            }

            inc_dirs = []
            for pkg, ds in incs.items():
                for d in ds:
                    p = os.path.join(spec[pkg].prefix, d)
                    if os.path.exists(p):
                        inc_dirs.append(p)

            env.set("CUPY_INCLUDE_PATH", ":".join(inc_dirs))

            env.set("HIPCC", self.spec["hip"].hipcc)
            env.set("ROCM_HOME", self.spec["hipcub"].prefix)
            env.set("CUPY_INSTALL_USE_HIP", 1)
