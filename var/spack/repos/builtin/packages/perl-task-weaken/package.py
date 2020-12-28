# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTaskWeaken(PerlPackage):
    """Ensure that a platform has weaken support"""

    homepage = "http://search.cpan.org/~adamk/Task-Weaken-1.04/lib/Task/Weaken.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/A/AD/ADAMK/Task-Weaken-1.04.tar.gz"

    version('1.04', sha256='67e271c55900fe7889584f911daa946e177bb60c8af44c32f4584b87766af3c4')
