# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPerlCritic(PerlPackage):
    """Critique Perl source code for best-practices."""

    homepage = "https://metacpan.org/pod/Perl::Critic"
    url = "https://cpan.metacpan.org/authors/id/P/PE/PETDANCE/Perl-Critic-1.152.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.152", sha256="e5bfaf67f61a2a6a0ed343f0403b19f515b4890eed6272abaab707749c5e5e1e")

    depends_on("perl@5.10.1:", type=("build", "link", "run", "test"))
    depends_on("perl-b-keywords@1.23:", type=("build", "run", "test"))
    depends_on("perl-config-tiny@2:", type=("build", "run", "test"))
    depends_on("perl-exception-class@1.23:", type=("build", "run", "test"))
    depends_on("perl-file-which", type=("build", "run", "test"))
    depends_on("perl-list-someutils@0.55:", type=("build", "run", "test"))
    depends_on("perl-module-pluggable@3.1:", type=("build", "run", "test"))
    depends_on("perl-perl-tidy", type=("build", "run", "test"))
    depends_on("perl-pod-parser", type=("build", "run", "test"))
    depends_on("perl-pod-spell@1:", type=("build", "run", "test"))
    depends_on("perl-ppi@1.277:", type=("build", "run", "test"))
    depends_on("perl-ppix-quotelike", type=("build", "run", "test"))
    depends_on("perl-ppix-regexp@0.027:", type=("build", "run", "test"))
    depends_on("perl-ppix-utils", type=("build", "run", "test"))
    depends_on("perl-readonly@2:", type=("build", "run", "test"))
    depends_on("perl-string-format@1.18:", type=("build", "run", "test"))
