# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTimedate(PerlPackage):
    """The parser contained here will only parse absolute dates, if you want a
    date parser that can parse relative dates then take a look at the Time
    modules by David Muir on CPAN."""

    homepage = "https://metacpan.org/release/TimeDate"
    url      = "https://cpan.metacpan.org/authors/id/G/GB/GBARR/TimeDate-2.30.tar.gz"

    version('2.30', sha256='75bd254871cb5853a6aa0403ac0be270cdd75c9d1b6639f18ecba63c15298e86')
