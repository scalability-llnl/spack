# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Atk(Package):
    """ATK provides the set of accessibility interfaces that are
       implemented by other toolkits and applications. Using the ATK
       interfaces, accessibility tools have full access to view and
       control running applications."""

    homepage = "https://developer.gnome.org/atk/"
    url      = "https://ftp.gnome.org/pub/gnome/sources/atk/2.30/atk-2.30.0.tar.xz"
    list_url = "https://ftp.gnome.org/pub/gnome/sources/atk"
    list_depth = 1

    version('2.36.0', sha256='fb76247e369402be23f1f5c65d38a9639c1164d934e40f6a9cf3c9e96b652788')
    version('2.30.0', sha256='dd4d90d4217f2a0c1fee708a555596c2c19d26fef0952e1ead1938ab632c027b')
    version('2.28.1', sha256='cd3a1ea6ecc268a2497f0cd018e970860de24a6d42086919d6bf6c8e8d53f4fc')
    version('2.20.0', sha256='493a50f6c4a025f588d380a551ec277e070b28a82e63ef8e3c06b3ee7c1238f0')
    version('2.14.0', sha256='2875cc0b32bfb173c066c22a337f79793e0c99d2cc5e81c4dac0d5a523b8fbad')

    depends_on('meson@0.40.1:', type='build', when='@2.28:')
    depends_on('meson@0.46.0:', type='build', when='@2.29:')
    depends_on('glib')
    depends_on('gettext')
    depends_on('pkgconfig', type='build')
    depends_on('gobject-introspection')
    depends_on('libffi')

    def url_for_version(self, version):
        """Handle gnome's version-based custom URLs."""
        url = 'http://ftp.gnome.org/pub/gnome/sources/atk'
        return url + '/%s/atk-%s.tar.xz' % (version.up_to(2), version)

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

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            meson('..', *std_meson_args)
            ninja('-v')
            ninja('install')

    @when('@:2.27')
    def install(self, spec, prefix):
        configure('--prefix={0}'.format(prefix))
        make()
        if self.run_tests:
            make('check')
        make('install')
        if self.run_tests:
            make('installcheck')
