# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlKyotocabinet(PerlPackage):
    """Kyoto Cabinet is a library of routines for managing a database."""

    homepage = "https://dbmx.net/kyotocabinet/"
    url = "https://dbmx.net/kyotocabinet/perlpkg/kyotocabinet-perl-1.20.tar.gz"

    maintainers("EbiArnie")

    license("GPL-3.0-or-later")

    version("1.20", sha256="19b3654dc6febfd0b91e54f36b2a0ebdaeaefaf7875f5aab337ad846a4095c32")

    depends_on("kyotocabinet", type=("build", "link", "run", "test"))
    depends_on("zlib-api", type=("build", "link", "run", "test"))
    depends_on("lzo", type=("build", "link", "run", "test"))
    depends_on("xz", type=("build", "link", "run", "test"))
