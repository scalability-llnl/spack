# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sentencepiece(CMakePackage):
    """Unsupervised text tokenizer for Neural Network-based text generation.

    This is the C++ package."""

    homepage = "https://github.com/google/sentencepiece"
    url = "https://github.com/google/sentencepiece/archive/v0.1.85.tar.gz"

    maintainers("adamjstewart")

    license("Apache-2.0")

    version("0.1.91", sha256="acbc7ea12713cd2a8d64892f8d2033c7fd2bb4faecab39452496120ace9a4b1b")
    version("0.1.85", sha256="dd4956287a1b6af3cbdbbd499b7227a859a4e3f41c9882de5e6bdd929e219ae6")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.1:", type="build")
    depends_on("gperftools")  # optional, 10-40% performance improvement
