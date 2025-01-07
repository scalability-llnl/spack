# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AmrWind(CMakePackage, CudaPackage, ROCmPackage):
    """AMR-Wind is a massively parallel, block-structured adaptive-mesh,
    incompressible flow sover for wind turbine and wind farm simulations."""

    homepage = "https://github.com/Exawind/amr-wind"
    url = "https://github.com/Exawind/amr-wind/archive/refs/tags/v1.3.0.tar.gz"
    git = "https://github.com/Exawind/amr-wind.git"

    maintainers("jrood-nrel", "psakievich")

    tags = ["ecp", "ecp-apps"]

    license("BSD-3-Clause")

    version("main", branch="main", submodules=True)
    version("3.3.1", tag="v3.3.1", submodules=True)
    version("3.3.0", tag="v3.3.0", submodules=True)
    version("3.2.3", tag="v3.2.3", submodules=True)
    version("3.2.2", tag="v3.2.2", submodules=True)
    version("3.2.1", tag="v3.2.1", submodules=True)
    version("3.2.0", tag="v3.2.0", submodules=True)
    version("3.1.7", tag="v3.1.7", submodules=True)
    version("3.1.6", tag="v3.1.6", submodules=True)
    version("3.1.5", tag="v3.1.5", submodules=True)
    version("3.1.4", tag="v3.1.4", submodules=True)
    version("3.1.3", tag="v3.1.3", submodules=True)
    version("3.1.2", tag="v3.1.2", submodules=True)
    version("3.1.1", tag="v3.1.1", submodules=True)
    version("3.1.0", tag="v3.1.0", submodules=True)
    version("3.0.2", tag="v3.0.2", submodules=True)
    version("3.0.1", tag="v3.0.1", submodules=True)
    version("3.0.0", tag="v3.0.0", submodules=True)
    version("2.6.0", tag="v2.6.0", submodules=True)
    version("2.5.0", tag="v2.5.0", submodules=True)
    version("2.4.3", tag="v2.4.3", submodules=True)
    version("2.4.2", tag="v2.4.2", submodules=True)
    version("2.4.1", tag="v2.4.1", submodules=True)
    version("2.4.0", tag="v2.4.0", submodules=True)
    version("2.3.2", tag="v2.3.2", submodules=True)
    version("2.3.1", tag="v2.3.1", submodules=True)
    version("2.3.0", tag="v2.3.0", submodules=True)
    version("2.2.1", tag="v2.2.1", submodules=True)
    version("2.2.0", tag="v2.2.0", submodules=True)
    version("2.1.0", tag="v2.1.0", submodules=True)
    version("2.0.0", tag="v2.0.0", submodules=True)
    version("1.4.0", tag="v1.4.0", submodules=True)
    version("1.3.1", tag="v1.3.1", submodules=True)
    version("1.3.0", tag="v1.3.0", submodules=True)
    version("1.2.1", tag="v1.2.1", submodules=True)
    version("1.2.0", tag="v1.2.0", submodules=True)
    version("1.1.0", tag="v1.1.0", submodules=True)
    version("1.0.1", tag="v1.0.1", submodules=True)
    version("1.0.0", tag="v1.0.0", submodules=True)
    version("0.9.0", tag="v0.9.0", submodules=True)

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("hypre", default=False, description="Enable Hypre integration")
    variant("ascent", default=False, description="Enable Ascent integration")
    variant("masa", default=False, description="Enable MASA integration")
    variant("mpi", default=True, description="Enable MPI support")
    variant("netcdf", default=False, description="Enable NetCDF support")
    variant("openfast", default=False, description="Enable OpenFAST integration")
    variant("openmp", default=False, description="Enable OpenMP for CPU builds")
    variant("shared", default=True, description="Build shared libraries")
    variant("tests", default=True, description="Activate regression tests")
    variant("tiny_profile", default=False, description="Activate tiny profile")
    variant("hdf5", default=False, description="Enable HDF5 plots with ZFP compression")
    variant("umpire", default=False, description="Enable UMPIRE memory pooling")
    variant("sycl", default=False, description="Enable SYCL backend")
    variant("gpu-aware-mpi", default=False, description="Enable GPU aware MPI")
    variant("helics", default=False, description="Enable HELICS support for control interface")
    variant(
        "waves2amr", default=False, description="Enable Waves2AMR support for ocean wave input"
    )
    variant("fft", default=False, description="Enable FFT support for MAC projection")

    depends_on("mpi", when="+mpi")
    depends_on("hdf5~mpi", when="+hdf5~mpi")
    depends_on("hdf5+mpi", when="+hdf5+mpi")
    depends_on("h5z-zfp", when="+hdf5")
    depends_on("zfp", when="+hdf5")
    depends_on("hypre~int64@2.20.0:", when="+hypre")
    depends_on("hypre+mpi", when="+hypre+mpi")
    depends_on("hypre+umpire", when="+hypre+umpire")
    depends_on("hypre+sycl", when="+hypre+sycl")
    depends_on("hypre+gpu-aware-mpi", when="+hypre+gpu-aware-mpi")
    depends_on("hypre@2.29.0:", when="@0.9.0:+hypre")
    depends_on("masa", when="+masa")
    depends_on("ascent~mpi", when="+ascent~mpi")
    depends_on("ascent+mpi", when="+ascent+mpi")
    depends_on("netcdf-c", when="+netcdf")
    depends_on("py-matplotlib", when="+masa")
    depends_on("py-pandas", when="+masa")
    depends_on("openfast+cxx", when="+openfast")
    depends_on("openfast+netcdf", when="+openfast+netcdf")
    depends_on("openfast@2.6.0:3.4.1", when="@0.9.0:1 +openfast")
    depends_on("openfast@3.5:", when="@2: +openfast")
    depends_on("helics@:3.3.2", when="+helics")
    depends_on("helics@:3.3.2+mpi", when="+helics+mpi")
    depends_on("fftw", when="@2.1: +waves2amr")
    depends_on("fftw", when="@3.3.1: +fft")

    for arch in CudaPackage.cuda_arch_values:
        depends_on("hypre+cuda cuda_arch=%s" % arch, when="+cuda+hypre cuda_arch=%s" % arch)
    for arch in ROCmPackage.amdgpu_targets:
        depends_on(
            "hypre+rocm amdgpu_target=%s" % arch, when="+rocm+hypre amdgpu_target=%s" % arch
        )
    for arch in CudaPackage.cuda_arch_values:
        depends_on("ascent+cuda cuda_arch=%s" % arch, when="+ascent+cuda cuda_arch=%s" % arch)

    conflicts("+openmp", when="+cuda")
    conflicts("+shared", when="+cuda")
    conflicts("@:2.0", when="+waves2amr")

    def setup_build_environment(self, env):
        # Avoid compile errors with Intel interprocedural optimization
        if self.spec.satisfies("%intel"):
            env.append_flags("CXXFLAGS", "-no-ipo")

    def cmake_args(self):
        define = self.define
        spec = self.spec

        vs = [
            "mpi",
            "cuda",
            "openmp",
            "netcdf",
            "hypre",
            "masa",
            "ascent",
            "openfast",
            "rocm",
            "tests",
            "tiny_profile",
            "fft",
            "helics",
            "umpire",
            "sycl",
        ]
        args = [self.define_from_variant("AMR_WIND_ENABLE_%s" % v.upper(), v) for v in vs]

        args += [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]

        if spec.satisfies("+mpi"):
            args.append(define("MPI_HOME", spec["mpi"].prefix))

        if spec.satisfies("+hdf5"):
            args.append(define("AMR_WIND_ENABLE_HDF5", True))
            args.append(define("AMR_WIND_ENABLE_HDF5_ZFP", True))
            # Help AMReX understand if HDF5 is parallel or not.
            # Building HDF5 with CMake as Spack does, causes this inspection to break.
            args.append(define("HDF5_IS_PARALLEL", spec.satisfies("+mpi")))

        if spec.satisfies("+cuda"):
            args.append(define("CMAKE_CUDA_ARCHITECTURES", spec.variants["cuda_arch"].value))

        if spec.satisfies("+rocm"):
            args.append(define("CMAKE_CXX_COMPILER", spec["hip"].hipcc))
            targets = spec.variants["amdgpu_target"].value
            args.append("-DAMReX_AMD_ARCH=" + ";".join(str(x) for x in targets))

        if spec.satisfies("+umpire"):
            args.append(define("UMPIRE_DIR", spec["umpire"].prefix))

        if spec.satisfies("+helics"):
            args.append(define("HELICS_DIR", spec["helics"].prefix))

        if spec.satisfies("+waves2amr"):
            args.append(self.define_from_variant("AMR_WIND_ENABLE_W2A", "waves2amr"))
            args.append(define("FFTW_DIR", spec["fftw"].prefix))

        if spec.satisfies("+fft"):
            args.append(define("FFTW_DIR", spec["fftw"].prefix))

        if spec.satisfies("+sycl"):
            requires(
                "%dpcpp",
                "%oneapi",
                policy="one_of",
                msg=(
                    "AMReX's SYCL GPU Backend requires DPC++ (dpcpp) "
                    "or the oneAPI CXX (icpx) compiler."
                ),
            )

        return args
