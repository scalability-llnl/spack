# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlScopeGuard(PerlPackage):
    """Lexically-scoped resource management"""

    homepage = "https://metacpan.org/pod/Scope::Guard"
    url = "https://cpan.metacpan.org/authors/id/C/CH/CHOCOLATE/Scope-Guard-0.21.tar.gz"

    maintainers("EbiArnie")

    version("0.21", sha256="8c9b1bea5c56448e2c3fadc65d05be9e4690a3823a80f39d2f10fdd8f777d278")

    depends_on("perl@5.6.1:", type=("build", "link", "run", "test"))
