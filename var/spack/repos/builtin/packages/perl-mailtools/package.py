# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMailtools(PerlPackage):
    """Perl module for handling mail"""

    homepage = "https://metacpan.org/release/MailTools"
    url = "https://cpan.metacpan.org/authors/id/M/MA/MARKOV/MailTools-2.21.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.21", sha256="4ad9bd6826b6f03a2727332466b1b7d29890c8d99a32b4b3b0a8d926ee1a44cb")

    depends_on("perl-timedate", type=("build", "run"))
