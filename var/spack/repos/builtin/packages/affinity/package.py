# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Affinity(CMakePackage, CudaPackage):
    """Simple applications for determining Linux thread and gpu affinity."""

    homepage = "https://github.com/bcumming/affinity"
    git = "https://github.com/bcumming/affinity.git"
    version("master", branch="master")

    maintainers("bcumming", "nhanford")

    license("BSD-3-Clause", checked_by="nhanford")

    variant("mpi", default=False, description="Build MPI support")
    variant("rocm", default=False, description="Build ROCm Support")

    depends_on("mpi", when="+mpi")
    depends_on("hip", when="+rocm")
    depends_on("mpi", when="+mpi")
    depends_on("mpi", when="+cuda")
