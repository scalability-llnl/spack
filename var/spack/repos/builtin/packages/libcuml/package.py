# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libcuml(CMakePackage):
    """cuML is a suite of libraries that implement machine
    learning algorithms and mathematical primitives functions
    that share compatible APIs with other RAPIDS projects."""

    homepage = "https://rapids.ai"
    url = "https://github.com/rapidsai/cuml/archive/v0.15.0.tar.gz"

    version("0.15.0", sha256="5c9c656ae4eaa94a426e07d7385fd5ea0e5dc7abff806af2941aee10d4ca99c7")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.14:", type="build")
    depends_on("zlib-api")
    depends_on("libcudf@0.8:")
    depends_on("cuda@9.2:")
    depends_on("blas")
    depends_on("nccl@2.4:")
    depends_on("treelite")
    depends_on("googletest")
    depends_on("libcumlprims")
    depends_on("mpi")
    depends_on("ucx")

    root_cmakelists_dir = "cpp"

    def cmake_args(self):
        args = []

        args.append("-DNCCL_PATH={0}".format(self.spec["nccl"].prefix))
        args.append("-DBUILD_CUML_C_LIBRARY=ON")
        args.append("-DWITH_UCX=ON")
        args.append("-DNVTX=OFF")
        args.append("-DBUILD_STATIC_FAISS=ON")
        args.append("-DSINGLEGPU=OFF")
        args.append("-DENABLE_CUMLPRIMS_MG=ON")
        args.append("-DBUILD_CUML_MPI_COMMS=ON")

        return args
