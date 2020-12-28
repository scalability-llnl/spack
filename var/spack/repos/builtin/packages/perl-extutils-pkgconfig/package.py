# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExtutilsPkgconfig(PerlPackage):
    """simplistic interface to pkg-config"""

    homepage = "http://search.cpan.org/~xaoc/ExtUtils-PkgConfig-1.16/lib/ExtUtils/PkgConfig.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/X/XA/XAOC/ExtUtils-PkgConfig-1.16.tar.gz"

    version('1.16', sha256='bbeaced995d7d8d10cfc51a3a5a66da41ceb2bc04fedcab50e10e6300e801c6e')

    depends_on('pkgconfig', type=('build', 'run'))
