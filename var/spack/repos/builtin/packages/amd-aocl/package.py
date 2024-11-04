# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AmdAocl(BundlePackage):
    """AMD Optimizing CPU Libraries (AOCL) - AOCL is a set of numerical
    libraries tuned specifically for AMD EPYC processor family. They have a
    simple interface to take advantage of the latest hardware innovations.
    The tuned implementations of industry standard  math libraries enable
    fast development of scientific and high performance computing projects

    LICENSING INFORMATION: By downloading, installing and using this software,
    you agree to the terms and conditions of the AMD AOCL license agreement.
    You may obtain a copy of this license agreement from
    https://www.amd.com/en/developer/aocl/aocl-eula.html
    https://www.amd.com/en/developer/aocl/eula/aocl-4-1-eula.html
    """

    homepage = "https://developer.amd.com/amd-aocl/"

    maintainers("amd-toolchain-support")

    version("5.0", preferred=True)
    version("4.2")
    version("4.1")
    version("4.0")
    version("3.2")
    version("3.1")
    version("3.0")
    version("2.2")

    variant("openmp", default=False, description="Enable OpenMP support.")

    with when("+openmp"):
        depends_on("amdblis threads=openmp")
        depends_on("amdfftw +openmp")
        depends_on("amdlibflame threads=openmp")
        depends_on("aocl-sparse +openmp")
        depends_on("aocl-da +openmp")
        depends_on("aocl-compression +openmp")

    with when("~openmp"):
        depends_on("amdblis threads=none")
        depends_on("amdfftw ~openmp")
        depends_on("amdlibflame threads=none")
        depends_on("aocl-sparse ~openmp")
        depends_on("aocl-da ~openmp")
        depends_on("aocl-compression ~openmp")

    for vers in ["2.2", "3.0", "3.1", "3.2", "4.0", "4.1", "4.2", "5.0"]:
        with when(f"@={vers}"):
            depends_on(f"amdblis@={vers}")
            depends_on(f"amdfftw@={vers}")
            depends_on(f"amdlibflame@={vers}")
            depends_on("amdlibflame ^[virtuals=blas] amdblis")
            depends_on(f"amdlibm@={vers}")
            depends_on(f"amdscalapack@={vers}")
            depends_on("amdscalapack ^[virtuals=blas] amdblis")
            depends_on("amdscalapack ^[virtuals=lapack] amdlibflame")
            depends_on(f"aocl-sparse@={vers}")
            if Version(vers) >= Version("4.2"):
                depends_on(f"aocl-compression@={vers}")
                depends_on(f"aocl-crypto@={vers}")
                depends_on(f"aocl-libmem@={vers}")
            if Version(vers) >= Version("5.0"):
                depends_on(f"aocl-da@={vers}")
