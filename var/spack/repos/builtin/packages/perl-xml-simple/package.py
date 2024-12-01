# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlXmlSimple(PerlPackage):
    """An API for simple XML files"""

    homepage = "https://metacpan.org/pod/XML::Simple"
    url = "http://search.cpan.org/CPAN/authors/id/G/GR/GRANTM/XML-Simple-2.24.tar.gz"

    license("Artistic-1.0-Perl")

    version("2.25", sha256="531fddaebea2416743eb5c4fdfab028f502123d9a220405a4100e68fc480dbf8")
    version("2.24", sha256="9a14819fd17c75fbb90adcec0446ceab356cab0ccaff870f2e1659205dc2424f")

    depends_on("perl-xml-parser", type=("build", "run"))
