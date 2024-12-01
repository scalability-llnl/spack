# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PalisadeDevelopment(CMakePackage):
    """
    PALISADE is a general lattice cryptography library that currently
    includes efficient implementations of the following lattice cryptography
    capabilities:

    Fully Homomorphic Encryption (FHE):
    - Brakerski/Fan-Vercauteren (BFV) scheme for integer arithmetic
    - Brakerski-Gentry-Vaikuntanathan (BGV) scheme for integer arithmetic
    - Cheon-Kim-Kim-Song (CKKS) scheme for real-number arithmetic
    - Ducas-Micciancio (FHEW) and Chillotti-Gama-Georgieva-Izabachene
      (TFHE) schemes for Boolean circuit evaluation

    Multi-Party Extensions of FHE (to support multi-key FHE):
    - Threshold FHE for BGV, BFV, and CKKS schemes
    - Proxy Re-Encryption for BGV, BFV, and CKKS schemes
    """

    homepage = "https://gitlab.com/palisade/palisade-development"
    git = "https://gitlab.com/palisade/palisade-development.git"
    maintainers("wohlbier")

    license("BSD-2-Clause")

    version("feature-fixed-point-encoding", branch="feature-fixed-point-encoding", submodules=True)
    version(
        "fppe-logreg-v1.0",
        tag="fppe-logreg-v1.0",
        commit="5ccb14ffffd65e70db048e143ec2350b97a20d40",
        submodules=True,
    )
    version("master", branch="master", preferred=True, submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared library.")
    variant("static", default=True, description="Build static library.")
    variant("with_be2", default=True, description="Build with backend 2.")
    variant("with_be4", default=True, description="Build with backend 4.")
    variant("with_intel_hexl", default=False, description="Use Intel HEXL.")
    variant("with_ntl", default=False, description="Build NTL.")

    depends_on("autoconf")
    depends_on("hwloc", when="%clang")
    depends_on("ntl", when="+with_ntl")
    depends_on("ntl+shared", when="+with_ntl +shared")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED", "shared"),
            self.define_from_variant("BUILD_STATIC", "static"),
            self.define_from_variant("WITH_BE2", "with_be2"),
            self.define_from_variant("WITH_BE4", "with_be4"),
            self.define_from_variant("WITH_INTEL_HEXL", "with_intel_hexl"),
            self.define_from_variant("WITH_NTL", "with_ntl"),
        ]
        if self.spec.satisfies("%clang"):
            OpenMP_C_FLAGS = "-fopenmp=libomp"
            OpenMP_C_LIB_NAMES = "libomp"
            args += [
                self.define("OpenMP_C", "clang"),
                self.define("OpenMP_C_FLAGS", OpenMP_C_FLAGS),
                self.define("OpenMP_C_LIB_NAMES", OpenMP_C_LIB_NAMES),
                self.define("OpenMP_CXX", "clang++"),
                self.define("OpenMP_CXX_FLAGS", OpenMP_C_FLAGS),
                self.define("OpenMP_CXX_LIB_NAMES", OpenMP_C_LIB_NAMES),
                self.define("OpenMP_libomp_LIBRARY", "libomp"),
                self.define("OpenMP_libgomp_LIBRARY", "libgomp"),
                self.define("OpenMP_libiomp5_LIBRARY", "libiomp5"),
            ]
        return args
