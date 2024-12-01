# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileCopyRecursive(PerlPackage):
    """Perl extension for recursively copying files and directories"""

    homepage = "https://metacpan.org/pod/File::Copy::Recursive"
    url = "http://search.cpan.org/CPAN/authors/id/D/DM/DMUEY/File-Copy-Recursive-0.38.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.45", sha256="d3971cf78a8345e38042b208bb7b39cb695080386af629f4a04ffd6549df1157")
    version("0.40", sha256="e8b8923b930ef7bcb59d4a97456d0e149b8487597cd1550f836451d936ce55a1")
    version("0.38", sha256="84ccbddf3894a88a2c2b6be68ff6ef8960037803bb36aa228b31944cfdf6deeb")
