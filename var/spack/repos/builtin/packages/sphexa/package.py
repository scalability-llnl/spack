# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sphexa(CMakePackage, CudaPackage, ROCmPackage):
    """SPH and N-body simulation framework"""

    homepage = "https://github.com/sphexa-org/sphexa"
    url = "https://github.com/sphexa-org/sphexa/archive/v0.0.tar.gz"
    git = "git@github.com:sphexa-org/sphexa.git"
    maintainers = ["sekelle"]

    license("MIT")

    version("0.93.1", sha256="95a93d0063ac8857b9be12c1aca24f5b2eef9dd4ffe8cf3f6b552a4dd54b940f")
    version("0.93", sha256="03bc24d5fc2ca8f42f18c02af39dd10a36fb4118f4d5cb5d6c651f9b7a2bece6")
    version("0.92", sha256="cb38a6e11c72ec0c40e8a28a9b0725c8b596d274d3164ab8dffa73501db0e3aa")
    version("0.91", sha256="2811ac0d3a70847219c43b2afce2505cee88575a4da74915937b1b3f0ee43df3")
    version("0.82", sha256="23ef1057996e1b5280b1dca88730efa398a830a42715421688bbdc81d8d090fe")
    version("0.81", sha256="a0f90207d78937db54e23b002e911be7138abc0f080fe2a529350582fa4e0e92")
    version("0.8", sha256="cecc0076d7b9a68fa79d3985b46ed67c49846f26df66eb98db956abcecb46b7c")
    version("develop", branch="develop")

    variant("hdf5", default=True, description="Enable support for HDF5 I/O")
    variant("gpu_aware_mpi", default=True, description="GPU aware MPI")

    depends_on("cmake@3.22:", type="build")

    depends_on("mpi")
    depends_on("cuda@11.2:", when="+cuda")
    depends_on("hip", when="+rocm")
    depends_on("rocthrust", when="+rocm")
    depends_on("rocprim", when="+rocm")
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
    conflicts("+cuda", when="+rocm")
    conflicts("+rocm", when="@:0.93.1")

    def cmake_args(self):
        spec, args = self.spec, []

        args += [self.define("SPH_EXA_WITH_H5PART", spec.variants["hdf5"].value)]

        args.append(self.define_from_variant("SPH_EXA_WITH_CUDA", "cuda"))
        args.append(self.define_from_variant("RYOANJI_WITH_CUDA", "cuda"))
        args.append(self.define_from_variant("CSTONE_WITH_CUDA", "cuda"))
        args.append(self.define_from_variant("SPH_EXA_WITH_HIP", "rocm"))
        args.append(self.define_from_variant("RYOANJI_WITH_HIP", "rocm"))
        args.append(self.define_from_variant("CSTONE_WITH_HIP", "rocm"))

        if spec.satisfies("+rocm") or spec.satisfies("+cuda"):
            args.append(
                self.define("CSTONE_WITH_GPU_AWARE_MPI", spec.variants["gpu_aware_mpi"].value)
            )

        if spec.satisfies("+rocm"):
            archs = spec.variants["amdgpu_target"].value
            if "none" not in archs:
                arch_str = ";".join(archs)
                args.append(self.define("CMAKE_HIP_ARCHITECTURES", arch_str))

        if spec.satisfies("+cuda"):
            args.append(self.define("CMAKE_CUDA_FLAGS", "-ccbin={0}".format(spec["mpi"].mpicxx)))
            archs = spec.variants["cuda_arch"].value
            if "none" not in archs:
                arch_str = ";".join(archs)
                args.append(self.define("CMAKE_CUDA_ARCHITECTURES", arch_str))

        return args
