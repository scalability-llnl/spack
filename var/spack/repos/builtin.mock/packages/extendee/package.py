# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Extendee(Package):
    """A package with extensions"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/extendee-1.0.tar.gz"

    extendable = True

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
