# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlListCompare(PerlPackage):
    """Compare elements of two or more lists"""

    homepage = "https://metacpan.org/pod/List::Compare"
    url = "https://cpan.metacpan.org/authors/id/J/JK/JKEENAN/List-Compare-0.55.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.55", sha256="cc719479836579d52b02bc328ed80a98f679df043a99b5710ab2c191669eb837")

    depends_on("perl-capture-tiny", type=("build", "test"))
