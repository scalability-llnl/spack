# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDevelCycle(PerlPackage):
    """Find memory cycles in objects"""

    homepage = "https://metacpan.org/pod/Devel::Cycle"
    url = "http://search.cpan.org/CPAN/authors/id/L/LD/LDS/Devel-Cycle-1.12.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.12", sha256="fd3365c4d898b2b2bddbb78a46d507a18cca8490a290199547dab7f1e7390bc2")
