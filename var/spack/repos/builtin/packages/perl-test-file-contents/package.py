# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestFileContents(PerlPackage):
    """Test routines for examining the contents of files"""

    homepage = "https://metacpan.org/pod/Test::File::Contents"
    url = "https://cpan.metacpan.org/authors/id/A/AR/ARISTOTLE/Test-File-Contents-0.242.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.242", sha256="a838ac0b6f6e10e89613b50ca61773cdba9ba4787ba82e7bb65daaf7084aa50b")

    depends_on("perl@5.8.3:", type=("build", "link", "run", "test"))
    depends_on("perl-text-diff@0.35:", type=("build", "run", "test"))
