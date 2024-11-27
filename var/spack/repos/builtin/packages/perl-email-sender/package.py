# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlEmailSender(PerlPackage):
    """A library for sending email"""

    homepage = "https://metacpan.org/pod/Email::Sender"
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Email-Sender-2.600.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("2.600", sha256="ecc675d030d79d9a4fb064567ea885c66b17c3862379ad30f8205a281cd8ee29")

    depends_on("perl@5.12.0:", type=("build", "link", "run", "test"))
    depends_on("perl-capture-tiny@0.08:", type=("build", "test"))
    depends_on("perl-email-abstract@3.006:", type=("build", "run", "test"))
    depends_on("perl-email-address-xs", type=("build", "run", "test"))
    depends_on("perl-email-simple@1.998:", type=("build", "run", "test"))
    depends_on("perl-module-runtime", type=("build", "run", "test"))
    depends_on("perl-moo@2.000000:", type=("build", "run", "test"))
    depends_on("perl-moox-types-mooselike@0.15:", type=("build", "run", "test"))
    depends_on("perl-sub-exporter", type=("build", "run", "test"))
    depends_on("perl-throwable", type=("build", "run", "test"))
    depends_on("perl-try-tiny", type=("build", "run", "test"))
