# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlExtutilsMakemaker(PerlPackage):
    """ExtUtils::MakeMaker - Create a module Makefile. This utility is designed
    to write a Makefile for an extension module from a Makefile.PL. It is based
    on the Makefile.SH model provided by Andy Dougherty and the perl5-porters.
    """
    homepage = "https://github.com/Perl-Toolchain-Gang/ExtUtils-MakeMaker"
    url      = "http://search.cpan.org/CPAN/authors/id/B/BI/BINGOS/ExtUtils-MakeMaker-7.24.tar.gz"

    version('7.24', sha256='416abc97c3bb2cc72bef28852522f2859de53e37bf3d0ae8b292067d78755e69')

    depends_on('perl@5.6.0:', type=('build', 'run'))
