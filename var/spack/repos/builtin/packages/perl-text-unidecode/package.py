# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTextUnidecode(PerlPackage):
    """plain ASCII transliterations of Unicode text"""

    homepage = "https://metacpan.org/pod/Text::Unidecode"
    url = "http://search.cpan.org/CPAN/authors/id/S/SB/SBURKE/Text-Unidecode-1.30.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.30", sha256="6c24f14ddc1d20e26161c207b73ca184eed2ef57f08b5fb2ee196e6e2e88b1c6")
