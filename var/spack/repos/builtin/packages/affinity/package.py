# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Affinity(CMakePackage, CudaPackage, ROCmPackage):
    """Simple applications for determining Linux thread and gpu affinity."""

    homepage = "https://github.com/bcumming/affinity"
    git = "https://github.com/bcumming/affinity.git"
    version("master", branch="master")

    maintainers("bcumming", "nhanford")

    license("BSD-3-Clause", checked_by="nhanford")

    variant("cuda", default=False, description="Build CUDA support.")
    variant("rocm", default=False, description="Build ROCm support.")
    variant("mpi", default=True, description="Build MPI support.")

    depends_on("cuda", when="+cuda")
    depends_on("hip", when="+rocm")
    depends_on("mpi", when="+cuda")
    depends_on("mpi", when="+rocm")
    depends_on("mpi", when="+mpi")
