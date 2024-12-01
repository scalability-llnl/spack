# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlParallelForkmanager(PerlPackage):
    """A simple parallel processing fork manager"""

    homepage = "https://metacpan.org/pod/Parallel::ForkManager"
    url = "http://search.cpan.org/CPAN/authors/id/Y/YA/YANICK/Parallel-ForkManager-1.19.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.02", sha256="c1b2970a8bb666c3de7caac4a8f4dbcc043ab819bbc337692ec7bf27adae4404")
    version("1.19", sha256="f1de2e9875eeb77d65f80338905dedd522f3913822502982f805aa71cde5a472")
