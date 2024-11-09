# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Agrep(MakefilePackage):
    """AGREP - an approximate GREP.
    Fast searching files for a string or regular expression,
    with approximate matching capabilities and user-definable records.
    Developed 1989-1991 by Udi Manber, Sun Wu et al. at the University
    of Arizona."""

    homepage = "https://www.tgries.de/agrep"
    url = "https://www.tgries.de/agrep/agrep-3.41.tgz"

    license("GPL-2.0-or-later")

    version("3.41", sha256="0508eafaf9725fc67cc955eb6d32ba4f50138443a4fea4275508d2c3f67a234e")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("agrep", prefix.bin)
