# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestLeaktrace(PerlPackage):
    """Test::LeakTrace provides several functions that trace memory leaks. This module scans
    arenas, the memory allocation system, so it can detect any leaked SVs in given blocks."""

    homepage = "https://metacpan.org/pod/Test::LeakTrace"
    url = "https://cpan.metacpan.org/authors/id/L/LE/LEEJO/Test-LeakTrace-0.17.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.17", sha256="777d64d2938f5ea586300eef97ef03eacb43d4c1853c9c3b1091eb3311467970")
