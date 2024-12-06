# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStringFormat(PerlPackage):
    """Sprintf-like string formatting capabilities with arbitrary format definitions"""

    homepage = "https://metacpan.org/pod/String::Format"
    url = "https://cpan.metacpan.org/authors/id/S/SR/SREZIC/String-Format-1.18.tar.gz"

    maintainers("EbiArnie")

    version("1.18", sha256="9e417a8f8d9ea623beea2d13a47c0d5a696fc8602c0509b826cd45f97b76e778")
