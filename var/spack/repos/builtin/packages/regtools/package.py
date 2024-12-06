# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Regtools(CMakePackage):
    """Tools that integrate DNA-seq and RNA-seq data to help interpret mutations in a regulatory
    and splicing context"""

    homepage = "https://regtools.readthedocs.org/"
    url = "https://github.com/griffithlab/regtools/archive/refs/tags/1.0.0.tar.gz"

    license("MIT", checked_by="A-N-Other")

    version("1.0.0", sha256="ed2b9db6b71b943924002653caee18511a22ed7cc3c88f428e7e9e0c2e4f431b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(join_path(self.build_directory, "regtools"), prefix.bin)
