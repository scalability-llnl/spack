# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Qrmumps(CMakePackage):
    """a software package for the solution of sparse, linear systems on
    multicore computers based on the QR factorization of the input matrix."""

    homepage = "https://gitlab.com/qr_mumps/qr_mumps"
    git = "https://gitlab.com/qr_mumps/qr_mumps"
    url = "https://gitlab.com/qr_mumps/qr_mumps/-/archive/3.1/qr_mumps-3.1.tar.gz"
    maintainers("fpruvost")

    version("master", branch="master")
    version("3.1", sha256="6e39dbfa1e6ad3730b006c8953a43cc6da3dfc91f00edeb68a641d364703b773")
    version("3.0.4", sha256="621a294c3bf1e60e4ea6ae29c0586760648947f650e0f86bbabaf82805fc17db")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("amd", default=True, description="Enable AMD ordering")
    variant("metis", default=True, description="Enable Metis ordering")
    variant("scotch", default=True, description="Enable Scotch ordering")
    variant("starpu", default=True, description="Enable StarPU runtime system support")
    variant("cuda", default=False, when="+starpu", description="Enable StarPU+CUDA")
    variant("fxt", default=False, when="+starpu", description="Enable FxT tracing through StarPU")

    depends_on("pkgconfig", type="build")
    depends_on("blas")
    depends_on("lapack")
    depends_on("suite-sparse", when="+amd")
    depends_on("metis", when="+metis")
    depends_on("scotch", when="+scotch")
    depends_on("starpu", when="+starpu")
    depends_on("cuda", when="+starpu+cuda")
    depends_on("starpu+cuda", when="+starpu+cuda")
    depends_on("starpu+fxt", when="+starpu+fxt")

    def cmake_args(self):
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define_from_variant("QRM_ORDERING_AMD", "amd"),
            self.define_from_variant("QRM_ORDERING_SCOTCH", "scotch"),
            self.define_from_variant("QRM_ORDERING_METIS", "metis"),
            self.define_from_variant("QRM_WITH_STARPU", "starpu"),
            self.define_from_variant("QRM_WITH_CUDA", "cuda"),
        ]

        return args
