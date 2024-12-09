# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Samblaster(MakefilePackage):
    """A tool to mark duplicates and extract discordant and split reads from
    sam files."""

    homepage = "https://github.com/GregoryFaust/samblaster"
    url = "https://github.com/GregoryFaust/samblaster/archive/v.0.1.24.tar.gz"

    license("MIT")

    version("0.1.26", sha256="6b42a53d64a3ed340852028546693a24c860f236fd70e90c2b24fde9dcc4fd63")
    version("0.1.24", sha256="72c42e0a346166ba00152417c82179bd5139636fea859babb06ca855af93d11f")
    version("0.1.23", sha256="0d35ce629771946e3d6fc199025747054e5512bffa1ba4446ed81160fffee57a")

    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("samblaster", prefix.bin)
