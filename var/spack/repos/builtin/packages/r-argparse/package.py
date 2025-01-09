# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RArgparse(RPackage):
    """Command Line Optional and Positional Argument Parser.

    A command line parser to be used with Rscript to write "#!" shebang scripts
    that gracefully accept positional and optional arguments and automatically
    generate usage."""

    cran = "argparse"

    license("GPL-2.0-or-later")

    version("2.2.3", sha256="a50cc4e1221f063e472a8cfe7e881a1d4abed5ef93cf40d5f65a2528cdfd2674")
    version("2.2.2", sha256="b62c9bf5e6ca35fb7a2e614a916815c04cbf6c6db3f89f99b4df76470a4a856d")
    version("2.1.6", sha256="2ad7faad795878b88969ac5d91ba38f4e96deb85dfea7148c3510f0eaa3de592")
    version("2.1.5", sha256="83e112beb47733849980b286d93ac930f0cbe6ac78fcb94fc9f6b0eea882658d")
    version("2.1.3", sha256="aeda31a54a8d7a0a511cfbf7c5868637e129922671d43938165867437fb6a66e")
    version("2.0.3", sha256="d26139c610ea0adf8d6632699cd34c4595ae3e7963bfc7a00cb3b7504f2059b0")
    version("2.0.1", sha256="949843920d14fc7c162aedab331a936499541736e7dafbb103fbfd79be8147ab")
    version("1.1.1", sha256="441449f0816411a868fd1b15cf4b2bc45931bbd4b67d6592dbe48875905cf93b")

    depends_on("r@3.6.0:", type=("build", "run"), when="@2.1.6:")

    depends_on("r-r6", type=("build", "run"), when="@2.0.0:")
    depends_on("r-findpython", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("python@3.2:", type=("build", "run"))

    depends_on("r-proto@1:", type=("build", "run"), when="@1.0.0:1.9.9")
    depends_on("r-getopt", type=("build", "run"), when="@1.0.0:1.9.9")
