# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlBioVariation(PerlPackage):
    """BioPerl variation-related functionality"""

    homepage = "https://metacpan.org/pod/Bio::Variation"
    url = "https://cpan.metacpan.org/authors/id/C/CJ/CJFIELDS/Bio-Variation-1.7.5.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.7.5", sha256="4bffdd060b5e793919f700e46056eb3f0195ed4df2e60ad68b383c31e51f824f")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-bioperl", type=("build", "run", "test"))
    depends_on("perl-io-string", type=("build", "run", "test"))
    depends_on("perl-xml-twig", type=("build", "run", "test"))
    depends_on("perl-xml-writer@0.4:", type=("build", "run", "test"))
