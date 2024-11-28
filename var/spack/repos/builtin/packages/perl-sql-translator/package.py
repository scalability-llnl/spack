# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSqlTranslator(PerlPackage):
    """SQL DDL transformations and more"""

    homepage = "https://metacpan.org/pod/SQL::Translator"
    url = "https://cpan.metacpan.org/authors/id/V/VE/VEESH/SQL-Translator-1.65.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.65", sha256="606750db6a4ebf2693aa9bc8444c998c169b76bc308f3d314ead5eac17bede4a")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-carp-clan", type=("build", "run", "test"))
    depends_on("perl-dbi@1.54:", type=("build", "run", "test"))
    depends_on("perl-file-sharedir@1.0:", type=("build", "run", "test"))
    depends_on("perl-file-sharedir-install", type=("build"))
    depends_on("perl-json-maybexs@1.003003:", type=("build", "test"))
    depends_on("perl-moo@1.000003:", type=("build", "run", "test"))
    depends_on("perl-package-variant@1.001001:", type=("build", "run", "test"))
    depends_on("perl-parse-recdescent@1.967009:", type=("build", "run", "test"))
    depends_on("perl-sub-quote", type=("build", "run", "test"))
    depends_on("perl-test-differences", type=("build", "test"))
    depends_on("perl-test-exception@0.42:", type=("build", "test"))
    depends_on("perl-try-tiny@0.04:", type=("build", "run", "test"))
    depends_on("perl-xml-writer@0.500:", type=("build", "test"))
    depends_on("perl-yaml@0.66:", type=("build", "test"))
