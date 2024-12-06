# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTestWithoutModule(PerlPackage):
    """Test fallback behaviour in absence of modules"""

    homepage = "https://metacpan.org/pod/Test::Without::Module"
    url = "https://cpan.metacpan.org/authors/id/C/CO/CORION/Test-Without-Module-0.21.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.21", sha256="3cdeafadac4853ebeafe689346d555da5dfa3cfa9d4c84e3e5e7bfee50beec46")
