# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class FrontistrBase(CMakePackage):
    """Base class for building Frontistr, shared with the Fujitsu optimized version
    of the package in the 'fujitsu-frontistr' package."""

    variant(
        "build_type",
        default="RELEASE",
        description="CMake build type",
        values=("DEBUG", "RELEASE"),
    )

    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("scalapack")
    depends_on("revocap-refiner")
    # depends_on('revocap-coupler')
    depends_on("metis")
    depends_on("mumps")
    depends_on("trilinos@:13.0.1")

    def cmake_args(self):
        define = self.define
        cmake_args = [
            define("WITH_ML", True),
            define("REFINER_INCLUDE_PATH", self.spec["revocap-refiner"].prefix.include),
            define(
                "REFINER_LIBRARIES",
                join_path(self.spec["revocap-refiner"].prefix.lib, "libRcapRefiner.a"),
            ),
        ]
        return cmake_args


class Frontistr(FrontistrBase):
    """Open-Source Large-Scale Parallel FEM Program for
    Nonlinear Structural Analysis"""

    homepage = "https://www.frontistr.com/"
    git = "https://gitlab.com/FrontISTR-Commons/FrontISTR.git"

    maintainers("hiroshi.okuda", "kgoto", "morita", "inagaki", "michioga")

    license("MIT")

    version("5.3", tag="v5.3", commit="5db1d80452b951905658da828285c2fd0537603c")
    version("5.2", tag="v5.2", commit="c66bdc397de319ca59a0565b3f3b1a3b33f0c50c")
    version("5.1.1", tag="v5.1.1", commit="57e9bbd529a6062f55e03c884b59af22f920eef1")
    version("5.1", tag="v5.1", commit="f3fe347a8fd83cd45983476521d43061c8528da0")
    version("5.0", tag="v5.0", commit="39b83f057a2639af4b5083fb911e0726f0972b75")
    version("master", tag="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated
