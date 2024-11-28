# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlBioEutilities(PerlPackage):
    """BioPerl low-level API for retrieving and storing data from NCBI eUtils"""

    homepage = "https://metacpan.org/pod/Bio::DB::EUtilities"
    url = "https://cpan.metacpan.org/authors/id/C/CJ/CJFIELDS/Bio-EUtilities-1.77.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.77", sha256="4d018c8cbda73c3d71487165261a3dfc4e823f8e22747497f6a586d5ad6f737f")

    depends_on("perl@5.10.0:", type=("build", "link", "run", "test"))
    depends_on("perl-bio-asn1-entrezgene", type=("build", "run", "test"))
    depends_on("perl-bioperl", type=("build", "run", "test"))
    depends_on("perl-http-message", type=("build", "run", "test"))
    depends_on("perl-libwww-perl", type=("build", "run", "test"))
    depends_on("perl-text-csv", type=("build", "run", "test"))
    depends_on("perl-uri", type=("build", "run", "test"))
    depends_on("perl-xml-simple", type=("build", "run", "test"))
