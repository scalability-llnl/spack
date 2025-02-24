# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPkgload(RPackage):
    """Simulate Package Installation and Attach.

    Simulates the process of installing a package and then attaching it. This
    is a key part of the 'devtools' package as it allows you to rapidly iterate
    while developing a package."""

    cran = "pkgload"

    license("GPL-3.0-only")

    version("1.4.0", sha256="09e4885e9cc25af29063a525da0b2ac9dd66fc7a95ea085bf5060312e3a67549")
    version("1.3.4", sha256="60b04b948cda4dc56257b1e89f9b0a4b1273cacecdb2bd995d66dd76e89926ce")
    version("1.3.3", sha256="b0898122876479cc4a35cd566654b3a7b50f8ac105565dbf3f8b9d4283816959")
    version("1.3.2.1", sha256="a1987b123fcbdb9d908b6dc55a04d3cf47d68cfa5090186e4876a429313374b2")
    version("1.3.2", sha256="35d19a032bfeeefcab92d76a768b4a420c2ede0920badaf48cca878592b46b2f")
    version("1.3.1", sha256="c6b8b70d7b7e194e7d44a42364f0362e971d9ab9c5794c4ae5ed4f9e61b1679a")
    version("1.3.0", sha256="5af653c901662260cc221971cc968355428cc6183b61c15be80aa9545f9f4228")
    version("1.2.4", sha256="d6912bc824a59ccc9b2895c3cf3b08a3ff310a333888bb8e90d1a6ce754dd90f")
    version("1.1.0", sha256="189d460dbba2b35fa15dd59ce832df252dfa654a5acee0c9a8471b4d70477b0d")
    version("1.0.2", sha256="3186564e690fb05eabe76e1ac0bfd4312562c3ac8794b29f8850399515dcf27c")

    depends_on("r@3.4.0:", type=("build", "run"), when="@1.3.0:")

    depends_on("r-cli", type=("build", "run"), when="@1.1.0:")
    depends_on("r-cli@3.3.0:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-crayon", type=("build", "run"), when="@1.1.0:1.3")
    depends_on("r-desc", type=("build", "run"))
    depends_on("r-glue", type=("build", "run"), when="@1.3.0:")
    depends_on("r-fs", type=("build", "run"), when="@1.3.0:")
    depends_on("r-lifecycle", type=("build", "run"), when="@1.4.0:")
    depends_on("r-processx", type=("build", "run"), when="@1.4.0:")
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-rlang@1.0.3:", type=("build", "run"), when="@1.3.0:1.3.3")
    depends_on("r-rlang@1.1.1:", type=("build", "run"), when="@1.3.4:")
    depends_on("r-rprojroot", type=("build", "run"))
    depends_on("r-withr", type=("build", "run"))
    depends_on("r-withr@2.4.3:", type=("build", "run"), when="@1.3.0:")

    depends_on("r-pkgbuild", type=("build", "run"), when="@:1.1.0")
    depends_on("r-pkgbuild", type=("build", "run"), when="@1.3.4:")
    depends_on("r-rstudioapi", type=("build", "run"), when="@:1.2.4")
