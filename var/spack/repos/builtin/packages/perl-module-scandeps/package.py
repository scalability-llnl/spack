# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlModuleScandeps(PerlPackage):
    """Module::ScanDeps - Recursively scan Perl code for dependencies"""

    homepage = "https://metacpan.org/pod/Module::ScanDeps"
    url = "https://cpan.metacpan.org/authors/id/R/RS/RSCHUPP/Module-ScanDeps-1.31.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.31", sha256="fc4d98d2b0015745f3b55b51ddf4445a73b069ad0cb7ec36d8ea781d61074d9d")
