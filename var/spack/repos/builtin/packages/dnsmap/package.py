# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dnsmap(MakefilePackage):
    """dnsmap was originally released back in 2006 and was inspired
    by the fictional story."""

    homepage = "https://github.com/makefu/dnsmap"
    git = "https://github.com/makefu/dnsmap.git"

    license("GPL-2.0-or-later")

    version("master", branch="master")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("dnsmap", prefix.bin)
