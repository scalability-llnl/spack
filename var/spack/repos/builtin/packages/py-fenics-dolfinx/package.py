# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFenicsDolfinx(PythonPackage):
    """Python interface to the next generation FEniCS problem solving
    environment"""

    homepage = "https://github.com/FEniCS/dolfinx"
    url = "https://github.com/FEniCS/dolfinx/archive/v0.1.0.tar.gz"
    git = "https://github.com/FEniCS/dolfinx.git"
    maintainers("chrisrichardson", "garth-wells", "nate-sime", "jhale")

    license("LGPL-3.0-only")

    version("main", branch="main")
    version("0.9.0", sha256="b266c74360c2590c5745d74768c04568c965b44739becca4cd6b5aa58cdbbbd1")
    version("0.8.0", sha256="acf3104d9ecc0380677a6faf69eabfafc58d0cce43f7777e1307b95701c7cad9")
    version("0.7.2", sha256="7d9ce1338ce66580593b376327f23ac464a4ce89ef63c105efc1a38e5eae5c0b")
    version("0.6.0", sha256="eb8ac2bb2f032b0d393977993e1ab6b4101a84d54023a67206e3eac1a8d79b80")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.21:", when="@0.9:", type="build")
    depends_on("cmake@3.19:", when="@:0.8", type="build")
    depends_on("hdf5", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("python@3.9:", when="@0.8:", type=("build", "run"))
    depends_on("python@3.8:", when="@0.7", type=("build", "run"))
    depends_on("python@3.8:3.10", when="@0.6.0", type=("build", "run"))

    depends_on("fenics-dolfinx@main", when="@main")
    depends_on("fenics-dolfinx@0.9.0", when="@0.9.0")
    depends_on("fenics-dolfinx@0.8.0", when="@0.8.0")
    depends_on("fenics-dolfinx@0.7.2", when="@0.7.2")
    depends_on("fenics-dolfinx@0.6.0", when="@0.6.0")

    depends_on("py-fenics-basix@main", type=("build", "run"), when="@main")
    depends_on("py-fenics-basix@0.9", type=("build", "link"), when="@0.9")
    depends_on("py-fenics-basix@0.8", type=("build", "link"), when="@0.8")

    depends_on("fenics-basix@main", type=("build", "link"), when="@main")
    depends_on("fenics-basix@0.9", type=("build", "link"), when="@0.9")
    depends_on("fenics-basix@0.8", type=("build", "link"), when="@0.8")
    depends_on("fenics-basix@0.7", type=("build", "link"), when="@0.7")
    depends_on("fenics-basix@0.6", type=("build", "link"), when="@0.6")

    depends_on("py-fenics-ffcx@main", type=("build", "run"), when="@main")
    depends_on("py-fenics-ffcx@0.9", type=("build", "run"), when="@0.9")
    depends_on("py-fenics-ffcx@0.8", type=("build", "run"), when="@0.8")
    depends_on("py-fenics-ffcx@0.7", type=("build", "run"), when="@0.7")
    depends_on("py-fenics-ffcx@0.6", type=("build", "run"), when="@0.6")

    depends_on("py-fenics-ufl@main", type=("build", "run"), when="@main")
    depends_on("py-fenics-ufl@2024.2", type=("build", "run"), when="@0.9")
    depends_on("py-fenics-ufl@2024.1", type=("build", "run"), when="@0.8")
    depends_on("py-fenics-ufl@2023.2", type=("build", "run"), when="@0.7")
    depends_on("py-fenics-ufl@2023.1", type=("build", "run"), when="@0.6")

    depends_on("py-numpy@1.21:", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-petsc4py", type=("build", "run"))
    depends_on("py-cffi@:1.16", type=("build", "run"))

    depends_on("py-nanobind@2:", when="@0.9:", type="build")
    depends_on("py-nanobind@1.8:1.9", when="@0.8", type="build")
    depends_on("py-scikit-build-core+pyproject@0.10:", when="@0.10:", type="build")
    depends_on("py-scikit-build-core+pyproject@0.5:", when="@0.8:0.9", type="build")

    depends_on("py-pybind11@2.7.0:", when="@:0.7", type=("build", "run"))
    depends_on("py-setuptools@42:", when="@:0.7", type="build")

    build_directory = "python"
