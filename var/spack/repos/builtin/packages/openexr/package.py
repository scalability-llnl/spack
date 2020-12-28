# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openexr(AutotoolsPackage):
    """OpenEXR Graphics Tools (high dynamic-range image file format)"""

    homepage = "http://www.openexr.com/"
    url = "https://github.com/openexr/openexr/releases/download/v2.3.0/openexr-2.3.0.tar.gz"

    # New versions should come from github now
    version('2.3.0', sha256='fd6cb3a87f8c1a233be17b94c74799e6241d50fc5efd4df75c7a4b9cf4e25ea6')

    version('2.2.0', sha256='36a012f6c43213f840ce29a8b182700f6cf6b214bea0d5735594136b44914231',
            url="http://download.savannah.nongnu.org/releases/openexr/openexr-2.2.0.tar.gz")
    version('2.1.0', sha256='54486b454073c1dcb5ae9892cf0f730ffefe62f38176325281505093fd218a14',
            url="http://download.savannah.nongnu.org/releases/openexr/openexr-2.1.0.tar.gz")
    version('2.0.1', sha256='b9924d2f9d57376ff99234209231ad97a47f5cfebd18a5d0570db6d1a220685a',
            url="http://download.savannah.nongnu.org/releases/openexr/openexr-2.0.1.tar.gz")
    version('1.7.0', sha256='b68a2164d01bd028d15bd96af2704634a344e291dc7cc2019a662045d8c52ca4',
            url="http://download.savannah.nongnu.org/releases/openexr/openexr-1.7.0.tar.gz")
    version('1.6.1', sha256='c616906ab958de9c37bb86ca7547cfedbdfbad5e1ca2a4ab98983c9afa6a5950',
            url="http://download.savannah.nongnu.org/releases/openexr/openexr-1.6.1.tar.gz")
    version('1.5.0', sha256='5a745eee4b8ab94cd16f85528c2debfebe6aa1ba23f5b8fc7933d4aa5c3c3416',
            url="http://download.savannah.nongnu.org/releases/openexr/openexr-1.5.0.tar.gz")
    version('1.4.0a', sha256='5d8a7327bd28eeb5d3064640d8eb32c3cd8c5a15999c70b0afa9f8af851936d1',
            url="http://download.savannah.nongnu.org/releases/openexr/openexr-1.4.0a.tar.gz")
    version('1.3.2', sha256='fa08ad904bf89e2968078d25d1d9817f5bc17f372d1bafabf82e8f08ca2adc20',
            url="http://download.savannah.nongnu.org/releases/openexr/openexr-1.3.2.tar.gz")

    variant('debug', default=False,
            description='Builds a debug version of the libraries')

    depends_on('pkgconfig', type='build')
    depends_on('ilmbase')
    depends_on('zlib', type=('build', 'link'))

    def configure_args(self):
        configure_options = []

        configure_options += self.enable_or_disable('debug')

        return configure_options
