# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Typhon(CMakePackage):
    """
    Typhon is a distributed communications library for unstructured mesh
    applications.
    """

    homepage = "https://github.com/UK-MAC/Typhon"
    url = "https://github.com/UK-MAC/Typhon/archive/v3.0.tar.gz"
    git = "https://github.com/UK-MAC/Typhon.git"

    license("GPL-3.0-only")

    version("develop", branch="develop")

    version("3.0.2", sha256="28087eb07bf91d23792900214728b5eea61b5e81aa33df28c032dadd6d89b76e")
    version("3.0.1", sha256="8d6e19192e52eadf92175423ae0efd8a1a343c2ea2bc48aacb9028074447c2bb")
    version("3.0", sha256="b9736269ebe9c0fd7efabc4716b0543144780ed26ddaf595083354113aa2efd7")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("mpi")

    def setup_build_environment(self, env):
        if self.spec.satisfies("%fj"):
            env.set("LDFLAGS", "--linkfortran")
