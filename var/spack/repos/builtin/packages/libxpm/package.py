# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libxpm(AutotoolsPackage, XorgPackage):
    """libXpm - X Pixmap (XPM) image file format library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libXpm"
    xorg_mirror_path = "lib/libXpm-3.5.12.tar.gz"

    version('3.5.12', sha256='2523acc780eac01db5163267b36f5b94374bfb0de26fc0b5a7bee76649fd8501')
    version('3.5.11', sha256='53ddf924441b7ed2de994d4934358c13d9abf4828b1b16e1255ade5032b31df7')
    version('3.5.10', sha256='f73f06928a140fd2090c439d1d55c6682095044495af6bf886f8e66cf21baee5')
    version('3.5.9', sha256='23beb930e27bc7df33cb0f6dbffc703852297c311b7e20146ff82e9a51f3e358')
    version('3.5.8', sha256='06472c7fdd175ea54c84162a428be19c154e7dda03d8bf91beee7f1d104669a6')
    version('3.5.7', sha256='422fbb311c4fe6ef337e937eb3adc8617a4320bd3e00fce06850d4360829b3ae')

    depends_on('gettext')
    depends_on('libx11')

    depends_on('xproto', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('util-macros', type='build')

    def setup_build_environment(self, env):
        # If libxpm is installed as an external package, gettext won't
        # be available in the spec. See
        # https://github.com/spack/spack/issues/9149 for details.
        if 'gettext' in self.spec:
            if self.spec['gettext'].prefix != '/usr':
                env.append_flags('LDFLAGS', '-L{0} -lintl'.format(
                    self.spec['gettext'].prefix.lib))
