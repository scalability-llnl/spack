# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExporterTiny(PerlPackage):
    """An exporter with the features of Sub::Exporter but only core
    dependencies"""

    homepage = "https://metacpan.org/pod/Exporter::Tiny"
    url = "http://search.cpan.org/CPAN/authors/id/T/TO/TOBYINK/Exporter-Tiny-1.000000.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.006002", sha256="6f295e2cbffb1dbc15bdb9dadc341671c1e0cd2bdf2d312b17526273c322638d")
    version("1.006001", sha256="8df2a7ee5a11bacb8166edd9ee8fc93172278a74d5abe2021a5f4a7d57915c50")
    version("1.006000", sha256="d95479ff085699d6422f7fc8306db085e34b626438deb82ec82d41df2295f400")
    version("1.000000", sha256="ffdd77d57de099e8f64dd942ef12a00a3f4313c2531f342339eeed2d366ad078")
