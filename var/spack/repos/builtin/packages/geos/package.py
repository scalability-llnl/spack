# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Geos(AutotoolsPackage):
    """GEOS (Geometry Engine - Open Source) is a C++ port of the Java
       Topology Suite (JTS). As such, it aims to contain the complete
       functionality of JTS in C++. This includes all the OpenGIS
       Simple Features for SQL spatial predicate functions and spatial
       operators, as well as specific JTS enhanced topology functions."""

    homepage = "http://trac.osgeo.org/geos/"
    url      = "https://download.osgeo.org/geos/geos-3.8.1.tar.bz2"

    maintainers = ['adamjstewart']

    version('3.8.1', sha256='4258af4308deb9dbb5047379026b4cd9838513627cb943a44e16c40e42ae17f7')
    version('3.7.2', sha256='2166e65be6d612317115bfec07827c11b403c3f303e0a7420a2106bc999d7707')
    version('3.6.2', sha256='045a13df84d605a866602f6020fc6cbf8bf4c42fb50de237a08926e1d7d7652a')
    version('3.6.1', sha256='4a2e4e3a7a09a7cfda3211d0f4a235d9fd3176ddf64bd8db14b4ead266189fc5')
    version('3.6.0', sha256='1fe7644f3240c8422b0143830ff142e44e8b01333c12f67681ccaab92142f2ea')
    version('3.5.1', sha256='e6bb0a7ba0e142b1e952fae9d946b2b532fa05a5c384e458f7cb8990e1fcac32')
    version('3.5.0', sha256='49982b23bcfa64a53333dab136b82e25354edeb806e5a2e2f5b8aa98b1d0ae02')
    version('3.4.3', sha256='cfbf68079117c1c2b76411636444ff41d73c31093c4cab9dcc9a8c1bbe7e3897')
    version('3.4.2', sha256='15e8bfdf7e29087a957b56ac543ea9a80321481cef4d4f63a7b268953ad26c53')
    version('3.4.1', sha256='d07ac375f3edd12425d6ce5a96db9739d5ff358cbdf60c6804f7a9e565af8ff2')
    version('3.4.0', sha256='3b2106d9baeede39d70e22672598d40cb63ee901f54436c774b250726d7bbdd5')
    version('3.3.9', sha256='3e2156165d593f3e85df9ac223170b2c11de3cb4697e4c7a761c3ffbf04fe0ee')
    version('3.3.8', sha256='ebecd4d1a71bcc28e5e883296cd8c52a80d5596335e74728f320989734fa503b')
    version('3.3.7', sha256='fd01c21b54a3c48cac3e7885f26d4ca10ea9944238776b8ce03489e5e45c592b')
    version('3.3.6', sha256='7ee6c1da9a1b87a3e29209e7cddbf19d36f9689d8e44fec2c9bcf6a1b1be3898')
    version('3.3.5', sha256='3b513fbe2d155364d61e76d9c250d6d8e75b5166783a233596c744373cb5874f')
    version('3.3.4', sha256='cd5400aa5f3fe32246dfed5d238c5017e1808162c865c016480b3e6c07271904')
    version('3.3.3', sha256='dfcf4bd70ab212a5b7bad21d01b84748f101a545092b56dafdc3882ef3bddec9')

    # Ruby bindings are fully supported
    variant('ruby',   default=False, description='Enable Ruby support')

    # Since version 3.0, the Python bindings are unsupported
    variant('python', default=False, description='Enable Python support')

    extends('ruby', when='+ruby')
    extends('python', when='+python')

    # Python 3 is supposedly supported, but I couldn't get it to work
    # https://trac.osgeo.org/geos/ticket/774
    depends_on('python@:2', when='@:3.5')

    depends_on('swig', type='build', when='+ruby')
    depends_on('swig', type='build', when='+python')

    # I wasn't able to get the ruby bindings working.
    # It resulted in "Undefined symbols for architecture x86_64".

    def configure_args(self):
        spec = self.spec
        args = []

        if '+ruby' in spec:
            args.append('--enable-ruby')
        else:
            args.append('--disable-ruby')

        if '+python' in spec:
            args.append('--enable-python')
        else:
            args.append('--disable-python')

        return args
