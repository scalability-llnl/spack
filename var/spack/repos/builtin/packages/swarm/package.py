# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Swarm(MakefilePackage):
    """A robust and fast clustering method for amplicon-based studies."""

    homepage = "https://github.com/torognes/swarm"
    url = "https://github.com/torognes/swarm/archive/v2.1.13.tar.gz"

    license("AGPL-3.0-only")

    version("3.0.0", sha256="b63761a9914ebf1fee14befaffd93af9c795b692c006c644d049a6d985b55810")
    version("2.1.13", sha256="ec4b22cc1874ec6d2c89fe98e23a2fb713aec500bc4a784f0556389d22c02650")

    depends_on("cxx", type="build")  # generated

    conflicts("@2.1.13", when="target=aarch64:")

    build_directory = "src"

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("scripts", prefix.scripts)
        install_tree("man", prefix.share.man)
