# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDataOptlist(PerlPackage):
    """Parse and validate simple name/value option pairs"""

    homepage = "https://metacpan.org/pod/Data::OptList"
    url = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Data-OptList-0.110.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.114", sha256="9fd1093b917a21fb79ae1607db53d113b4e0ad8fe0ae776cb077a7e50044fdf3")
    version("0.113", sha256="36aebc5817b7d4686b649434c2ee41f45c8bf97d4ca5a99f607cc40f695a4285")
    version("0.110", sha256="366117cb2966473f2559f2f4575ff6ae69e84c69a0f30a0773e1b51a457ef5c3")

    depends_on("perl-sub-install", type=("build", "run"))
    depends_on("perl-extutils-makemaker@6.78:", when="@0.113:", type=("build", "run"))
