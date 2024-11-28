# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDbixClass(PerlPackage):
    """Extensible and flexible object <-> relational mapper."""

    homepage = "https://metacpan.org/pod/DBIx::Class"
    url = "https://cpan.metacpan.org/authors/id/R/RI/RIBASUSHI/DBIx-Class-0.082843.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.082843", sha256="341e0b6ecb29d8c49174a6c09d7c6dbf38729ba4015ee7fd70360a4ffee1f251")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-class-accessor-grouped@0.10012:", type=("build", "run", "test"))
    depends_on("perl-class-c3-componentised@1.0009:", type=("build", "run", "test"))
    depends_on("perl-class-inspector@1.24:", type=("build", "run", "test"))
    depends_on("perl-config-any@0.20:", type=("build", "run", "test"))
    depends_on("perl-context-preserve@0.01:", type=("build", "run", "test"))
    depends_on("perl-data-dumper-concise@2.020:", type=("build", "run", "test"))
    depends_on("perl-dbd-sqlite@1.29:", type=("build", "link"))
    depends_on("perl-dbi@1.57:", type=("build", "run", "test"))
    depends_on("perl-devel-globaldestruction@0.09:", type=("build", "run", "test"))
    depends_on("perl-hash-merge@0.12:", type=("build", "run", "test"))
    depends_on("perl-module-find@0.07:", type=("build", "run", "test"))
    depends_on("perl-moo@2.000:", type=("build", "run", "test"))
    depends_on("perl-mro-compat@0.12:", type=("build", "run", "test"))
    depends_on("perl-namespace-clean@0.24:", type=("build", "run", "test"))
    depends_on("perl-package-stash@0.28:", type=("build", "link"))
    depends_on("perl-path-class@0.18:", type=("build", "run", "test"))
    depends_on("perl-scope-guard@0.03:", type=("build", "run", "test"))
    depends_on("perl-sql-abstract-classic@1.91:", type=("build", "run", "test"))
    depends_on("perl-sub-name@0.04:", type=("build", "run", "test"))
    depends_on("perl-test-deep@0.101:", type=("build", "link"))
    depends_on("perl-test-exception@0.31:", type=("build", "link"))
    depends_on("perl-test-warn@0.21:", type=("build", "link"))
    depends_on("perl-try-tiny@0.07:", type=("build", "run", "test"))
