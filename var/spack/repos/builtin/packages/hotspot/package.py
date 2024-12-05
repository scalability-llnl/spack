# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hotspot(MakefilePackage):
    """HotSpot is an accurate and fast thermal model suitable for use ini
    architectural studies."""

    homepage = "http://lava.cs.virginia.edu/HotSpot/index.htm"
    git = "https://github.com/uvahotspot/HotSpot.git"

    version("6.0", commit="a7a3286e368867c26381e0a23e36b3e273bdeda9")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("hotspot", prefix.bin)
        install("hotfloorplan", prefix.bin)
