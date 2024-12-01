# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RecolaSm(CMakePackage):
    """Standard Model files for the Recola generator."""

    tags = ["hep"]

    homepage = "https://recola.gitlab.io/recola2/modelfiles/modelfiles.html"
    url = "https://recola.hepforge.org/downloads/?f=SM_2.2.3.tar.gz"

    maintainers("vvolkl")

    license("GPL-3.0-only")

    version("2.2.3", sha256="9ebdc4fd8ca48789de0b6bbb2ab7e4845c92d19dfe0c3f67866cbf114d6242a5")

    depends_on("fortran", type="build")  # generated

    depends_on("collier")

    def cmake_args(self):
        args = [
            self.define("static", True),
            self.define("collier_path", self.spec["collier"].prefix.lib.cmake),
        ]
        return args
