# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class IqTree(CMakePackage):
    """IQ-TREE Efficient software for phylogenomic inference"""

    homepage = "http://www.iqtree.org"
    git = "https://github.com/iqtree/iqtree2.git"
    url = "https://github.com/Cibiv/IQ-TREE/archive/v1.6.12.tar.gz"

    license("GPL-2.0-or-later")

    version(
        "2.3.2", tag="v2.3.1", commit="60f1aa68646ab84cc96b55a7548707adde15f47a", submodules=True
    )
    version(
        "2.3.1", tag="v2.3.1", commit="2914a2f7aac0a1a3c4fadde42c83e5dee315186d", submodules=True
    )
    version(
        "2.2.2.7",
        tag="v2.2.2.7",
        commit="bd3468c7af6572ea29002dfdba377804f8f56c26",
        submodules=True,
    )
    version(
        "2.1.3", tag="v2.1.3", commit="3d31be9e56b05ffbc5f8488fc8285597b433c99f", submodules=True
    )
    version(
        "2.0.6", tag="v2.0.6", commit="219e88407ac915a209a29808a81084bf0d5f1a84", submodules=True
    )
    version("1.6.12", sha256="9614092de7a157de82c9cc402b19cc8bfa0cb0ffc93b91817875c2b4bb46a284")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("openmp", default=True, description="Enable OpenMP support.")
    variant("mpi", default=False, description="Enable MPI support.")
    variant("lsd2", default=True, description="Activate Least Squares Dating.")

    maintainers("ilbiondo")

    # Depends on Eigen3 and zlib

    depends_on("boost+container+math+exception")
    depends_on("eigen")
    depends_on("zlib-api")
    depends_on("mpi", when="+mpi")

    def cmake_args(self):
        spec = self.spec
        args = []
        iqflags = []

        if spec.satisfies("+lsd2"):
            args.append("-DUSE_LSD2=ON")

        if spec.satisfies("+openmp"):
            iqflags.append("omp")

        if spec.satisfies("+mpi"):
            iqflags.append("mpi")

        if not iqflags:
            iqflags.append("single")

        args.append("-DIQTREE_FLAGS=" + ",".join(iqflags))

        return args
