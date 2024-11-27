# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSubInstall(PerlPackage):
    """Install subroutines into packages easily"""

    homepage = "https://metacpan.org/pod/Sub::Install"
    url = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Sub-Install-0.928.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.929", sha256="80b1e281d8cd3b2b31dac711f5c8a1657a87cd80bbe69af3924bcbeb4e5db077")
    version("0.928", sha256="61e567a7679588887b7b86d427bc476ea6d77fffe7e0d17d640f89007d98ef0f")
