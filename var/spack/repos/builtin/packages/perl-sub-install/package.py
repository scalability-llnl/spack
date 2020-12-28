# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSubInstall(PerlPackage):
    """Install subroutines into packages easily"""

    homepage = "http://search.cpan.org/~rjbs/Sub-Install-0.928/lib/Sub/Install.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/R/RJ/RJBS/Sub-Install-0.928.tar.gz"

    version('0.928', sha256='61e567a7679588887b7b86d427bc476ea6d77fffe7e0d17d640f89007d98ef0f')
