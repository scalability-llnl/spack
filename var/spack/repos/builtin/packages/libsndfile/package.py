# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsndfile(AutotoolsPackage):
    """Libsndfile is a C library for reading and writing files containing
    sampled sound (such as MS Windows WAV and the Apple/SGI AIFF format)
    through one standard library interface. It is released in source code
    format under the Gnu Lesser General Public License."""

    homepage = "http://www.mega-nerd.com/libsndfile/"
    url      = "http://www.mega-nerd.com/libsndfile/files/libsndfile-1.0.28.tar.gz"

    version('1.0.28', sha256='1ff33929f042fa333aed1e8923aa628c3ee9e1eb85512686c55092d1e5a9dfa9')

    variant('alsa', default=False, description='Use alsa in example programs')
    variant('external-libs',
            default=False,
            description='Build with support for FLAC, Ogg and Vorbis')
    variant('sqlite', default=False, description='Build with sqlite support')

    depends_on('pkgconfig', type='build')
    depends_on('alsa-lib', when='+alsa')
    depends_on('flac@1.3.1:', when='+external-libs')
    depends_on('libogg@1.1.3:', when='+external-libs')
    depends_on('libvorbis@1.2.3:', when='+external-libs')
    depends_on('sqlite@3.2:', when='+sqlite')

    def configure_args(self):
        args = []

        args += self.enable_or_disable('alsa')
        args += self.enable_or_disable('external-libs')
        args += self.enable_or_disable('sqlite')

        return args
