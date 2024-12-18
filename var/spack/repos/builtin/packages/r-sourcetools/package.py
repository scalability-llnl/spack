# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSourcetools(RPackage):
    """Tools for Reading, Tokenizing and Parsing R Code.

    Tools for the reading and tokenization of R code. The 'sourcetools' package
    provides both an R and C++ interface for the tokenization of R code, and
    helpers for interacting with the tokenized representation of R code."""

    cran = "sourcetools"

    license("MIT")

    version("0.1.7-1", sha256="96812bdb7a0dd99690d84e4b0a3def91389e4290f53f01919ef28a50554e31d1")
    version("0.1.7", sha256="47984406efb3b3face133979ccbae9fefb7360b9a6ca1a1c11473681418ed2ca")
    version("0.1.6", sha256="c9f48d2f0b7f7ed0e7fecdf8e730b0b80c4d567f0e1e880d118b0944b1330c51")
    version("0.1.5", sha256="c2373357ad76eaa7d03f9f01c19b5001a3e4db788acbca068b0abbe7a99ea64b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@3.0.2:", type=("build", "run"))
