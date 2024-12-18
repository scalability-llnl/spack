# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSubName(PerlPackage):
    """Name or rename a sub"""

    homepage = "https://metacpan.org/pod/Sub::Name"
    url = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Sub-Name-0.21.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.27", sha256="ecf36fba1c47ca93e1daa394968ed39c4186867459d9cd173c421e2b972043e8")
    version("0.26", sha256="2d2f2d697d516c89547e7c4307f1e79441641cae2c7395e7319b306d390df105")
    version("0.21", sha256="bd32e9dee07047c10ae474c9f17d458b6e9885a6db69474c7a494ccc34c27117")
