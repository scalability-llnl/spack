# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kmergenie(MakefilePackage):
    """KmerGenie estimates the best k-mer length for genome de novo assembly."""

    homepage = "http://kmergenie.bx.psu.edu/"
    url = "http://kmergenie.bx.psu.edu/kmergenie-1.7044.tar.gz"

    license("CECILL-1.1")

    version("1.7051", sha256="13148e5a2c700359cffca363b66ffa8f23c5db6af6eec03f739139ffdfee763f")
    version("1.7044", sha256="46f2a08a2d7b1885414143e436829dd7e61fcc31ec4e429433e516a168d2978e")

    depends_on("cxx", type="build")  # generated

    depends_on("python", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("r", type=("build", "run"))
    depends_on("zlib-api")

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix.bin)
