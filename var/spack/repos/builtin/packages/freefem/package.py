# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Freefem(AutotoolsPackage):
    """FreeFEM is a popular 2D and 3D partial differential equations (PDE) solver.
    It allows you to easily implement your own physics modules using the provided
    FreeFEM language. FreeFEM offers a large list of finite elements, like the
    Lagrange, Taylor-Hood, etc., usable in the continuous and discontinuous
    Galerkin method framework.
    """

    homepage = "https://freefem.org"
    url = "https://github.com/FreeFem/FreeFem-sources/archive/refs/tags/v4.10.tar.gz"

    maintainers("corentin-dev")

    version("4.14", sha256="931cbfe9ef6f6530756c300c5ae47bfdaca21c560a5407cb33325a376a3b6af8")
    version("4.13", sha256="aefd4ff02333209f7433abef2e74acb621b6946063ff27e81cf2da43120b6ae4")
    version("4.12", sha256="291c5f46761711d6303914f9c4f165fd85a7b7b69141f7473e0b6484ce6ab0f5")
    version("4.11", sha256="d0c6921791e5f94646d8dde4d9ed3c11b979e47e7bbb3c0a66467b04dd56983a")
    version("4.10", sha256="957994c8f24cc2a671b8c116ae530796c3a431d4157ee71a3d6aab7122e7570d")
    version("4.9", sha256="299ba2b73dfff578b7890f693c1e835680bf55eba87263cabd60d81909e1e0e4")
    version("4.8", sha256="499b1ca24d45088226a238412ea1492d9cc3eb6088866904145511469780180d")
    version("4.7-1", sha256="60d84424d20b5f6abaee638dc423480fc76f9c389bba1a2f23fd984e39a3fb96")
    version("4.7", sha256="c1797b642e9c3d543eaad4949d26ce1e986f531ee9be14fff606ea525ada9206")
    version("4.6", sha256="6c09af8e189fc02214b0e664b679b49832c134e29cf1ede3cab29cf754f6078f")
    version("4.5", sha256="5b2d4125c312da8fbedd49a72e742f18f35e0ae100c82fb493067dfad5d51432")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=False, description="Activate MPI support")
    variant("petsc", default=False, description="Compile with PETSc/SLEPc")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("m4", type="build")
    # depends_on("patch", type="build")
    # depends_on("unzip", type="build")

    depends_on("netlib-lapack")

    depends_on("mpi", when="+mpi")
    depends_on("slepc", when="+petsc")

    # Patches to help configure find correctly MPI flags
    # when using full path for compilers.
    patch(
        "acmpi.patch",
        when="@4.9",
        sha256="8157d89fc19227a555b54a4f2eb1c44da8aef3192077a6df2e88093b850f4c50",
    )
    patch(
        "acmpi4.8.patch",
        when="@:4.8",
        sha256="be84f7b1b8182ff0151c258056a09bda70d72a611b0a4da1fa1954df2e0fe84e",
    )

    def configure_args(self):
        spec = self.spec
        options = [
            "--disable-mkl",
            "CFLAGS=%s" % " ".join(spec.compiler_flags["cflags"]),
            "FFLAGS=%s" % " ".join(spec.compiler_flags["fflags"]),
            "CXXFLAGS=%s" % " ".join(spec.compiler_flags["cxxflags"]),
        ]

        if spec.satisfies("+petsc"):
            options.append("--with-petsc=%s" % spec["petsc"].prefix.lib.petsc.conf.petscvariables)
            options.append("--with-slepc-ldflags=%s" % spec["slepc"].libs.ld_flags)
            options.append("--with-slepc-include=%s" % spec["slepc"].headers.include_flags)
        else:
            options.append("--without-petsc")
            options.append("--without-slepc")

        return options
