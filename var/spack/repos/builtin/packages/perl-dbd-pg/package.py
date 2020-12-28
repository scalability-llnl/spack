# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDbdPg(PerlPackage):
    """DBD::Pg is a Perl module that works with the DBI module to provide
    access to PostgreSQL databases."""

    homepage = "https://metacpan.org/pod/DBD::Pg"
    url      = "https://cpan.metacpan.org/authors/id/T/TU/TURNSTEP/DBD-Pg-3.10.0.tar.gz"

    version('3.10.0', sha256='e103268a63e2828e3d43659bdba5f743446cbbe047a766f843112eedae105f80')

    depends_on('postgresql')
    depends_on('perl-dbi', type=('build', 'run'))
