# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AtSpi2Core(MesonPackage):
    """The At-Spi2 Core package provides a Service Provider Interface for the
       Assistive Technologies available on the GNOME platform and a library
       against which applications can be linked."""

    homepage = "http://www.linuxfromscratch.org/blfs/view/cvs/x/at-spi2-core.html"
    url      = "http://ftp.gnome.org/pub/gnome/sources/at-spi2-core/2.28/at-spi2-core-2.38.0.tar.xz"
    list_url = "http://ftp.gnome.org/pub/gnome/sources/at-spi2-core"
    list_depth = 1

    version('2.38.0', sha256='84e36c3fe66862133f5fe229772b76aa2526e10de5014a3778f2fa46ce550da5')
    version('2.36.0', sha256='88da57de0a7e3c60bc341a974a80fdba091612db3547c410d6deab039ca5c05a')
    version('2.28.0', sha256='42a2487ab11ce43c288e73b2668ef8b1ab40a0e2b4f94e80fca04ad27b6f1c87')

    depends_on('meson@0.46.0:', type='build')
    depends_on('glib@2.56.1:')
    depends_on('dbus@1.12.8:')
    depends_on('gettext')
    depends_on('libx11')
    depends_on('libxi')
    depends_on('libxtst')
    depends_on('recordproto')
    depends_on('inputproto')
    depends_on('fixesproto')
    depends_on('pkgconfig', type='build')
    depends_on('python', type='build')
    depends_on('gobject-introspection')

    def url_for_version(self, version):
        """Handle gnome's version-based custom URLs."""
        url = 'http://ftp.gnome.org/pub/gnome/sources/at-spi2-core'
        return url + '/%s/at-spi2-core-%s.tar.xz' % (version.up_to(2), version)

    def setup_run_environment(self, env):
        env.prepend_path("GI_TYPELIB_PATH",
                         join_path(self.prefix.lib, 'girepository-1.0'))

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("GI_TYPELIB_PATH",
                         join_path(self.prefix.lib, 'girepository-1.0'))

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("GI_TYPELIB_PATH",
                         join_path(self.prefix.lib, 'girepository-1.0'))

    def setup_build_environment(self, env):
        # this avoids an "import site" error in the build
        env.unset('PYTHONHOME')
