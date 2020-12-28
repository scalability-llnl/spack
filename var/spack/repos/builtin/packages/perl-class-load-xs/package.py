# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlClassLoadXs(PerlPackage):
    """This module provides an XS implementation for portions of
       Class::Load."""

    homepage = "http://search.cpan.org/~ether/Class-Load-XS-0.10/lib/Class/Load/XS.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/E/ET/ETHER/Class-Load-XS-0.10.tar.gz"

    version('0.10', sha256='5bc22cf536ebfd2564c5bdaf42f0d8a4cee3d1930fc8b44b7d4a42038622add1')

    depends_on('perl-class-load', type=('build', 'run'))
