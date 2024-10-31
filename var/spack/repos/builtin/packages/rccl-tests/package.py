# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RcclTests(MakefilePackage):
    """These tests check both the performance and the correctness of RCCL
    operations. They can be compiled against RCCL."""

    homepage = "https://github.com/ROCm/rccl-tests"
    git = "https://github.com/ROCm/rccl-tests.git"
    url = "https://github.com/ROCm/rccl-tests.git"
    tags = ["rocm"]

    maintainers("bvanessen")

    license("BSD-3-Clause")

    version("develop", branch="develop", preferred=True)
    version("master", branch="master")

    depends_on("cxx", type="build")  # generated

    variant("mpi", default=True, description="with MPI support")

    depends_on("hip")
    depends_on("rccl")
    depends_on("mpi", when="+mpi")

    def build_targets(self):
        targets = []
        targets.append("HIP_HOME={0}".format(self.spec["hip"].prefix))
        targets.append("RCCL_HOME={0}".format(self.spec["rccl"].prefix))
        if "+mpi" in self.spec:
            targets.append("MPI_HOME={0}".format(self.spec["mpi"].prefix))
            targets.append("MPI=1")
        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install_tree("./build", prefix.bin)
