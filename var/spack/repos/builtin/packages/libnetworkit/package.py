# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libnetworkit(CMakePackage):
    """NetworKit is a growing open-source toolkit for large-scale network
       analysis. Its aim is to provide tools for the analysis of large networks
       in the size range from thousands to billions of edges. For this purpose,
       it implements efficient graph algorithms, many of them parallel to
       utilize multicore architectures. These are meant to compute standard
       measures of network analysis, such as degree sequences, clustering
       coefficients, and centrality measures. In this respect, NetworKit is
       comparable to packages such as NetworkX, albeit with a focus on
       parallelism and scalability."""

    homepage = "https://networkit.github.io/"
    url      = "https://github.com/networkit/networkit/archive/6.1.tar.gz"

    maintainers = ['fabratu']

    version('8.1', sha256='0a22eb839606b9fabfa68c7add12c4de5eee735c6f8bb34420e5916ce5d7f829')
    version('8.0', sha256='cdf9571043edbe76c447622ed33efe9cba2880f887ca231d98f6d3c22027e20e')
    version('7.1', sha256='60026c3be581ae9d5c919c861605082fcb9c8205758b3ddfcde2408153ae166e')
    version('7.0', sha256='4faf16c5fae3e14d3c1b6f30e25c6e093dcf6a3dbf021235f3161ac2a527f682')
    version('6.1', sha256='22c953ea1054c356663b31c77114c2f0c8fec17e0e707aeec23026241beab9b2')

    variant('static', default=False, description='Enables the build of shared libraries')
    variant('doc', default=False, description='Enables the build with sphinx documentation')

    depends_on('libtlx')
    depends_on('py-sphinx', when='+doc', type='build')

    patch('0001-Name-agnostic-import-of-tlx-library.patch', when='@6.1:')

    def cmake_args(self):
        spec = self.spec

        tlx_libs = spec['libtlx'].prefix

        args = ['-DNETWORKIT_EXT_TLX=%s' % tlx_libs,
                '-DNETWORKIT_STATIC=%s' %
                ('ON' if '+static' in spec else 'OFF')]

        return args
