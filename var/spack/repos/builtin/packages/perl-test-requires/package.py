# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestRequires(PerlPackage):
    """Checks to see if the module can be loaded."""

    homepage = "http://search.cpan.org/~tokuhirom/Test-Requires-0.10/lib/Test/Requires.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/T/TO/TOKUHIROM/Test-Requires-0.10.tar.gz"

    version('0.10', sha256='2768a391d50ab94b95cefe540b9232d7046c13ee86d01859e04c044903222eb5')
