# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Alan(Package):
    """Alignment viewer for linux terminal"""

    homepage = "https://github.com/mpdunne/alan"
    url = "https://github.com/mpdunne/alan/archive/2.1.1.tar.gz"

    version("2.1.1", sha256="c92ac570be6da490a0b3178c565cf649414829d74a14e9f6ec32c5a05caa1755")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("alan", prefix.bin)
