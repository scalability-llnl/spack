# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.version import Version

from spack.pkg.builtin.rocm_config import RocmConfig

class RocmSuite(BundlePackage):
    """AMD ROCm Suite.
    """

    maintainers = ["srekolam", "renjithravindrankannath", "haampie", "kwryankrattiger"]
    tags = ["rocm"]

    variant("openmp", default=True, description="Enable OpenMP extensions for ROCm")
    variant("fortran", default=True, description="Enable Fortran extensions for ROCm")
      # - hipfort

    variant("blas", default=False, description="Enable BLAS extensions for ROCm")
      # - hipblas
    variant("fft", default=False, description="Enable FFT extensions for ROCm")
    variant("ai", default=False, description="Enable AI tools for ROCm")

      # - miopen-hip
    variant("opencl", default=False, description="Enable OpenCL extensions for ROCm")
    # - hip-rocclr # Needs fix for install
    # - rocm-opencl
    # - rocm-clang-ocl

    # variant("sycl", default=False, description="Enable Sycl extensions for ROCm")
    # - hipsycl # Needs fixes for to use llvm-amdgpu clang and update to package

    variant("dev", default=False, description="Enable Development/Debugging tools for ROCm")

    for _version, _config in RocmConfig.rocm_versions.items():
        version(_version, **_config)
        depends_on("rocm-config@{0}".format(_version), when="@{0}".format(_version))

        depends_on("hip@{0}".format(_version), when="@{0}".format(_version))
        depends_on("llvm-amdgpu@{0}".format(_version), when="@{0}".format(_version))
        depends_on("hsa-rocr-dev@{0}".format(_version), when="@{0}".format(_version))

        # - rocprim amdgpu_target=gfx1030
        # - rocrand amdgpu_target=gfx1030

        # Fortran
        depends_on("hipfort@{0}".format(_version), when="@{0} +fortran".format(_version))

        # OpenMP
        depends_on("rocm-openmp-extras@{0}".format(_version), when="@{0} +fortran".format(_version))
        depends_on("rocm-openmp-extras@{0}".format(_version), when="@{0} +openmp".format(_version))

        # Fortran
        depends_on("hipfort@{0}".format(_version), when="@{0} +fortran".format(_version))

        # FFT
        depends_on("hipfft@{0}".format(_version), when="@{0} +fft".format(_version))
        depends_on("rocfft@{0}".format(_version), when="@{0} +fft".format(_version))

        # Dev
        depends_on("hipify-clang@{0}".format(_version), when="@{0} +dev".format(_version))
        depends_on("rocm-cmake@{0}".format(_version), when="@{0} +dev".format(_version))
        depends_on("rocm-dbgapi@{0}".format(_version), when="@{0} +dev".format(_version))
        depends_on("rocm-debug-agent@{0}".format(_version), when="@{0} +dev".format(_version))
        depends_on("rocm-gdb@{0}".format(_version), when="@{0} +dev".format(_version))
        depends_on("rocm-info@{0}".format(_version), when="@{0} +dev".format(_version))
        depends_on("rocprofilter-dev@{0}".format(_version), when="@{0} +dev".format(_version))
        depends_on("roctracer-dev@{0}".format(_version), when="@{0} +dev".format(_version))
        depends_on("roctracer-dev-api@{0}".format(_version), when="@{0} +dev".format(_version))

    """
      - hipcub
        # - rocm-validation-suite # Needs hip-rocclr
        # - rocm-smi # Deprecated after 4.1.0 in favor of rocm-smi-lib
        # - rocm-smi-lib

        # BLAS
        # - hipblas
        # - rocblas amdgpu_target=gfx1030
        # - rocm-tensile # Build issues, excluded from suite because it is implicit with rocblas

        # Thrust (includes CUB)
        # - rocthrust
        # - hipcub

        # Linear Algebra Solvers
        # - hipsolver
        # - hipsparse
        # - rocsolver ~optimal amdgpu_target=gfx1030 # Disabling optimal to improve build time
        # - rocsparse amdgpu_target=gfx1030
        # - rocalution

      - rocalution
      - rocblas amdgpu_target=gfx1030
      # - hipsycl # Needs fixes for to use llvm-amdgpu clang
      # - rocm-smi # Deprecated after 4.1.0 in favor of rocm-smi-lib
      - rocm-smi-lib
      # - rocm-tensile # Build issues
      # - rocm-validation-suite # Needs hip-rocclr
      - rocprim amdgpu_target=gfx1030
      - rocrand amdgpu_target=gfx1030
      - rocthrust
    """

    # conflicts("cuda-suite")
    conflicts("rocm-device-libs", msg="ROCm device libs are now built by llvm-amdgpu")

    # Add compiler minimum versions based on the first release where the
    # processor is included in llvm/lib/Support/TargetParser.cpp
    depends_on("llvm-amdgpu@4.1.0:", when="^rocm-config amdgpu_target=gfx900:xnack-")
    depends_on("llvm-amdgpu@4.1.0:", when="^rocm-config amdgpu_target=gfx906:xnack-")
    depends_on("llvm-amdgpu@4.1.0:", when="^rocm-config amdgpu_target=gfx908:xnack-")
    depends_on("llvm-amdgpu@4.1.0:", when="^rocm-config amdgpu_target=gfx90c")
    depends_on("llvm-amdgpu@4.3.0:", when="^rocm-config amdgpu_target=gfx90a")
    depends_on("llvm-amdgpu@4.3.0:", when="^rocm-config amdgpu_target=gfx90a:xnack-")
    depends_on("llvm-amdgpu@4.3.0:", when="^rocm-config amdgpu_target=gfx90a:xnack+")
    depends_on("llvm-amdgpu@5.2.0:", when="^rocm-config amdgpu_target=gfx940")
    depends_on("llvm-amdgpu@4.5.0:", when="^rocm-config amdgpu_target=gfx1013")
    depends_on("llvm-amdgpu@3.8.0:", when="^rocm-config amdgpu_target=gfx1030")
    depends_on("llvm-amdgpu@3.9.0:", when="^rocm-config amdgpu_target=gfx1031")
    depends_on("llvm-amdgpu@4.1.0:", when="^rocm-config amdgpu_target=gfx1032")
    depends_on("llvm-amdgpu@4.1.0:", when="^rocm-config amdgpu_target=gfx1033")
    depends_on("llvm-amdgpu@4.3.0:", when="^rocm-config amdgpu_target=gfx1034")
    depends_on("llvm-amdgpu@4.5.0:", when="^rocm-config amdgpu_target=gfx1035")
    depends_on("llvm-amdgpu@5.2.0:", when="^rocm-config amdgpu_target=gfx1036")
    depends_on("llvm-amdgpu@5.3.0:", when="^rocm-config amdgpu_target=gfx1100")
    depends_on("llvm-amdgpu@5.3.0:", when="^rocm-config amdgpu_target=gfx1101")
    depends_on("llvm-amdgpu@5.3.0:", when="^rocm-config amdgpu_target=gfx1102")
    depends_on("llvm-amdgpu@5.3.0:", when="^rocm-config amdgpu_target=gfx1103")
    conflicts("^blt@:0.3.6", when="+rocm")
