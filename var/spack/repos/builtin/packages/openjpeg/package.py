# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openjpeg(CMakePackage):
    """OpenJPEG is an open-source JPEG 2000 codec written in C language.

    It has been developed in order to promote the use of JPEG 2000, a
    still-image compression standard from the Joint Photographic
    Experts Group (JPEG).
    Since April 2015, it is officially recognized by ISO/IEC and
    ITU-T as a JPEG 2000 Reference Software.
    """

    homepage = 'https://github.com/uclouvain/openjpeg'
    url = 'https://github.com/uclouvain/openjpeg/archive/v2.3.1.tar.gz'

    version('2.3.1', sha256='63f5a4713ecafc86de51bfad89cc07bb788e9bba24ebbf0c4ca637621aadb6a9')
    version('2.3.0', sha256='3dc787c1bb6023ba846c2a0d9b1f6e179f1cd255172bde9eb75b01f1e6c7d71a')
    version('2.2.0', sha256='6fddbce5a618e910e03ad00d66e7fcd09cc6ee307ce69932666d54c73b7c6e7b')
    version('2.1.2', sha256='4ce77b6ef538ef090d9bde1d5eeff8b3069ab56c4906f083475517c2c023dfa7')
    version('2.1.1', sha256='82c27f47fc7219e2ed5537ac69545bf15ed8c6ba8e6e1e529f89f7356506dbaa')
    version('2.1.0', sha256='4afc996cd5e0d16360d71c58216950bcb4ce29a3272360eb29cadb1c8bce4efc')
    version('2.0.1', sha256='f184d402a218359184fd162075bb5246a68165b9776678185b6a379c49093816')
    version('2.0.0', sha256='5480f801a9f88af1a456145e41f3adede1dfae425bbac66a19c7eeeba94a1249')
    version('1.5.2', sha256='3734e95edd0bef6e056815591755efd822228dc3cd866894e00a2c929026b16d')
    version('1.5.1', sha256='6a42fcc23cb179f69a1e94429089e5a5926aee1ffe582a0a6bd91299d297e61a')

    depends_on('zlib')

    # The problem with install name of the library on MacOs was fixed starting
    # version 2.1.1: https://github.com/uclouvain/openjpeg/commit/b9a247b559e62e55f5561624cf4a19aee3c8afdc
    # The solution works for the older versions (at least starting 1.5.1) too.
    patch('macos.patch', when='@:2.1.0 platform=darwin')

    def url_for_version(self, version):
        if version >= Version('2.1.1'):
            return super(Openjpeg, self).url_for_version(version)

        # Before version 2.2.0, release tarballs of the versions like x.y.0
        # did not have the ".0" in their names:
        if version[2] == 0:
            version = version.up_to(2)

        url_fmt = \
            'https://github.com/uclouvain/openjpeg/archive/version.{0}.tar.gz'

        return url_fmt.format(version)

    @property
    def libs(self):
        return find_libraries('libopenjp{0}'.format(self.version.up_to(1)),
                              root=self.prefix, recursive=True)
