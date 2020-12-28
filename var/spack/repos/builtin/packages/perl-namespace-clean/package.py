# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlNamespaceClean(PerlPackage):
    """Keep imports and functions out of your namespace."""

    homepage = "http://search.cpan.org/~ribasushi/namespace-clean-0.27/lib/namespace/clean.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RI/RIBASUSHI/namespace-clean-0.27.tar.gz"

    version('0.27', sha256='8a10a83c3e183dc78f9e7b7aa4d09b47c11fb4e7d3a33b9a12912fd22e31af9d')

    depends_on('perl-b-hooks-endofscope', type=('build', 'run'))
