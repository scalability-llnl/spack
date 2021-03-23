# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Ns3Dev(WafPackage):
    """
    ns-3 is a discrete-event network simulator,
    targeted primarily for research and educational use
    """

    homepage = "https://www.nsnam.org/"
    url      = "https://gitlab.com/nsnam/ns-3-dev/-/archive/ns-3.30.1/ns-3-dev-ns-3.30.1.tar.bz2"

    maintainers = ['yee29']

    version('3.30.1', sha256='e8b3849d83a224f42c0cd2b9e692ec961455aca23f36fb86fcf6bbed2b495a3d')
    version('3.30',   sha256='53cefcad74fec6cc332368a05ed1f8c1a29f86295cb44b6b0509c6d2d18d90d0')
    version('3.29',   sha256='0254341487891421e4c6040476c6634c4c2931d4f7c6b9617a6ae494c8ee6ffd')
    version('3.28',   sha256='5295e1f6e2ee1ff8cd92d3937c8b3266e0d5926adffc42c7fb0ea9ce549a91b7')
    version('3.27',   sha256='26233011654043822b8ede525a52f8532ed181997b609a606681a0d5c8d64a26')

    variant('helics', default=False, description="Enable Helics support in ns-3")
    variant('boost', default=True, description="Compile with Boost libraries")

    # Build dependency
    depends_on('helics', when='+helics')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when='+boost')
    depends_on('pkgconfig', type='build')

    resource(name='helics',
             when='+helics',
             git='https://github.com/GMLC-TDC/helics-ns3.git',
             destination='contrib', placement='helics')

    def configure_args(self):
        args = []

        if '+boost' in self.spec:
            args.extend([
                '--boost-includes={0}'.format(
                    self.spec['boost'].prefix.include),
                '--boost-libs={0}'.format(
                    self.spec['boost'].prefix.lib)
            ])

        if '+helics' in self.spec:
            args.append('--with-helics={0}'.format(self.spec['helics'].prefix))
        return args
