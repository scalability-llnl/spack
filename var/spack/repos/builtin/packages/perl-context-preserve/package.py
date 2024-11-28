# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlContextPreserve(PerlPackage):
    """Run code after a subroutine call, preserving the context the subroutine
    would have seen if it were the last statement in the caller"""

    homepage = "https://metacpan.org/pod/Context::Preserve"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/Context-Preserve-0.03.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.03", sha256="09914a4c2c7bdb99cab680c183cbf492ec98d6e23fbcc487fcc4ae10567dfd1f")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-test-exception", type=("build", "test"))
