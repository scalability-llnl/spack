# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlGzipFaster(PerlPackage):
    """Simple and fast gzip and gunzip"""

    homepage = "https://metacpan.org/pod/Gzip::Faster"
    url = "https://cpan.metacpan.org/authors/id/B/BK/BKB/Gzip-Faster-0.21.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.21", sha256="c65f41ca108e7e53ec34c30dbb1b5d614bf4b8100673646cf301d0caf82c7aa5")

    depends_on("c", type="build")  # generated

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
