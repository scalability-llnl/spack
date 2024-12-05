# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlApacheLogformatCompiler(PerlPackage):
    """Compile a log format string to perl-code"""

    homepage = "https://metacpan.org/pod/Apache::LogFormat::Compiler"
    url = (
        "https://cpan.metacpan.org/authors/id/K/KA/KAZEBURO/Apache-LogFormat-Compiler-0.36.tar.gz"
    )

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.36", sha256="94509503ee74ea820183d070c11630ee5bc0fd8c12cb74fae953ed62e4a1ac17")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-http-message", type=("build", "test"))
    depends_on("perl-module-build-tiny@0.035:", type=("build"))
    depends_on("perl-posix-strftime-compiler@0.30:", type=("build", "run", "test"))
    depends_on("perl-test-mocktime", type=("build", "test"))
    depends_on("perl-test-requires", type=("build", "test"))
    depends_on("perl-try-tiny@0.12:", type=("build", "test"))
    depends_on("perl-uri", type=("build", "test"))
