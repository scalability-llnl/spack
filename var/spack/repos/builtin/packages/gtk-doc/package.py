# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GtkDoc(AutotoolsPackage):
    """GtkDoc is a tool used to extract API documentation from
    C-code like Doxygen, but handles documentation of GObject
    (including signals and properties) that makes it very
    suitable for GTK+ apps and libraries. It uses docbook for
    intermediate files and can produce html by default and
    pdf/man-pages with some extra work."""

    homepage = "https://wiki.gnome.org/DocumentationProject/GtkDoc"
    url = "https://gitlab.gnome.org/GNOME/gtk-doc/-/archive/1.33.2/gtk-doc-1.33.2.tar.gz"

    license("GPL-2.0-or-later AND GFDL-1.1-or-later")

    version("1.33.2", sha256="2d1b0cbd26edfcb54694b2339106a02a81d630a7dedc357461aeb186874cc7c0")
    version("1.32", sha256="0890c1f00d4817279be51602e67c4805daf264092adc58f9c04338566e8225ba")

    depends_on("c", type="build")  # generated

    # Commented out until package dblatex has been created
    # variant('pdf', default=False, description='Adds PDF support')

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("itstool", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig@0.19:", type=("build", "run"))

    depends_on("python@3.2:", type=("build", "run"))
    depends_on("py-pygments", type=("build", "run"))
    depends_on("py-anytree", type=("test"))
    depends_on("py-lxml", type=("test"))
    depends_on("py-parameterized", type=("test"))
    depends_on("py-six", type=("test"))
    depends_on("libxslt")
    depends_on("libxml2@2.3.6:")
    depends_on("docbook-xsl")
    depends_on("docbook-xml")
    # depends_on('dblatex', when='+pdf')

    patch("build.patch")

    def setup_build_environment(self, env):
        """If test/tools.sh does not find gtkdocize it starts a sh which blocks"""
        env.prepend_path("PATH", join_path(self.stage.source_path, "buildsystems", "autotools"))

    def install(self, spec, prefix):
        make("install", "V=1")
        install(join_path("buildsystems", "autotools", "gtkdocize"), prefix.bin)

    def installcheck(self):
        """gtk-doc does not support installcheck properly, skip it"""
        pass

    def url_for_version(self, version):
        """Handle gnome's version-based custom URLs."""

        if version <= Version("1.32"):
            url = "https://gitlab.gnome.org/GNOME/gtk-doc/-/archive/GTK_DOC_{0}/gtk-doc-GTK_DOC_{0}.tar.gz"
            return url.format(version.underscored)

        url = "https://gitlab.gnome.org/GNOME/gtk-doc/-/archive/{0}/gtk-doc-{0}.tar.gz"
        return url.format(version)

    def configure_args(self):
        args = ["--with-xml-catalog={0}".format(self.spec["docbook-xml"].package.catalog)]
        return args
