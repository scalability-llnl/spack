# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileSlurp(PerlPackage):
    """File::Slurp - Simple and Efficient Reading/Writing/Modifying of Complete
    Files"""

    homepage = "https://metacpan.org/pod/File::Slurp"
    url = "https://cpan.metacpan.org/authors/id/C/CA/CAPOEIRAB/File-Slurp-9999.32.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("9999.32", sha256="4c3c21992a9d42be3a79dd74a3c83d27d38057269d65509a2f555ea0fb2bc5b0")
