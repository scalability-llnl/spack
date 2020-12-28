# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExtutilsInstallpaths(PerlPackage):
    """ExtUtils::InstallPaths - Build.PL install path logic made easy"""

    homepage = "https://metacpan.org/pod/ExtUtils::InstallPaths"
    url      = "https://cpan.metacpan.org/authors/id/L/LE/LEONT/ExtUtils-InstallPaths-0.012.tar.gz"

    version('0.012', sha256='84735e3037bab1fdffa3c2508567ad412a785c91599db3c12593a50a1dd434ed')
