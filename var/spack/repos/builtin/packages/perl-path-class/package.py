# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPathClass(PerlPackage):
    """Cross-platform path specification manipulation"""

    homepage = "https://metacpan.org/pod/Path::Class"
    url = "https://cpan.metacpan.org/authors/id/K/KW/KWILLIAMS/Path-Class-0.37.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.37", sha256="654781948602386f2cb2e4473a739f17dc6953d92aabc2498a4ca2561bc248ce")
