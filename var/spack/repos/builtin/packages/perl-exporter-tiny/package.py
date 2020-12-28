# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExporterTiny(PerlPackage):
    """An exporter with the features of Sub::Exporter but only core
    dependencies"""

    homepage = "http://search.cpan.org/~tobyink/Exporter-Tiny/lib/Exporter/Tiny.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/T/TO/TOBYINK/Exporter-Tiny-1.000000.tar.gz"

    version('1.000000', sha256='ffdd77d57de099e8f64dd942ef12a00a3f4313c2531f342339eeed2d366ad078')
