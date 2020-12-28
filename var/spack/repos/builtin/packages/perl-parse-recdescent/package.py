# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlParseRecdescent(PerlPackage):
    """Generate Recursive-Descent Parsers"""

    homepage = "http://search.cpan.org/~jtbraun/Parse-RecDescent-1.967015/lib/Parse/RecDescent.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/J/JT/JTBRAUN/Parse-RecDescent-1.967015.tar.gz"

    version('1.967015', sha256='1943336a4cb54f1788a733f0827c0c55db4310d5eae15e542639c9dd85656e37')

    depends_on('perl-module-build', type='build')
