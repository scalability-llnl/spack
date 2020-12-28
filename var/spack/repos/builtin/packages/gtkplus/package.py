# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gtkplus(AutotoolsPackage):
    """The GTK+ 2 package contains libraries used for creating graphical user
       interfaces for applications."""
    homepage = "http://www.gtk.org"
    url = "http://ftp.gnome.org/pub/gnome/sources/gtk+/2.24/gtk+-2.24.31.tar.xz"
    version('3.20.10', sha256='e81da1af1c5c1fee87ba439770e17272fa5c06e64572939814da406859e56b70')
    version('2.24.32', sha256='b6c8a93ddda5eabe3bfee1eb39636c9a03d2a56c7b62828b359bf197943c582e')
    version('2.24.31', sha256='68c1922732c7efc08df4656a5366dcc3afdc8791513400dac276009b40954658')
    version('2.24.25', sha256='38af1020cb8ff3d10dda2c8807f11e92af9d2fa4045de61c62eedb7fbc7ea5b3')

    variant('cups', default='False', description='enable cups support')

    depends_on('pkgconfig', type='build')

    depends_on('atk')
    depends_on('gdk-pixbuf')
    depends_on('glib')
    depends_on('shared-mime-info')
    # Hardcode X11 support (former +X variant),
    # see #6940 for rationale:
    depends_on('pango+X')
    depends_on('cairo+X+pdf+gobject')
    depends_on('gobject-introspection')
    depends_on('libepoxy', when='@3:')
    depends_on('libxi', when='@3:')
    depends_on('inputproto', when='@3:')
    depends_on('fixesproto', when='@3:')
    depends_on('at-spi2-atk', when='@3:')
    depends_on('gettext', when='@3:')
    depends_on('cups', when='+cups')

    patch('no-demos.patch', when='@2:2.99')

    def url_for_version(self, version):
        url = 'http://ftp.gnome.org/pub/gnome/sources/gtk+'
        return url + '/%s/gtk+-%s.tar.xz' % (version.up_to(2), version)

    def patch(self):
        # remove disable deprecated flag.
        filter_file(r'CFLAGS="-DGDK_PIXBUF_DISABLE_DEPRECATED $CFLAGS"',
                    '', 'configure', string=True)

    def setup_run_environment(self, env):
        env.prepend_path("GI_TYPELIB_PATH",
                         join_path(self.prefix.lib, 'girepository-1.0'))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH",
                         join_path(self.prefix.lib, 'girepository-1.0'))

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH",
                         join_path(self.prefix.lib, 'girepository-1.0'))

    def configure_args(self):
        args = []
        # disable building of gtk-doc files following #9771
        args.append('--disable-gtk-doc-html')
        true = which('true')
        args.append('GTKDOC_CHECK={0}'.format(true))
        args.append('GTKDOC_CHECK_PATH={0}'.format(true))
        args.append('GTKDOC_MKPDF={0}'.format(true))
        args.append('GTKDOC_REBASE={0}'.format(true))
        if '~cups' in self.spec:
            args.append('--disable-cups')
        return args
