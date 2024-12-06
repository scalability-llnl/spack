# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Spfft(CMakePackage, CudaPackage, ROCmPackage):
    """Sparse 3D FFT library with MPI, OpenMP, CUDA and ROCm support."""

    homepage = "https://github.com/eth-cscs/SpFFT"
    url = "https://github.com/eth-cscs/SpFFT/archive/v0.9.8.zip"
    git = "https://github.com/eth-cscs/SpFFT.git"

    maintainers("AdhocMan", "haampie")

    license("BSD-3-Clause")

    version("develop", branch="develop")
    version("master", branch="master")

    version("1.1.0", sha256="231454a3142bc56249b1b551ac5175882311365509cc111d7ad0e91ed5537102")
    version("1.0.6", sha256="e1b927c61f8abbb4a9937653f917169e6253e8c40b850df491594310943ca14b")
    version("1.0.5", sha256="2a59d856286ea8559f00a32fc38f9f7546209cfa90112232a5288a69689a6e05")
    version("1.0.4", sha256="41e63880d95343da0d8c3dbe5bfb3d46a1d612199cc9cc13a936f1628a7fdb8e")
    version("1.0.3", sha256="4f87734e3582ef96ddc0402d0db78cfc173bed9cab3e0d9c6a6bf8b660d69559")
    version("1.0.2", sha256="9b1296bda0b9ec3d37c74fd64354a01ebc6e2da7cb026c1f821882160b03c692")
    version("1.0.1", sha256="f8ab706309776cfbd2bfd8e29a6a9ffb5c8f3cd62399bf82db1e416ae5c490c8")
    version("1.0.0", sha256="bd98897aa6734563ec63cd84168e731ef2e2bbc01a574c6dc59b74475742b6ee")
    version("0.9.13", sha256="5ccc93c9362bec14cfb6e31dd0e7ae7e48db0453ab49ebc9722041b69db759ef")
    version("0.9.12", sha256="1f7bf5164dcceb0e3bbce7d6ff9faef3145ad17cf3430149d40a98c43c010acc")
    version("0.9.11", sha256="36542a60378e8672654188dee006975ef9e10f502791459ff7ebf4b38451cb9b")
    version("0.9.10", sha256="9cbbb7ba5e53e17eeb45e809841d8272e5333f739c2442a99c3e255c1ddec3e9")
    version("0.9.9", sha256="a8fd7a2d767716bb73185ca03bf4c106c6981b79130f3e456e5d2e744a2b3ba0")
    version("0.9.8", sha256="f49fa51316bbfa68309e951d2375e1f6904120c93868cbe13bc2974c0b801a3f")

    variant("openmp", default=True, description="Build with OpenMP support")
    variant("mpi", default=True, description="enable MPI")
    variant("single_precision", default=False, description="Sinlge precision")
    variant("gpu_direct", default=False, description="GPU aware MPI")
    variant("static", default=False, description="build static library")
    variant("fortran", default=False, description="enable fortran")
    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo"),
    )
    depends_on("fftw-api@3")
    depends_on("mpi", when="+mpi")
    depends_on("cmake@3.11:", type="build")
    depends_on("cmake@3.18:", type="build", when="@1.1.0:")
    depends_on("cmake@3.21:", type="build", when="@1.1.0: +rocm")

    depends_on("cuda@9:10", when="@:0.9.11 +cuda")
    depends_on("cuda@9:", when="@0.9.12:1.0.6 +cuda")
    depends_on("cuda@11:", when="@1.1.0: +cuda")

    # Workaround for compiler bug in ROCm 4.5+ added in SpFFT 1.0.6
    conflicts("+rocm", when="@:1.0.5")

    with when("+rocm"):
        depends_on("rocfft")
        depends_on("hipfft")
        # hip 6.0 requires v1.1.0 and later
        conflicts("^hip@6.0.0:", when="@:1.0.6 +rocm")

    # Fix compilation error in some cases due to missing include statement
    # before version 1.0.3
    patch("0001-fix-missing-limits-include.patch", when="@:1.0.2")

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define_from_variant("SPFFT_OMP", "openmp"),
            self.define_from_variant("SPFFT_MPI", "mpi"),
            self.define_from_variant("SPFFT_SINGLE_PRECISION", "single_precision"),
            self.define_from_variant("SPFFT_GPU_DIRECT", "gpu_direct"),
            self.define_from_variant("SPFFT_FORTRAN", "fortran"),
            self.define_from_variant("SPFFT_STATIC", "static"),
        ]

        if spec.satisfies("+cuda"):
            args += ["-DSPFFT_GPU_BACKEND=CUDA"]

            cuda_arch = self.spec.variants["cuda_arch"].value
            if cuda_arch[0] != "none":
                args += [self.define("CMAKE_CUDA_ARCHITECTURES", cuda_arch)]

        if spec.satisfies("@1.1.0: +rocm"):
            # v1.1.0 switched to CMake HIP language feature
            args += ["-DSPFFT_GPU_BACKEND=ROCM"]
            rocm_arch = self.spec.variants["amdgpu_target"].value
            if rocm_arch[0] != "none":
                args += [self.define("CMAKE_HIP_ARCHITECTURES", rocm_arch)]
        elif spec.satisfies("+rocm"):
            archs = ",".join(self.spec.variants["amdgpu_target"].value)
            args += [
                "-DSPFFT_GPU_BACKEND=ROCM",
                "-DHIP_ROOT_DIR={0}".format(spec["hip"].prefix),
                "-DHIP_HCC_FLAGS=--amdgpu-target={0}".format(archs),
                "-DHIP_CXX_COMPILER={0}".format(self.spec["hip"].hipcc),
            ]

        if "fftw" in spec:
            args += ["-DSPFFT_FFTW_LIB=FFTW"]
        elif "intel-mkl" in spec:
            args += ["-DSPFFT_FFTW_LIB=MKL"]

        return args
