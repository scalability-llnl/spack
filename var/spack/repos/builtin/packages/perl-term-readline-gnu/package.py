# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PerlTermReadlineGnu(PerlPackage):
    """Perl extension for the GNU Readline/History Library."""

    homepage = "https://metacpan.org/pod/Term::ReadLine::Gnu"
    url      = "https://cpan.metacpan.org/authors/id/H/HA/HAYASHI/Term-ReadLine-Gnu-1.36.tar.gz"

    version('1.36', sha256='9a08f7a4013c9b865541c10dbba1210779eb9128b961250b746d26702bab6925')

    depends_on('readline')
