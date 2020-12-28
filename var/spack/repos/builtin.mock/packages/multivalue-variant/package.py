# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MultivalueVariant(Package):
    homepage = "http://www.llnl.gov"
    url = "http://www.llnl.gov/mpileaks-1.0.tar.gz"

    version(1.0, 'foobarbaz')
    version(2.1, 'foobarbaz')
    version(2.2, 'foobarbaz')
    version(2.3, 'foobarbaz')

    variant('debug', default=False, description='Debug variant')
    variant(
        'foo', description='Multi-valued variant',
        values=any_combination_of('bar', 'baz', 'barbaz'),
    )

    variant(
        'fee',
        description='Single-valued variant',
        default='bar',
        values=('bar', 'baz', 'barbaz'),
        multi=False
    )

    depends_on('mpi')
    depends_on('callpath')
    depends_on('a')
    depends_on('a@1.0', when='fee=barbaz')
