# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlGraphReadwrite(PerlPackage):
    """Write out directed graph in Dot format"""

    homepage = "https://metacpan.org/pod/Graph::ReadWrite"
    url = "http://search.cpan.org/CPAN/authors/id/N/NE/NEILB/Graph-ReadWrite-2.09.tar.gz"

    license("Artistic-1.0")

    version("2.10", sha256="516c1ea9facb995dbc38d1735d58974b2399862567e731b729c8d0bc2ee5a14b")
    version("2.09", sha256="b01ef06ce922eea12d5ce614d63ddc5f3ee7ad0d05f9577051d3f87a89799a4a")
