# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlBioCluster(PerlPackage):
    """BioPerl cluster modules"""

    homepage = "https://metacpan.org/pod/Bio::Cluster"
    url = "https://cpan.metacpan.org/authors/id/C/CJ/CJFIELDS/Bio-Cluster-1.7.3.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.7.3", sha256="1967fb3899b92f245b5bf6cb64ef076fc3f8427b1a96ca5f7b74d220b6191fbb")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-bio-variation", type=("build", "run", "test"))
    depends_on("perl-bioperl", type=("build", "run", "test"))
    depends_on("perl-xml-sax", type=("build", "run", "test"))
