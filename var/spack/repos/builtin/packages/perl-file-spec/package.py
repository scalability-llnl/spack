# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileSpec(PerlPackage):
    """File::Spec - Perl extension for portably performing operations on file names"""

    homepage = "https://metacpan.org/pod/File::Spec"
    url = "https://cpan.metacpan.org/authors/id/K/KW/KWILLIAMS/File-Spec-0.90.tar.gz"

    version("0.90", sha256="695a34604e1b6a98327fe2b374504329735b07c2c45db9f55df1636e4c29bf79")
