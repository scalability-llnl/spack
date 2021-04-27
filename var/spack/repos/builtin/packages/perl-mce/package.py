# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PerlMce(PerlPackage):
    """MCE - Many-Core Engine for Perl providing parallel processing
    capabilities.

    MCE spawns a pool of workers and therefore does not fork a new process per
    each element of data. Instead, MCE follows a bank queuing model. Imagine
    the line being the data and bank-tellers the parallel workers. MCE enhances
    that model by adding the ability to chunk the next n elements from the
    input stream to the next available worker."""

    homepage = "https://github.com/marioroy/mce-perl"
    url      = "https://cpan.metacpan.org/authors/id/M/MA/MARIOROY/MCE-1.874.tar.gz"

    version('1.874', sha256='d809e3018475115ad7eccb8bef49bde3bf3e75abbbcd80564728bbcfab86d3d0')
