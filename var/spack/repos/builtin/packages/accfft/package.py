# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Accfft(CMakePackage, CudaPackage):
    """AccFFT extends existing FFT libraries for CUDA-enabled
    Graphics Processing Units (GPUs) to distributed memory clusters
    """

    homepage = "http://accfft.org"
    git = "https://github.com/amirgholami/accfft.git"

    license("GPL-2.0-only")

    version("develop", branch="master")

    depends_on("cxx", type="build")  # generated

    variant("pnetcdf", default=True, description="Add support for parallel NetCDF")
    variant("shared", default=True, description="Enables the build of shared libraries")

    # See: http://accfft.org/articles/install/#installing-dependencies
    depends_on("fftw precision=float,double ~mpi+openmp")

    depends_on("parallel-netcdf", when="+pnetcdf")

    # fix error [-Wc++11-narrowing]
    patch("fix_narrowing_error.patch")

    parallel = False

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define("FFTW_ROOT", spec["fftw"].prefix),
            self.define("FFTW_USE_STATIC_LIBS", "false"),
            self.define("BUILD_GPU", str(spec.satisfies("+cuda")).lower()),
            self.define("BUILD_SHARED", str(spec.satisfies("+shared")).lower()),
        ]

        if spec.satisfies("+cuda"):
            cuda_arch = [x for x in spec.variants["cuda_arch"].value if x]
            if cuda_arch:
                args.append(f"-DCUDA_NVCC_FLAGS={' '.join(self.cuda_flags(cuda_arch))}")

        return args
