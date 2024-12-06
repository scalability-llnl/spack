# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlEmailStuffer(PerlPackage):
    """A more casual approach to creating and sending Email:: emails"""

    homepage = "https://metacpan.org/pod/Email::Stuffer"
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Email-Stuffer-0.020.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.020", sha256="0a1efb7f2dedd39052b126f718ca2d3b5845a4123a39392fd9dfa0c76e6057c7")

    depends_on("perl@5.12.0:", type=("build", "link", "run", "test"))
    depends_on("perl-email-mime@1.943:", type=("build", "run", "test"))
    depends_on("perl-email-sender", type=("build", "run", "test"))
    depends_on("perl-module-runtime", type=("build", "run", "test"))
    depends_on("perl-moo", type=("build", "test"))
    depends_on("perl-params-util@1.05:", type=("build", "run", "test"))
    depends_on("perl-test-fatal", type=("build", "test"))
