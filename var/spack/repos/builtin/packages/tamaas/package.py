# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPipBuilder
from spack.package import *


class Tamaas(SConsPackage):
    """Tamaas is a C++ library with a Python interface that efficiently solves
    contact mechanics problems with periodic rough surfaces, plasticity,
    adhesion and friction."""

    homepage = "https://gitlab.com/tamaas/tamaas"
    url = "https://gitlab.com/tamaas/tamaas/-/archive/v2.4.0/tamaas-v2.4.0.tar.gz"
    git = "https://gitlab.com/tamaas/tamaas.git"
    maintainers("prs513rosewood")

    version("master", branch="master")
    version("2.8.0", sha256="8ec49bf484a622c0554452416d1804eefbd545da79ced352f2ea63bbd17c83f0")
    version("2.7.1", sha256="d7de6db3f5532bb9c8ab7e8cca1cdb5c133050dd5720249dde07027b0d41641f")
    version("2.7.0", sha256="bc5717c1ead621cb9c18a073fdafbe8778fd160ad23d80c98283445d79066579")
    version("2.6.0", sha256="4aafa0f727f43afc6ae45705ae80cf113a6a95e728bdf536c22b3b39be87f153")
    version(
        "2.5.0.post1", sha256="28e52dc5b8a5f77588c73a6ef396c44c6a8e9d77e3e4929a4ab07232dc9bc565"
    )
    version("2.4.0", sha256="38edba588ff3a6643523c28fb391e001dbafa9d0e58053b9e080eda70f8c71c9")
    version("2.3.1", sha256="7d63e374cbc7b5b93578ece7be5c084d1c2f0dbe1d57c4f0c8abd5ff5fff9ab0")
    version("2.3.0", sha256="0529e015c6cb5bbabaea5dce6efc5ec0f2aa76c00541f0d90ad0e2e3060a4520")

    depends_on("cxx", type="build")  # generated

    variant("python", default=True, description="Provide Python bindings for Tamaas")
    variant(
        "solvers",
        default=True,
        when="+python",
        description="Enables extra Scipy-based nonlinear solvers",
    )
    variant("petsc", default=False, when="@2.8.0:", description="Additional PETSc solvers")

    # Python 3.6 causes unicode issues with scons
    depends_on("python@3.7:", type="build", when="~python")
    depends_on("scons@3:", type="build")

    depends_on("thrust", type="build")
    depends_on("boost", type="build")
    depends_on("fftw-api@3:")

    # compilers that don't use C++14 by default cause configure issues
    conflicts("%gcc@:5")
    conflicts("%clang@:5")
    conflicts("%intel")

    # MPI type-traits issues (constexpr vs static const) in recent gcc
    # fixed for tamaas versions > 2.6.0
    patch("recent_compilers.patch", when="@:2.6.0%gcc@11:")

    with when("+python"):
        extends("python")
        depends_on("python@3.7:", type=("build", "run"))
        depends_on("py-numpy", type=("build", "run"))
        depends_on("py-scipy", when="+solvers", type="run")
        depends_on("py-pybind11", type="build")
        depends_on("py-wheel", type="build")
        depends_on("py-pip", type="build")

    depends_on("petsc", type="build", when="+petsc")

    def build_args(self, spec, prefix):
        args = [
            "build_type=release",
            "use_mpi={}".format(spec["fftw-api"].satisfies("+mpi")),
            "backend={}".format("omp" if spec["fftw-api"].satisfies("+openmp") else "cpp"),
            "fftw_threads={}".format("omp" if spec["fftw-api"].satisfies("+openmp") else "none"),
            "build_python={}".format(spec.satisfies("+python")),
            "verbose=True",
            "strip_info=True",
            "real_type=double",
            "integer_type=int",
            "build_tests=False",
            "doc_builders=none",
            "prefix={}".format(prefix),
            "BOOST_ROOT={}".format(spec["boost"].prefix),
            "THRUST_ROOT={}".format(spec["thrust"].prefix),
            "FFTW_ROOT={}".format(spec["fftw-api"].prefix),
        ]

        if spec.satisfies("+python"):
            args += ["PYBIND11_ROOT={}".format(spec["py-pybind11"].prefix)]

        if spec.satisfies("+petsc"):
            args += ["PETSC_ROOT={}".format(spec["petsc"].prefix), "use_petsc=True"]

        return args

    def install(self, spec, prefix):
        """Install the package."""
        args = self.install_args(spec, prefix)

        scons("install-lib", *args)

        if spec.satisfies("+python"):
            pip(*PythonPipBuilder.std_args(self), f"--prefix={prefix}", "build-release/python")
