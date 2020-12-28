# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class SinglevalueVariant(Package):
    homepage = "http://www.llnl.gov"
    url = "http://www.llnl.gov/mpileaks-1.0.tar.gz"

    version(1.0, 'foobarbaz')

    variant(
        'fum',
        description='Single-valued variant with type in values',
        default='bar',
        values=str,
        multi=False
    )
