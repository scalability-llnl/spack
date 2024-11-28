# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlBioAsn1Entrezgene(PerlPackage):
    """Regular expression-based Perl Parser for NCBI Entrez Gene."""

    homepage = "https://metacpan.org/pod/Bio::ASN1::EntrezGene"
    url = "https://cpan.metacpan.org/authors/id/C/CJ/CJFIELDS/Bio-ASN1-EntrezGene-1.73.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.73", sha256="f9e778db705ce5c35ad2798e38a8490b644edfdc14253aa1b74a1f5e79fc6a4b")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-bio-cluster", type=("build", "run", "test"))
    depends_on("perl-bioperl", type=("build", "run", "test"))
