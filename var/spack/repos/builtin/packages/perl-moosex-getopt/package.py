# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMoosexGetopt(PerlPackage):
    """A Moose role for processing command line options"""

    homepage = "https://metacpan.org/pod/MooseX::Getopt"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/MooseX-Getopt-0.76.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.76", sha256="ff8731bd2b1df83347dfb6afe9ca15c04d2ecd8b288e5793d095eaf956b6b028")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-getopt-long-descriptive@0.088:", type=("build", "run", "test"))
    depends_on("perl-module-build-tiny@0.034:", type=("build"))
    depends_on("perl-module-runtime", type=("build", "test"))
    depends_on("perl-moose", type=("build", "run", "test"))
    depends_on("perl-moosex-role-parameterized@1.01:", type=("build", "run", "test"))
    depends_on("perl-namespace-autoclean", type=("build", "run", "test"))
    depends_on("perl-path-tiny@0.009:", type=("build", "test"))
    depends_on("perl-test-deep", type=("build", "test"))
    depends_on("perl-test-fatal@0.003:", type=("build", "test"))
    depends_on("perl-test-needs", type=("build", "test"))
    depends_on("perl-test-trap", type=("build", "test"))
    depends_on("perl-test-warnings@0.009:", type=("build", "test"))
    depends_on("perl-try-tiny", type=("build", "run", "test"))
