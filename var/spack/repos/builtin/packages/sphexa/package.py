# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sphexa(CMakePackage, CudaPackage, ROCmPackage):
    """SPH and N-body simulation framework"""

    homepage = "https://github.com/sphexa-org/sphexa"
    url = "https://github.com/sphexa-org/sphexa/archive/v0.0.0.tar.gz"
    git = "https://github.com/sphexa-org/sphexa.git"
    maintainers = ["sekelle"]

    license("MIT")

    version("0.93.1", sha256="95a93d0063ac8857b9be12c1aca24f5b2eef9dd4ffe8cf3f6b552a4dd54b940f")
    version("develop", branch="develop")

    variant("hdf5", default=True, description="Enable support for HDF5 I/O")
    variant("gpu_aware_mpi", default=True, description="GPU aware MPI")

    depends_on("cmake@3.22:", type="build")

    depends_on("mpi")
    depends_on("cuda@11.2:", when="+cuda")
    depends_on("hip", when="+rocm")
    depends_on("rocthrust", when="+rocm")
    depends_on("hipcub", when="+rocm")
    depends_on("hdf5 +mpi", when="+hdf5")

    # Build MPI with GPU support when GPU aware MPI is requested.
    # For cray-mpich, the user is responsible to configure it for GPU aware MPI.
    with when("+gpu_aware_mpi"):
        depends_on("openmpi +cuda", when="+cuda ^[virtuals=mpi] openmpi")
        depends_on("mpich +cuda", when="+cuda ^[virtuals=mpi] mpich")
        depends_on("mvapich +cuda", when="+cuda ^[virtuals=mpi] mvapich")
        depends_on("mvapich2 +cuda", when="+cuda ^[virtuals=mpi] mvapich2")

        depends_on("mpich +rocm", when="+rocm ^[virtuals=mpi] mpich")

    conflicts("%gcc@:10")
    conflicts("cuda_arch=none", when="+cuda", msg="CUDA architecture is required")
    conflicts("amdgpu_target=none", when="+rocm", msg="HIP architecture is required")
    conflicts("+cuda", when="+rocm", msg="CUDA and HIP cannot both be enabled")

    def cmake_args(self):
        spec = self.spec

        args = [
            self.define_from_variant("SPH_EXA_WITH_H5PART", "hdf5"),
            self.define_from_variant("SPH_EXA_WITH_CUDA", "cuda"),
            self.define_from_variant("RYOANJI_WITH_CUDA", "cuda"),
            self.define_from_variant("CSTONE_WITH_CUDA", "cuda"),
            self.define_from_variant("SPH_EXA_WITH_HIP", "rocm"),
            self.define_from_variant("RYOANJI_WITH_HIP", "rocm"),
            self.define_from_variant("CSTONE_WITH_HIP", "rocm"),
        ]

        if spec.satisfies("+rocm") or spec.satisfies("+cuda"):
            args.append(self.define_from_variant("CSTONE_WITH_GPU_AWARE_MPI", "gpu_aware_mpi"))

        if spec.satisfies("+rocm"):
            archs = spec.variants["amdgpu_target"].value
            arch_str = ";".join(archs)
            args.append(self.define("CMAKE_HIP_ARCHITECTURES", arch_str))

        if spec.satisfies("+cuda"):
            args.append(self.define("CMAKE_CUDA_FLAGS", "-ccbin={0}".format(spec["mpi"].mpicxx)))
            archs = spec.variants["cuda_arch"].value
            arch_str = ";".join(archs)
            args.append(self.define("CMAKE_CUDA_ARCHITECTURES", arch_str))

        return args
