# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openlibm(MakefilePackage):
    """OpenLibm is an effort to have a high quality, portable, standalone C
    mathematical library"""

    homepage = "https://github.com/JuliaMath/openlibm"
    url = "https://github.com/JuliaMath/openlibm/archive/refs/tags/v0.8.0.tar.gz"

    maintainers("haampie")

    license("MIT AND BSD-2-Clause AND ISC AND LGPL-2.1-or-later")

    version("0.8.1", sha256="ba8a282ecd92d0033f5656bb20dfc6ea3fb83f90ba69291ac8f7beba42dcffcf")
    version("0.8.0", sha256="03620768df4ca526a63dd675c6de95a5c9d167ff59555ce57a61c6bf49e400ee")
    version("0.7.5", sha256="be983b9e1e40e696e8bbb7eb8f6376d3ca0ae675ae6d82936540385b0eeec15b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def make(self, spec, prefix):
        args = [
            "prefix={0}".format(prefix),
            "USE_GCC={0}".format("1" if self.compiler.name == "gcc" else "0"),
            "USE_CLANG={0}".format("1" if self.compiler.name == "clang" else "0"),
        ]
        make(*args)

    def install(self, spec, prefix):
        args = ["prefix={0}".format(prefix)]
        make("install", *args)
