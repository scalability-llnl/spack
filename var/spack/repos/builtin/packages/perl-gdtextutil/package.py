# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlGdtextutil(PerlPackage):
    """Text utilities for use with GD"""

    homepage = "https://metacpan.org/pod/GD::Text"
    url = "http://search.cpan.org/CPAN/authors/id/M/MV/MVERB/GDTextUtil-0.86.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.86", sha256="886ecbf85cfe94f4135ee5689c4847a9ae783ecb99e6759e12c734f2dd6116bc")

    depends_on("perl-gd", type=("build", "run"))
