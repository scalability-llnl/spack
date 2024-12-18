# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nvshmem(MakefilePackage, CudaPackage):
    """NVSHMEM is a parallel programming interface based on OpenSHMEM that
    provides efficient and scalable communication for NVIDIA GPU
    clusters. NVSHMEM creates a global address space for data that spans
    the memory of multiple GPUs and can be accessed with fine-grained
    GPU-initiated operations, CPU-initiated operations, and operations on
    CUDA streams."""

    homepage = "https://developer.nvidia.com/nvshmem"

    maintainers("bvanessen")

    license("BSD-3-Clause-Open-MPI")

    version("2.7.0-6", sha256="23ed9b0187104dc87d5d2bc1394b6f5ff29e8c19138dc019d940b109ede699df")
    version("2.6.0-1", sha256="fc0e8de61b034f3a079dc231b1d0955e665a9f57b5013ee98b6743647bd60417")
    version("2.5.0-19", sha256="dd800b40f1d296e1d3ed2a9885adcfe745c3e57582bc809860e87bd32abcdc60")
    version("2.4.1-3", sha256="8b6c0eab321b6352911e470f9e81a777a49e58148ec3728453b9522446dba178")
    version("2.2.1-0", sha256="c8efc6cd560e0ed66d5fe4c5837c650247bec7b0dc65b5089deb8ab49658e1c3")
    version("2.1.2-0", sha256="367211808df99b4575fb901977d9f4347065c61a26642d65887f24d60342a4ec")
    version("2.0.3-0", sha256="20da93e8508511e21aaab1863cb4c372a3bec02307b932144a7d757ea5a1bad2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("cuda", default=True, description="Build with CUDA")
    variant("ucx", default=True, description="Build with UCX support")
    variant("nccl", default=True, description="Build with NCCL support")
    variant("gdrcopy", default=True, description="Build with gdrcopy support")
    variant("mpi", default=True, description="Build with MPI support")
    variant("shmem", default=False, description="Build with shmem support")
    variant(
        "gpu_initiated_support",
        default=False,
        when="@2.6:",
        description="Build with support for GPU initiated communication",
    )
    conflicts("~cuda")

    def url_for_version(self, version):
        ver_str = "{0}".format(version)
        directory = ver_str.split("-")[0]
        url_fmt = "https://developer.download.nvidia.com/compute/redist/nvshmem/{0}/source/nvshmem_src_{1}.txz"
        return url_fmt.format(directory, version)

    depends_on("mpi", when="+mpi")
    depends_on("ucx", when="+ucx")
    depends_on("gdrcopy", when="+gdrcopy")
    depends_on("nccl", when="+nccl")

    def setup_build_environment(self, env):
        env.set("CUDA_HOME", self.spec["cuda"].prefix)
        env.set("NVSHMEM_PREFIX", self.prefix)

        if "+ucx" in self.spec:
            env.set("NVSHMEM_UCX_SUPPORT", "1")
            env.set("UCX_HOME", self.spec["ucx"].prefix)

        if "+gdrcopy" in self.spec:
            env.set("NVSHMEM_USE_GDRCOPY", "1")
            env.set("GDRCOPY_HOME", self.spec["gdrcopy"].prefix)

        if "+nccl" in self.spec:
            env.set("NVSHMEM_USE_NCCL", "1")
            env.set("NCCL_HOME", self.spec["nccl"].prefix)

        if "+mpi" in self.spec:
            env.set("NVSHMEM_MPI_SUPPORT", "1")
            env.set("MPI_HOME", self.spec["mpi"].prefix)

            if self.spec.satisfies("^spectrum-mpi") or self.spec.satisfies("^openmpi"):
                env.set("NVSHMEM_MPI_IS_OMPI", "1")
            else:
                env.set("NVSHMEM_MPI_IS_OMPI", "0")

        if "+shmem" in self.spec:
            env.set("NVSHMEM_SHMEM_SUPPORT", "1")
            env.set("SHMEM_HOME", self.spec["mpi"].prefix)

        if "+gpu_initiated_support" in self.spec:
            env.set("NVSHMEM_GPUINITIATED_SUPPORT", "1")
