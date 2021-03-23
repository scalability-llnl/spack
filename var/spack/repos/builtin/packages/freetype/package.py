# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Freetype(AutotoolsPackage):
    """FreeType is a freely available software library to render fonts.
    It is written in C, designed to be small, efficient, highly customizable,
    and portable while capable of producing high-quality output (glyph images)
    of most vector and bitmap font formats."""

    homepage = "https://www.freetype.org/index.html"
    url      = "https://download.savannah.gnu.org/releases/freetype/freetype-2.10.1.tar.gz"

    version('2.10.4', sha256='5eab795ebb23ac77001cfb68b7d4d50b5d6c7469247b0b01b2c953269f658dac')
    version('2.10.1', sha256='3a60d391fd579440561bf0e7f31af2222bc610ad6ce4d9d7bd2165bca8669110')
    version('2.10.0', sha256='955e17244e9b38adb0c98df66abb50467312e6bb70eac07e49ce6bd1a20e809a')
    version('2.9.1',  sha256='ec391504e55498adceb30baceebd147a6e963f636eb617424bcfc47a169898ce')
    version('2.7.1',  sha256='162ef25aa64480b1189cdb261228e6c5c44f212aac4b4621e28cf2157efb59f5')
    version('2.7',    sha256='7b657d5f872b0ab56461f3bd310bd1c5ec64619bd15f0d8e08282d494d9cfea4')
    version('2.5.3',  sha256='41217f800d3f40d78ef4eb99d6a35fd85235b64f81bc56e4812d7672fca7b806')

    depends_on('libpng')
    depends_on('bzip2')
    depends_on('pkgconfig', type='build')

    conflicts('%intel', when='@2.8:',
              msg='freetype-2.8 and above cannot be built with icc (does not '
              'support __builtin_shuffle)')

    patch('windows.patch', when='@2.9.1')

    @property
    def headers(self):
        headers = find_headers('*', self.prefix.include, recursive=True)
        headers.directories = [self.prefix.include.freetype2]
        return headers

    def configure_args(self):
        args = ['--with-harfbuzz=no']
        if self.spec.satisfies('@2.9.1:'):
            args.append('--enable-freetype-config')
        return args
