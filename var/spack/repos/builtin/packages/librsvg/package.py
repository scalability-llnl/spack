# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Librsvg(AutotoolsPackage):
    """Library to render SVG files using Cairo"""

    homepage = "https://wiki.gnome.org/Projects/LibRsvg"
    url      = "https://download.gnome.org/sources/librsvg/2.44/librsvg-2.44.14.tar.xz"

    version('2.51.0', sha256='89d32e38445025e1b1d9af3dd9d3aeb9f6fce527aeecbecf38b369b34c80c038')
    version('2.50.2', sha256='6211f271ce4cd44a7318190d36712e9cea384a933d3e3570004edeb210a056d3')
    version('2.50.0', sha256='b3fadba240f09b9c9898ab20cb7311467243e607cf8f928b7c5f842474ee3df4')
    version('2.44.14', sha256='6a85a7868639cdd4aa064245cc8e9d864dad8b8e9a4a8031bb09a4796bc4e303')

    depends_on("gobject-introspection", type='build')
    depends_on("pkgconfig", type='build')
    depends_on("rust", type='build')
    depends_on('gtk-doc', type='build')
    depends_on("cairo+gobject")
    depends_on("gdk-pixbuf")
    depends_on("glib")
    depends_on("libcroco")
    depends_on("pango")
    depends_on('libffi')
    depends_on('libxml2')
    depends_on('shared-mime-info')

    def url_for_version(self, version):
        url  = "https://download.gnome.org/sources/librsvg/"
        url += "{0}/librsvg-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)

    def setup_build_environment(self, env):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)

    def setup_run_environment(self, env):
        env.prepend_path('XDG_DATA_DIRS', self.prefix.share)
