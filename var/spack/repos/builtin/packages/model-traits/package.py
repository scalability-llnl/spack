# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ModelTraits(CMakePackage):
    """Model setup and querying in C++."""

    homepage = "https://github.com/jacobmerson/model-traits/"
    url = "https://github.com/jacobmerson/model-traits/archive/refs/tags/v0.1.0.tar.gz"
    git = "https://github.com/jacobmerson/model-traits.git"

    maintainers("jacobmerson")

    license("BSD-3-Clause")

    version("0.2.1", sha256="241ce5738ea72182a570ae474aedff58751e6ea448bd174005c5520c8b5a95d1")
    version("0.2.0", sha256="f367cf96a4c1c19f6e2dcf92af6bf69b39217a01fe6f1942d4825258eca8d4bc")
    version("0.1.1", sha256="75af53b4f576071570fdcfa7a4ce150b935cf21368da41d16d8377c5b3b93713")
    version("0.1.0", sha256="ff7c1c5be6977f1d3dc592e8b6c5bff5a8b7ea80d0f059d85c02300bdb8faf2c")
    version("main", branch="main")

    depends_on("cxx", type="build")  # generated

    variant("yaml", default=True, description="build the Yaml IO backend")
    variant("simmetrix", default=False, description="build the Simmetrix backend")
    variant("pumi", default=False, description="build the pumi examples")

    depends_on("yaml-cpp@0.6.3:", when="+yaml")
    depends_on("catch2@3.0.0-preview3:", type="test")
    depends_on("pumi", when="+pumi")
    depends_on("simmetrix-simmodsuite", when="+simmetrix")
    depends_on("fmt@7.1.3")
    depends_on("cmake@3.14.0:", type="build")
    depends_on("mpi", when="+simmetrix")
    depends_on("mpi", when="+pumi")

    def cmake_args(self):
        args = [self.define("BUILD_TESTING", self.run_tests)]
        if self.spec.satisfies("@:0.1.1"):
            args.extend(
                [
                    self.define("BUILD_EXTERNAL", False),
                    self.define_from_variant("ENABLE_SCOREC", "pumi"),
                    self.define_from_variant("ENABLE_SIMMETRIX", "simmetrix"),
                    self.define_from_variant("ENABLE_YAML", "yaml"),
                ]
            )
        else:
            args.extend(
                [
                    self.define("MODEL_TRAITS_BUILD_EXTERNAL", False),
                    self.define_from_variant("MODEL_TRAITS_ENABLE_SCOREC", "pumi"),
                    self.define_from_variant("MODEL_TRAITS_ENABLE_SIMMETRIX", "simmetrix"),
                    self.define_from_variant("MODEL_TRAITS_ENABLE_YAML", "yaml"),
                ]
            )
        if "+simmetrix" in self.spec:
            args.append(
                self.define("SIM_MPI", self.spec["mpi"].name + self.spec["mpi"].version.string)
            )
            args.append(self.define("SKIP_SIMMETRIX_VERSION_CHECK", True))
        if "+pumi" in self.spec or "+simmetrix" in self.spec:
            args.extend(
                [
                    self.define("CMAKE_CXX_COMPILER", self.spec["mpi"].mpicxx),
                    self.define("CMAKE_C_COMPILER", self.spec["mpi"].mpicc),
                    self.define("CMAKE_Fortran_COMPILER", self.spec["mpi"].mpif77),
                ]
            )
        return args
