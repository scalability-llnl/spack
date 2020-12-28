# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestRequiresinternet(PerlPackage):
    """Easily test network connectivity"""

    homepage = "http://search.cpan.org/~mallen/Test-RequiresInternet-0.05/lib/Test/RequiresInternet.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/M/MA/MALLEN/Test-RequiresInternet-0.05.tar.gz"

    version('0.05', sha256='bba7b32a1cc0d58ce2ec20b200a7347c69631641e8cae8ff4567ad24ef1e833e')
