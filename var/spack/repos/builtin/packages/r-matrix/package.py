# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMatrix(RPackage):
    """Sparse and Dense Matrix Classes and Methods.

    A rich hierarchy of matrix classes, including triangular, symmetric, and
    diagonal matrices, both dense and sparse and with pattern, logical and
    numeric entries.   Numerous methods for and operations on these matrices,
    using 'LAPACK' and 'SuiteSparse' libraries."""

    cran = "Matrix"

    license("GPL-3.0-only")

    version("1.7-0", sha256="fb97bba0df370222eb4f7e2da2e94dd01053b5e054b1c51829ff9a6efc08ad37")
    version("1.5-4", sha256="15ceb61993d61b442068104abb46e6d91b5a1179c01eeb64563b853abab66f06")
    version("1.5-1", sha256="557dba0358172d67dc63eb5db90841915bb5ce1528f941a8005ae808d635575d")
    version("1.4-1", sha256="42b24f1d1e94482b0ff0ef1292e2df29f69694bdbee47b3d6bfeec46fafb2f7e")
    version("1.4-0", sha256="c2b463702e4051b621f5e2b091a33f883f1caa97703d65f7a52b78caf81206f6")
    version("1.3-4", sha256="ab42179d44545e99bbdf44bb6d04cab051dd2aba552b1f6edd51ed71b55f6c39")
    version("1.3-3", sha256="f77ec8de43ae7bfa19dfdc7e76bfefbb21b3223dbc174423fcde70b44cf36a3b")
    version("1.3-2", sha256="950ba5d91018e711fd2743b3486a50dc47ae9c271389fce587792f0a9aab9531")
    version("1.2-17", sha256="db43e6f0196fd5dfd05a7e88cac193877352c60d771d4ec8772763e645723fcc")
    version("1.2-14", sha256="49a6403547b66675cb44c1afb04bb87130c054510cb2b94971435a826ab41396")
    version("1.2-11", sha256="ba8cd6565612552fe397e909721817b6cc0604a91299d56d118208006888dc0b")
    version("1.2-8", sha256="3cd2a187c45fc18a0766dc148b7f83dbf6f2163c256e887c41cbaa7c9a20dbb7")
    version("1.2-6", sha256="4b49b639b7bf612fa3d1c1b1c68125ec7859c8cdadae0c13f499f24099fd5f20")

    depends_on("r@3.0.1:", type=("build", "run"))
    depends_on("r@3.2.0:", type=("build", "run"), when="@1.2-13:")
    depends_on("r@3.6.0:", type=("build", "run"), when="@1.3-2:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.3-3:")
    depends_on("r@4.4.0:", type=("build", "run"), when="@1.7-0:")
    depends_on("r-lattice", type=("build", "run"))
