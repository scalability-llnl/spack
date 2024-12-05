# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPosixStrftimeCompiler(PerlPackage):
    """GNU C library compatible strftime for loggers and servers"""

    homepage = "https://metacpan.org/pod/POSIX::strftime::Compiler"
    url = "https://cpan.metacpan.org/authors/id/K/KA/KAZEBURO/POSIX-strftime-Compiler-0.46.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.46", sha256="bf88873248ef88cc5e68ed074493496be684ec334e11273d4654306dd9dae485")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-module-build-tiny@0.035:", type=("build"))
