# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTermAnsicolorMarkup(PerlPackage):
    """Colorize tagged strings for screen output"""

    homepage = "https://metacpan.org/pod/Term::ANSIColor::Markup"
    url = "https://cpan.metacpan.org/authors/id/K/KE/KENTARO/Term-ANSIColor-Markup-0.06.tar.gz"

    maintainers("EbiArnie")

    license("MIT")

    version("0.06", sha256="66f1c2f2f403fdaae0902b36202d57356b6b5b5a57b3cca8d0248ffbe78c753f")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-class-accessor-lvalue", type=("build", "run", "test"))
    depends_on("perl-html-parser", type=("build", "run", "test"))
    depends_on("perl-test-exception", type=("build", "link"))
    depends_on("perl-module-install", type=("build", "link"))
