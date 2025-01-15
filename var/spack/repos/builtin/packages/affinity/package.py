# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install affinity
#
# You can edit this file again by typing:
#
#     spack edit affinity
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class Affinity(CMakePackage):
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
