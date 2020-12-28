# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlParallelForkmanager(PerlPackage):
    """A simple parallel processing fork manager"""

    homepage = "http://search.cpan.org/~yanick/Parallel-ForkManager/lib/Parallel/ForkManager.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/Y/YA/YANICK/Parallel-ForkManager-1.19.tar.gz"

    version('1.19', sha256='f1de2e9875eeb77d65f80338905dedd522f3913822502982f805aa71cde5a472')
