# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GtkorvoCercsEnv(CMakePackage):
    """A utility library used by some GTkorvo packages."""

    homepage = "https://github.com/GTkorvo/cercs_env"
    url = "https://github.com/GTkorvo/cercs_env/archive/v1.0.tar.gz"
    git = "https://github.com/GTkorvo/cercs_env.git"

    version("develop", branch="master")
    version("1.0", sha256="e4080a98c1af5003a038361c8bb343843665cac428101ac7d721bad8ba7d244e")

    depends_on("c", type="build")  # generated

    def cmake_args(self):
        args = ["-DENABLE_TESTING=0", "-DENABLE_SHARED_STATIC=STATIC"]
        return args
