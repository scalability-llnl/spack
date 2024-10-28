# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FenicsBasix(CMakePackage):
    """Basix is a finite element definition and tabulation runtime library"""

    homepage = "https://github.com/FEniCS/basix"
    url = "https://github.com/FEniCS/basix/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/basix.git"
    maintainers("mscroggs", "chrisrichardson", "garth-wells", "jhale")

    license("MIT")

    version("main", branch="main")
    version("0.9.0", sha256="60e96b2393084729b261cb10370f0e44d12735ab3dbd1f15890dec23b9e85329")
    version("0.8.0", sha256="b299af82daf8fa3e4845e17f202491fe71b313bf6ab64c767a5287190b3dd7fe")
    version("0.7.0", sha256="9bee81b396ee452eec8d9735f278cb44cb6994c6bc30aec8ed9bb4b12d83fa7f")
    version("0.6.0", sha256="687ae53153c98facac4080dcdc7081701db1dcea8c5e7ae3feb72aec17f83304")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.21:", when="@0.9:", type="build")
    depends_on("cmake@3.19:", when="@:0.8", type="build")
    depends_on("blas")
    depends_on("lapack")

    conflicts("%gcc@:9.10", msg="fenics-basix requires GCC-10 or newer for C++20 support")
    conflicts("%clang@:9.10", msg="fenics-basix requires Clang-10 or newer for C++20 support")

    root_cmakelists_dir = "cpp"
