# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlConfigTiny(PerlPackage):
    """Read/Write .ini style files with as little code as possible"""

    homepage = "https://metacpan.org/pod/Config::Tiny"
    url = "https://cpan.metacpan.org/authors/id/R/RS/RSAVAGE/Config-Tiny-2.30.tgz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.30", sha256="b2f7345619b3b8e636dd39ea010731c9dc2bfb8f022bcbd86ae6ad17866e110d")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
