# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ffmpeg(AutotoolsPackage):
    """FFmpeg is a complete, cross-platform solution to record,
    convert and stream audio and video."""

    homepage = "https://ffmpeg.org"
    url      = "http://ffmpeg.org/releases/ffmpeg-4.1.1.tar.bz2"

    maintainers = ['xjrc']

    version('4.2.2',  sha256='b620d187c26f76ca19e74210a0336c3b8380b97730df5cdf45f3e69e89000e5c')
    version('4.1.1',  sha256='0cb40e3b8acaccd0ecb38aa863f66f0c6e02406246556c2992f67bf650fab058')
    version('4.1',    sha256='b684fb43244a5c4caae652af9022ed5d85ce15210835bce054a33fb26033a1a5')
    version('3.2.4',  sha256='c0fa3593a2e9e96ace3c1757900094437ad96d1d6ca19f057c378b5f394496a4')
    version('2.8.15', sha256='35647f6c1f6d4a1719bc20b76bf4c26e4ccd665f46b5676c0e91c5a04622ee21')
    version('1.0.10', sha256='1dbde434c3b5c573d3b2ffc1babe3814f781c10c4bc66193a4132a44c9715176')

    # Licensing
    variant('gpl', default=True,
            description='allow use of GPL code, the resulting libs '
            'and binaries will be under GPL')
    variant('version3', default=True,
            description='upgrade (L)GPL to version 3')
    variant('nonfree', default=False,
            description='allow use of nonfree code, the resulting libs '
            'and binaries will be unredistributable')

    # NOTE: The libopencv option creates a circular dependency.
    # NOTE: There are more possible variants that would require additional
    # spack packages.

    # meta variants: These will toggle several settings
    variant('X', default=False, description='X11 support')
    variant('drawtext', default=False, description='drawtext filter')

    # options
    variant('bzlib', default=True, description='bzip2 support')
    variant('libaom', default=False, description='AV1 video encoding/decoding')
    variant('libmp3lame', default=False, description='MP3 encoding')
    variant('libopenjpeg', default=False, description='JPEG 2000 de/encoding')
    variant('libopus', default=False, description='Opus de/encoding')
    variant('libsnappy', default=False,
            description='Snappy compression, needed for hap encoding')
    variant('libspeex', default=False, description='Speex de/encoding')
    variant('libssh', default=False, description='SFTP protocol')
    variant('libvorbis', default=False, description='Vorbis en/decoding')
    variant('libwebp', default=False, description='WebP encoding via libwebp')
    # TODO: There is an issue with the spack headers property in the libxml2
    # package recipe. Comment out the libxml2 variant until that is resolved.
    # variant('libxml2', default=False,
    #         description='XML parsing, needed for dash demuxing support')
    variant('libzmq', default=False, description='message passing via libzmq')
    variant('lzma', default=False, description='lzma support')
    variant('avresample', default=False, description='AV reasmpling component')
    variant('openssl', default=False, description='needed for https support')
    variant('sdl2', default=False, description='sdl2 support')
    variant('shared', default=True, description='build shared libraries')

    depends_on('alsa-lib', when='platform=linux')
    depends_on('libiconv')
    depends_on('yasm@1.2.0:')
    depends_on('zlib')

    depends_on('aom', when='+libaom')
    depends_on('bzip2', when='+bzlib')
    depends_on('fontconfig', when='+drawtext')
    depends_on('freetype', when='+drawtext')
    depends_on('fribidi', when='+drawtext')
    depends_on('lame', when='+libmp3lame')
    depends_on('libssh', when='+libssh')
    depends_on('libvorbis', when='+libvorbis')
    depends_on('libwebp', when='+libwebp')
    # TODO: enable libxml2 when libxml2 header issue is resolved
    # depends_on('libxml2', when='+libxml2')
    depends_on('libxv', when='+X')
    depends_on('libzmq', when='+libzmq')
    depends_on('openjpeg', when='+libopenjpeg')
    depends_on('openssl', when='+openssl')
    depends_on('opus', when='+libopus')
    depends_on('sdl2', when='+sdl2')
    depends_on('snappy', when='+libsnappy')
    depends_on('speex', when='+libspeex')
    depends_on('xz', when='+lzma')

    # TODO: enable when libxml2 header issue is resolved
    # conflicts('+libxml2', when='@:3.999')
    # See: https://www.ffmpeg.org/index.html#news (search AV1)
    conflicts('+libaom', when='@:3.999')
    # All of the following constraints were sourced from the official 'ffmpeg'
    # change log, which can be found here:
    # https://raw.githubusercontent.com/FFmpeg/FFmpeg/release/4.0/Changelog
    conflicts('+sdl2', when='@:3.1.999')
    conflicts('+libsnappy', when='@:2.7.999')
    conflicts('+X', when='@:2.4.999')
    conflicts('+lzma', when='@2.3.999:')
    conflicts('+libwebp', when='@2.1.999:')
    conflicts('+libssh', when='@2.0.999:')
    conflicts('+libzmq', when='@:1.999.999')
    conflicts('%nvhpc')

    @property
    def libs(self):
        return find_libraries('*', self.prefix, recursive=True)

    @property
    def headers(self):
        headers = find_all_headers(self.prefix.include)
        headers.directories = [self.prefix.include]
        return headers

    def enable_or_disable_meta(self, variant, options):
        switch = 'enable' if '+{0}'.format(variant) in self.spec else 'disable'
        return ['--{0}-{1}'.format(switch, option) for option in options]

    def configure_args(self):
        spec = self.spec
        config_args = [
            '--enable-pic',
            '--cc={0}'.format(spack_cc),
            '--cxx={0}'.format(spack_cxx)
        ]

        # '+X' meta variant #

        xlib_opts = []

        if spec.satisfies('@2.5:'):
            xlib_opts.extend([
                'libxcb',
                'libxcb-shape',
                'libxcb-shm',
                'libxcb-xfixes',
                'xlib',
            ])

        config_args += self.enable_or_disable_meta('X', xlib_opts)

        # '+drawtext' meta variant #

        drawtext_opts = [
            '{0}fontconfig'.format('lib' if spec.satisfies('@3:') else ''),
            'libfreetype',
        ]

        if spec.satisfies('@2.3:'):
            drawtext_opts.append('libfribidi')

        config_args += self.enable_or_disable_meta('drawtext', drawtext_opts)

        # other variants #

        variant_opts = [
            'bzlib',
            'libmp3lame',
            'libopenjpeg',
            'libopus',
            'libspeex',
            'libvorbis',
            'avresample',
            'openssl',
            'shared',
        ]

        if spec.satisfies('@2.0:'):
            variant_opts.append('libzmq')
        if spec.satisfies('@2.1:'):
            variant_opts.append('libssh')
        if spec.satisfies('@2.2:'):
            variant_opts.append('libwebp')
        if spec.satisfies('@2.4:'):
            variant_opts.append('lzma')
        if spec.satisfies('@2.8:'):
            variant_opts.append('libsnappy')
        if spec.satisfies('@3.2:'):
            variant_opts.append('sdl2')
        if spec.satisfies('@4:'):
            variant_opts.append('libaom')
            # TODO: enable when libxml2 header issue is resolved
            # variant_opts.append('libxml2')

        for variant_opt in variant_opts:
            config_args += self.enable_or_disable(variant_opt)

        return config_args
