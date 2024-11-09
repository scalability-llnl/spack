# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Maverick(MakefilePackage):
    """MavericK is a program for inferring population structure on the basis
    of genetic information."""

    homepage = "https://github.com/bobverity/MavericK"
    url = "https://github.com/bobverity/MavericK/archive/v1.0.4.tar.gz"

    version("1.0.4", sha256="d4634c1b3f09cec9eb60d72348e2f479d74220ecbdebd940bb18b480db8df8cb")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    conflicts("%gcc@:6.0")
    conflicts("%cce")
    conflicts("%apple-clang")
    conflicts("%clang")
    conflicts("%intel")
    conflicts("%nag")
    conflicts("%pgi")
    conflicts("%xl")
    conflicts("%xl_r")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("MavericK", prefix.bin)
