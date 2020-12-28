# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlGdgraph(PerlPackage):
    """Graph Plotting Module for Perl 5"""

    homepage = "http://search.cpan.org/~bwarfield/GDGraph/Graph.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/B/BW/BWARFIELD/GDGraph-1.4308.tar.gz"

    version('1.4308', sha256='75b3c7e280431404ed096c6e120d552cc39052a8610787149515e94b9ba237cb')

    depends_on('perl-capture-tiny', type=('build', 'run'))
    depends_on('perl-test-exception', type=('build', 'run'))
    depends_on('perl-gdtextutil', type=('build', 'run'))
    depends_on('perl-gd', type=('build', 'run'))
