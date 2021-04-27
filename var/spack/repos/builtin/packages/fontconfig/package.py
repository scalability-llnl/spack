# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fontconfig(AutotoolsPackage):
    """Fontconfig is a library for configuring/customizing font access"""
    homepage = "http://www.freedesktop.org/wiki/Software/fontconfig/"
    url      = "http://www.freedesktop.org/software/fontconfig/release/fontconfig-2.12.3.tar.gz"

    version('2.13.1', sha256='9f0d852b39d75fc655f9f53850eb32555394f36104a044bb2b2fc9e66dbbfa7f')
    version('2.12.3', sha256='ffc3cbf6dd9fcd516ee42f48306a715e66698b238933d6fa7cef02ea8b3b818e')
    version('2.12.1', sha256='a9f42d03949f948a3a4f762287dbc16e53a927c91a07ee64207ebd90a9e5e292')
    version('2.11.1', sha256='b6b066c7dce3f436fdc0dfbae9d36122b38094f4f53bd8dffd45e195b0540d8d')

    depends_on('freetype')
    depends_on('gperf', type='build', when='@2.12.2:')
    depends_on('libxml2')
    depends_on('pkgconfig', type='build')
    depends_on('font-util')
    depends_on('uuid', when='@2.13.1:')

    # Resolve known issue with tarballs 2.12.3 - 2.13.0 plus
    # https://gitlab.freedesktop.org/fontconfig/fontconfig/-/issues/10
    @run_before('configure')
    def _rm_offending_header(self):
        force_remove(join_path('src', 'fcobjshash.h'))

    def configure_args(self):
        font_path = join_path(self.spec['font-util'].prefix, 'share', 'fonts')

        return [
            '--enable-libxml2',
            '--disable-docs',
            '--with-default-fonts={0}'.format(font_path)
        ]

    @run_after('install')
    def system_fonts(self):
        # point configuration file to system-install fonts
        # gtk applications were failing to display text without this
        config_file = join_path(self.prefix, 'etc', 'fonts', 'fonts.conf')
        filter_file('<dir prefix="xdg">fonts</dir>',
                    '<dir prefix="xdg">fonts</dir><dir>/usr/share/fonts</dir>',
                    config_file)
