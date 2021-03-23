# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class SpliceH(AutotoolsPackage):
    """Simple package with one optional dependency"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/splice-h-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    variant('foo', default=False, description='nope')
    variant('bar', default=False, description='nope')
    variant('baz', default=False, description='nope')

    depends_on('splice-z')
    depends_on('splice-z+foo', when='+foo')
