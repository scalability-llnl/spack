# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExtutilsInstallpaths(PerlPackage):
    """ExtUtils::InstallPaths - Build.PL install path logic made easy"""

    homepage = "https://metacpan.org/pod/ExtUtils::InstallPaths"
    url = "https://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-InstallPaths-0.012.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.013", sha256="65969d3ad8a3a2ea8ef5b4213ed5c2c83961bb5bd12f7ad35128f6bd5b684aa0")
    version("0.012", sha256="84735e3037bab1fdffa3c2508567ad412a785c91599db3c12593a50a1dd434ed")

    depends_on("perl-extutils-config", type=("build", "run"))
