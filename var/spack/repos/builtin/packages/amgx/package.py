# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Amgx(CMakePackage, CudaPackage):
    """AmgX provides a simple path to accelerated core solver technology on
    NVIDIA GPUs. AmgX provides up to 10x acceleration to the computationally
    intense linear solver portion of simulations, and is especially well
    suited for implicit unstructured methods. It is a high performance,
    state-of-the-art library and includes a flexible solver composition
    system that allows a user to easily construct complex nested solvers and
    preconditioners."""

    homepage = "https://developer.nvidia.com/amgx"
    url = "https://github.com/nvidia/amgx/archive/v2.1.0.tar.gz"

    maintainers("js947")

    license("BSD-3-Clause")

    version("2.3.0", sha256="419b3cd5bd3eb3469cbef79d64a8d19d5db88dd5cce809e49cac6fc4fc2edff1")
    version("2.2.0", sha256="dac78516bb528135cad903399fe0093aa0904e304565ef2d3da4fae05eda7928")
    version("2.1.0", sha256="6245112b768a1dc3486b2b3c049342e232eb6281a6021fffa8b20c11631f63cc")
    version("2.0.1", sha256="6f9991f1836fbf4ba2114ce9f49febd0edc069a24f533bd94fd9aa9be72435a7")
    version("2.0.0", sha256="8ec7ea8412be3de216fcf7243c4e2a8bcf76878e6865468e4238630a082a431b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("cuda", default=True, description="Build with CUDA")
    variant("mpi", default=True, description="Enable MPI support")
    variant("mkl", default=False, description="Enable MKL support")
    variant("magma", default=False, description="Enable Magma support")

    depends_on("mpi", when="+mpi")
    depends_on("mkl", when="+mkl")
    depends_on("magma", when="+magma")

    def cmake_args(self):
        args = []
        args.append("-DCMAKE_NO_MPI={0}".format("1" if "+mpi" not in self.spec else "0"))

        if self.spec.satisfies("+cuda"):
            args.append("-DWITH_CUDA=ON")
            cuda_arch = self.spec.variants["cuda_arch"].value
            if cuda_arch != "none":
                args.append("-DCUDA_ARCH={0}".format(cuda_arch[0]))
        else:
            args.append("-DWITH_CUDA=OFF")

        if self.spec.satisfies("+mkl"):
            args.append("-DMKL_ROOT_DIR={0}".format(self.spec["mkl"].prefix))

        if self.spec.satisfies("+magma"):
            args.append("-DMAGMA_ROOT_DIR={0}".format(self.spec["magma"].prefix))

        return args
