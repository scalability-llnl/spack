# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dlpack(Package):
    """DLPack is an RFC for common tensor and operator guidelines
    in deep learning systems."""

    homepage = "https://github.com/dmlc/dlpack"
    git = "https://github.com/dmlc/dlpack.git"
    url = "https://github.com/dmlc/dlpack/archive/refs/tags/v0.5.tar.gz"

    license("Apache-2.0")

    version("master", branch="master")
    version("0.8", sha256="cf965c26a5430ba4cc53d61963f288edddcd77443aa4c85ce722aaf1e2f29513")
    version("0.5", sha256="9209ac194a175aaab4381313891fba047cb173b2bdd15ac934f83f567f9cd514")
    version("0.4", sha256="d0a533189ecd45a033b72e276fccaa2122cfd76de125e0a5e126bdea0fec2d24")
    version("0.3", sha256="703149f5b39ead42cc734c03c7c4bd581fcad1c5a3939e7a4b5bc82f54c3c32a")
    version("0.2", sha256="419f76ef723d21b72b704b2c4bf718dcd9d2ecd44cd28c8a71798389b7932ae5")
    version("0.1", sha256="c69b06bfe03711e9d9d3f4d3f307d6dfd7e21d4864a053cca26296d5d05c175c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        install_tree("include", prefix.include)
