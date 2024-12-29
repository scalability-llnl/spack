# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsBasix(PythonPackage):
    """Python interface to Basix, a finite element definition and tabulation runtime library"""

    homepage = "https://github.com/FEniCS/basix"
    url = "https://github.com/FEniCS/basix/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/basix.git"
    maintainers("chrisrichardson", "mscroggs", "garth-wells", "jhale")

    license("MIT")

    version("main", branch="main")
    version("0.9.0", sha256="60e96b2393084729b261cb10370f0e44d12735ab3dbd1f15890dec23b9e85329")
    version("0.8.0", sha256="b299af82daf8fa3e4845e17f202491fe71b313bf6ab64c767a5287190b3dd7fe")
    version("0.7.0", sha256="9bee81b396ee452eec8d9735f278cb44cb6994c6bc30aec8ed9bb4b12d83fa7f")
    version("0.6.0", sha256="687ae53153c98facac4080dcdc7081701db1dcea8c5e7ae3feb72aec17f83304")

    depends_on("cxx", type="build")  # generated

    depends_on("fenics-basix@main", type=("build", "run"), when="@main")
    depends_on("fenics-basix@0.9.0", type=("build", "run"), when="@0.9.0")
    depends_on("fenics-basix@0.8.0", type=("build", "run"), when="@0.8.0")
    depends_on("fenics-basix@0.7.0", type=("build", "run"), when="@0.7.0")
    depends_on("fenics-basix@0.6.0", type=("build", "run"), when="@0.6.0")

    # See python/CMakeLists.txt
    depends_on("cmake@3.21:", when="@0.9:", type="build")
    depends_on("cmake@3.19:", when="@0.8", type="build")
    depends_on("cmake@3.16:", when="@:0.7", type="build")

    # See python/pyproject.toml
    depends_on("python@3.9:", when="@0.8:", type=("build", "run"))
    depends_on("python@3.8:", when="@:0.7", type=("build", "run"))
    depends_on("py-numpy@1.21:", type=("build", "run"))
    depends_on("py-pybind11@2.9.1:", when="@:0.7", type="build")
    depends_on("py-setuptools@42:", when="@:0.7", type="build")
    depends_on("py-nanobind@2:", when="@0.10:", type="build")
    depends_on("py-nanobind@1.6.0:", when="@0.8:0.9", type="build")
    depends_on("py-scikit-build-core+pyproject@0.10:", when="@0.10:", type="build")
    depends_on("py-scikit-build-core+pyproject@0.5.0:", when="@0.8:0.9", type="build")

    build_directory = "python"
