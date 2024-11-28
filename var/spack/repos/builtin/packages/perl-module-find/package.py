# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleFind(PerlPackage):
    """Find and use installed modules in a (sub)category"""

    homepage = "https://metacpan.org/pod/Module::Find"
    url = "https://cpan.metacpan.org/authors/id/C/CR/CRENZ/Module-Find-0.16.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.16", sha256="4bcaaa376915014728d4f533a98c5b59d665051cd3cdbafc960e5a66fd131092")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
