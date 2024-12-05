# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Dpmjet(MakefilePackage):
    """DPMJET-III is a Monte Carlo event generator for hadron, photon
    and nuclear collisions."""

    homepage = "https://github.com/DPMJET/DPMJET"
    url = "https://github.com/DPMJET/DPMJET/archive/refs/tags/v19.3.3.zip"
    list_url = "https://github.com/DPMJET/DPMJET/tags"
    git = "https://github.com/DPMJET/DPMJET.git"

    maintainers("wdconinc")

    license("BSD-3-Clause")

    version("19.3.5", sha256="5a546ca20f86abaecda1828eb5b577aee8a532dffb2c5e7244667d5f25777909")
    version("19.3.4", sha256="646f520aa67ef6355c45cde155a5dd55f7c9d661314358a7668f6ff472f5d5f9")
    version("19.3.3", sha256="4f449a36b48ff551beb4303d66bac18bebc52dbcac907f84ab7716c914ad6d8a")
    version("19.2.0", sha256="0f5c1af4419e1a8fa4b46cc24ae1da98abe5c119064275e1848538fe033f02cc")
    version("19.1.3", sha256="f2f7f9eee0fcd1e2770382fa6e3491418607e33de2272e04b6d75ebc97640474")

    depends_on("python@3:")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter(r"install: \$\(pylib\)", "install:")

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
        install_tree("include", prefix.include)
