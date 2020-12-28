# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pango(AutotoolsPackage):
    """Pango is a library for laying out and rendering of text, with
       an emphasis on internationalization. It can be used anywhere
       that text layout is needed, though most of the work on Pango so
       far has been done in the context of the GTK+ widget toolkit."""
    homepage = "http://www.pango.org"
    url      = "http://ftp.gnome.org/pub/GNOME/sources/pango/1.40/pango-1.40.3.tar.xz"
    list_url = "http://ftp.gnome.org/pub/gnome/sources/pango/"
    list_depth = 1

    version('1.41.0', sha256='1f76ef95953dc58ee5d6a53e5f1cb6db913f3e0eb489713ee9266695cae580ba')
    version('1.40.3', sha256='abba8b5ce728520c3a0f1535eab19eac3c14aeef7faa5aded90017ceac2711d3')
    version('1.40.1', sha256='e27af54172c72b3ac6be53c9a4c67053e16c905e02addcf3a603ceb2005c1a40')
    version('1.36.8', sha256='18dbb51b8ae12bae0ab7a958e7cf3317c9acfc8a1e1103ec2f147164a0fc2d07')

    variant('X', default=False, description="Enable an X toolkit")

    depends_on("pkgconfig@0.9.0:", type="build")
    depends_on("harfbuzz")
    depends_on("cairo+ft+fc")
    depends_on("cairo~X", when='~X')
    depends_on("cairo+X", when='+X')
    depends_on("libxft", when='+X')
    depends_on("glib")
    depends_on('gobject-introspection')
    depends_on('fontconfig')
    depends_on('freetype@2:')
    depends_on('libffi')

    depends_on('harfbuzz@1.2.3:', when='@1.41.0')
    depends_on('libxft@2.0.0:', when='@1.41.0 +X')
    depends_on('glib@2.33.12:', when='@1.41.0')
    depends_on('fontconfig@2.11.91:', when='@1.41.0')

    def url_for_version(self, version):
        url = "http://ftp.gnome.org/pub/GNOME/sources/pango/{0}/pango-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def configure_args(self):
        args = []
        if self.spec.satisfies('+X'):
            args.append('--with-xft')
        else:
            args.append('--without-xft')

        # disable building of gtk-doc files following #9885 and #9771
        args.append('--disable-gtk-doc-html')
        true = which('true')
        args.append('GTKDOC_CHECK={0}'.format(true))
        args.append('GTKDOC_CHECK_PATH={0}'.format(true))
        args.append('GTKDOC_MKPDF={0}'.format(true))
        args.append('GTKDOC_REBASE={0}'.format(true))

        return args

    def install(self, spec, prefix):
        make("install", parallel=False)

    def setup_run_environment(self, env):
        env.prepend_path("GI_TYPELIB_PATH",
                         join_path(self.prefix.lib, 'girepository-1.0'))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH",
                         join_path(self.prefix.lib, 'girepository-1.0'))

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH",
                         join_path(self.prefix.lib, 'girepository-1.0'))
