# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Glvis(MakefilePackage):
    """GLVis: an OpenGL tool for visualization of FEM meshes and functions"""

    homepage = "http://glvis.org"
    git      = "https://github.com/glvis/glvis.git"

    maintainers = ['goxberry', 'v-dobrev', 'tzanio']

    # glvis (like mfem) is downloaded from a URL shortener at request
    # of upstream author Tzanio Kolev <tzanio@llnl.gov>.  See here:
    # https://github.com/mfem/mfem/issues/53
    #
    # The following procedure should be used to verify security when a
    # new version is added:
    #
    # 1. Verify that no checksums on old versions have changed.
    #
    # 2. Verify that the shortened URL for the new version is listed at:
    #    http://glvis.org/download/
    #
    # 3. Use http://getlinkinfo.com or similar to verify that the
    #    underling download link for the latest version comes has the
    #    prefix: http://glvis.github.io/releases
    #
    # If this quick verification procedure fails, additional discussion
    # will be required to verify the new version.

    version('develop', branch='master')

    version('3.4',
            sha256='289fbd2e09d4456e5fee6162bdc3e0b4c8c8d54625f3547ad2a69fef319279e7',
            url='https://bit.ly/glvis-3-4',
            extension='.tar.gz')

    version('3.3',
            sha256='e24d7c5cb53f208b691c872fe82ea898242cfdc0fd68dd0579c739e070dcd800',
            url='http://goo.gl/C0Oadw',
            extension='.tar.gz')

    version('3.2',
            sha256='c82cb110396e63b6436a770c55eb6d578441eaeaf3f9cc20436c242392e44e80',
            url='http://goo.gl/hzupg1',
            extension='.tar.gz')

    version('3.1',
            sha256='793e984ddfbf825dcd13dfe1ca00eccd686cd40ad30c8789ba80ee175a1b488c',
            url='http://goo.gl/gQZuu9',
            extension='tar.gz')

    variant('screenshots',
            default='png',
            values=('xwd', 'png', 'tiff'),
            description='Backend used for screenshots')
    variant('fonts', default=True,
            description='Use antialiased fonts via freetype & fontconfig')

    depends_on('mfem@develop', when='@develop')
    depends_on('mfem@3.4.0', when='@3.4')
    depends_on('mfem@3.3', when='@3.3')
    depends_on('mfem@3.2', when='@3.2')
    depends_on('mfem@3.1', when='@3.1')

    depends_on('gl')
    depends_on('glu')
    depends_on('libx11')

    depends_on('libpng', when='screenshots=png')
    depends_on('libtiff', when='screenshots=tiff')
    depends_on('freetype', when='+fonts')
    depends_on('fontconfig', when='+fonts')

    def edit(self, spec, prefix):

        def yes_no(s):
            return 'YES' if self.spec.satisfies(s) else 'NO'

        mfem = spec['mfem']
        config_mk = mfem.package.config_mk

        gl_libs = spec['glu'].libs + spec['gl'].libs + spec['libx11'].libs
        args = ['CC={0}'.format(env['CC']),
                'PREFIX={0}'.format(prefix.bin),
                'MFEM_DIR={0}'.format(mfem.prefix),
                'CONFIG_MK={0}'.format(config_mk),
                'GL_OPTS=-I{0} -I{1} -I{2}'.format(
                    spec['libx11'].prefix.include,
                    spec['gl'].prefix.include,
                    spec['glu'].prefix.include),
                'GL_LIBS={0}'.format(gl_libs.ld_flags)]

        if 'screenshots=png' in spec:
            args += [
                'USE_LIBPNG=YES', 'USE_LIBTIFF=NO',
                'PNG_OPTS=-DGLVIS_USE_LIBPNG -I{0}'.format(
                    spec['libpng'].prefix.include),
                'PNG_LIBS={0}'.format(spec['libpng'].libs.ld_flags)]
        elif 'screenshots=tiff' in spec:
            args += [
                'USE_LIBPNG=NO', 'USE_LIBTIFF=YES',
                'TIFF_OPTS=-DGLVIS_USE_LIBTIFF -I{0}'.format(
                    spec['libtiff'].prefix.include),
                'TIFF_LIBS={0}'.format(spec['libtiff'].libs.ld_flags)]
        else:
            args += ['USE_LIBPNG=NO', 'USE_LIBTIFF=NO']

        args.append('USE_FREETYPE={0}'.format(yes_no('+fonts')))
        if '+fonts' in spec:
            args += [
                'FT_OPTS=-DGLVIS_USE_FREETYPE {0} -I{1}'.format(
                    spec['freetype'].headers.include_flags,
                    spec['fontconfig'].prefix.include),
                'FT_LIBS={0} {1}'.format(
                    spec['freetype'].libs.ld_flags,
                    spec['fontconfig'].libs.ld_flags)]

        self.build_targets = args
        self.install_targets += args
