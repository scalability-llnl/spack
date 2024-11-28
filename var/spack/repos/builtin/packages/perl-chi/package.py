# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlChi(PerlPackage):
    """Unified cache handling interface"""

    homepage = "https://metacpan.org/pod/CHI"
    url = "https://cpan.metacpan.org/authors/id/A/AS/ASB/CHI-0.61.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.61", sha256="583545c9e5312bb4193ab16de9f55ff8f4b4a7ded128cee8dd2cb021d4678b5b")

    depends_on("perl-cache-cache", type=("build", "run", "test"))
    depends_on("perl-carp-assert@0.20:", type=("build", "run", "test"))
    depends_on("perl-class-load", type=("build", "run", "test"))
    depends_on("perl-data-uuid", type=("build", "run", "test"))
    depends_on("perl-digest-jhash", type=("build", "run", "test"))
    depends_on("perl-hash-moreutils", type=("build", "run", "test"))
    depends_on("perl-json-maybexs@1.003003:", type=("build", "run", "test"))
    depends_on("perl-list-moreutils@0.13:", type=("build", "run", "test"))
    depends_on("perl-log-any@0.08:", type=("build", "run", "test"))
    depends_on("perl-module-mask", type=("build", "run", "test"))
    depends_on("perl-moo@1.003:", type=("build", "run", "test"))
    depends_on("perl-moox-types-mooselike@0.23:", type=("build", "run", "test"))
    depends_on("perl-moox-types-mooselike-numeric", type=("build", "run", "test"))
    depends_on("perl-string-rewriteprefix", type=("build", "run", "test"))
    depends_on("perl-task-weaken", type=("build", "run", "test"))
    depends_on("perl-test-class", type=("build", "run", "test"))
    depends_on("perl-test-deep", type=("build", "run", "test"))
    depends_on("perl-test-exception", type=("build", "run", "test"))
    depends_on("perl-test-warn", type=("build", "run", "test"))
    depends_on("perl-time-duration@1.06:", type=("build", "run", "test"))
    depends_on("perl-time-duration-parse@0.03:", type=("build", "run", "test"))
    depends_on("perl-timedate", type=("build", "run", "test"))
    depends_on("perl-try-tiny@0.05:", type=("build", "run", "test"))
