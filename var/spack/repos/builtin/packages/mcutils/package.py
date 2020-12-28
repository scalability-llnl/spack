# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mcutils(MakefilePackage):
    """A collection of routines for classification and manipulation of
       particle physics simulated HepMC event records."""

    homepage = "https://bitbucket.org/andybuckley/mcutils"
    url      = "https://bitbucket.org/andybuckley/mcutils/get/mcutils-1.3.4.tar.gz"

    tags = ['hep']

    version('1.3.4', sha256='0bf9795cc248871ab2b663d2eef647311eacaea4982997950096de68747e65a3')
    version('1.3.3', sha256='bfb2f0e0e6de358928436f309f3f1b084d3d652073c440f262de878332116ecb')
    version('1.3.2', sha256='e17d417e8d4f8d17a6879ea18dcd2cd76e161d37eae08b84893504d1b08f9708')
    version('1.3.1', sha256='081263ee6844fccedad780e6a2fbaf1ad0073a6706bc4b34109050b72c2c4b27')
    version('1.3.0', sha256='20a89ce536547dc8f56e7779a3ec8cfe9987edb1646009ecfc682ff1ddf0277b')
    version('1.2.1', sha256='004325be41925d97e711ffe4311d9c8aa8e88873541bcc1a385d2e1ce1d17a96')
    version('1.2.0', sha256='f9589d45bff06d8c8742d35d78d1ed570a0d181fd7ee5d6f97ab9e48f0ee32f4')
    version('1.1.2', sha256='5a5781caf2d81c21f4b040a1d31975c354526bcf7c8c9067543f7303c8155844')
    version('1.1.1', sha256='3e5c47d2264886613fc9423b020cf50dc7031a02b752da3a84f794c36ba7443a')
    version('1.1.0', sha256='96fc2586430032ed4b378edb02150c5c9db405e1767dbf847ffe9ac043daf6e9')
    version('1.0.3', sha256='b5bec5a4b2146b6987b351d632119c3b4c449c2ee53ae0ddc8cb1d3672907df5')
    version('1.0.2', sha256='74e2c381f5f3719888b15a2e00075051bb2b84b3d73633d429818a77de66ca7c')
    version('1.0.1', sha256='bb884a4cfb56b5139c08df0be554466e504e9c46096a858f904d659894a62131')
    version('1.0.0', sha256='d08dea19fb42b1846e0a7134e2347648b037bf82b2d75086d018734bc2996b06')

    depends_on('heputils', when='@1.1.0:')

    def install(self, spec, prefix):
        make('install', 'PREFIX={0}'.format(prefix))
