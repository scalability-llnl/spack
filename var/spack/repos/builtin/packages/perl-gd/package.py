# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlGd(PerlPackage):
    """Interface to Gd Graphics Library"""

    homepage = "http://search.cpan.org/~lds/GD-2.53/GD.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/L/LD/LDS/GD-2.53.tar.gz"

    version('2.53', sha256='d05d01fe95e581adb3468cf05ab5d405db7497c0fb3ec7ecf23d023705fab7aa')

    depends_on('perl-module-build', type='build')
    depends_on('perl-extutils-makemaker', type=('build', 'run'))
    depends_on('perl-extutils-pkgconfig', type=('build', 'run'))
    depends_on('libgd')
