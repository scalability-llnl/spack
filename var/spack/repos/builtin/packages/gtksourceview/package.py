# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Gtksourceview(AutotoolsPackage):
    """GtkSourceView is a GNOME library that extends GtkTextView, the
    standard GTK+ widget for multiline text editing. GtkSourceView adds
    support for syntax highlighting, undo/redo, file loading and saving,
    search and replace, a completion system, printing, displaying line
    numbers, and other features typical of a source code editor.
    """

    homepage = "https://projects.gnome.org/gtksourceview"
    url = "https://download.gnome.org/sources/gtksourceview/4.2/gtksourceview-4.2.0.tar.xz"

    license("LGPL-2.1-or-later")

    version("4.2.0", sha256="c431eb234dc83c7819e58f77dd2af973252c7750da1c9d125ddc94268f94f675")
    version("3.24.11", sha256="691b074a37b2a307f7f48edc5b8c7afa7301709be56378ccf9cc9735909077fd")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("gobject-introspection", type="build")
    depends_on("intltool", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("gettext")
    depends_on("glib@2.48.0:", when="@3.24.11:4.2.0")
    depends_on("gtkplus@3.20.0:", when="@3.24.11:4.2.0")
    depends_on("libxml2@2.6:", when="@3.24.11:4.2.0")
    depends_on("pango")
    depends_on("gdk-pixbuf")
    depends_on("atk")
    depends_on("iconv")

    def url_for_version(self, version):
        url = "https://download.gnome.org/sources/gtksourceview/"
        url += "{0}/gtksourceview-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_build_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    def setup_run_environment(self, env):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)

    # TODO: If https://github.com/spack/spack/pull/12344 is merged, this
    # method is unnecessary.
    def autoreconf(self, spec, prefix):
        autoreconf = which("autoreconf")
        autoreconf("-ifv")
