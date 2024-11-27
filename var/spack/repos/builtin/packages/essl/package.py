# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Essl(BundlePackage):
    """IBM's Engineering and Scientific Subroutine Library (ESSL)."""

    homepage = "https://www.ibm.com/systems/power/software/essl/"

    # https://www.ibm.com/docs/en/essl/6.2?topic=whats-new
    version("6.2.1.1")

    variant("ilp64", default=False, description="64 bit integers")
    variant(
        "threads",
        default="openmp",
        description="Multithreading support",
        values=("openmp", "none"),
        multi=False,
    )
    variant("cuda", default=False, description="CUDA acceleration")
    variant("lapackforessl", default=False, description="Provides lapackforessl lapack library")

    provides("blas")
    provides("lapack", when="+lapackforessl")

    conflicts(
        "+cuda",
        when="+ilp64",
        msg="ESSL+cuda+ilp64 cannot combine CUDA acceleration 64 bit integers",
    )

    conflicts(
        "+cuda",
        when="threads=none",
        msg="ESSL+cuda threads=none cannot combine CUDA acceleration"
        " without multithreading support",
    )

    @property
    def blas_libs(self):
        spec = self.spec
        prefix = self.prefix

        if spec.satisfies("+ilp64"):
            essl_lib = ["libessl6464"]
        else:
            essl_lib = ["libessl"]

        if spec.satisfies("threads=openmp"):
            # ESSL SMP support requires XL or Clang OpenMP library
            if spec.satisfies("%xl") or spec.satisfies("%xl_r") or spec.satisfies("%clang"):
                if spec.satisfies("+ilp64"):
                    essl_lib = ["libesslsmp6464"]
                else:
                    if spec.satisfies("+cuda"):
                        essl_lib = ["libesslsmpcuda"]
                    else:
                        essl_lib = ["libesslsmp"]

        essl_root = prefix.lib64
        essl_libs = find_libraries(essl_lib, root=essl_root, shared=True)

        return essl_libs

    @property
    def lapack_libs(self):
        essl_libs = find_libraries(
            ["liblapackforessl", "liblapackforessl_"], root=self.prefix.lib64, shared=True
        )
        return essl_libs
