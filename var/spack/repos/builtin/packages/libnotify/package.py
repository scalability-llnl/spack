# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libnotify(MesonPackage):
    """libnotify is a library for sending desktop notifications"""

    homepage = "https://github.com/GNOME/libnotify"
    url = "https://github.com/GNOME/libnotify/archive/0.7.9.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.7.9", sha256="9bd4f5fa911d27567e7cc2d2d09d69356c16703c4e8d22c0b49a5c45651f3af0")

    depends_on("c", type="build")  # generated

    # Libnotify is having trouble with finding the DTD and XSLT for docbook,
    # which is required for both of these varients.
    # variant('docbook', default=False,
    #         description='Build docbook docs. Currently broken')
    # variant('gtkdoc', default=False,
    #         description='Build with gtkdoc. Currently broken')

    depends_on("pkgconfig", type="build")
    depends_on("glib@2.26.0:")
    depends_on("gtkplus@2.90:")
    depends_on("gobject-introspection")
    depends_on("libxslt", type="build")
    depends_on("docbook-xsl", type="build")
    # depends_on('gtk-doc', when='+gtkdoc', type='build')
    # depends_on('xmlto', when='+docbook', type='build')

    patch("docbook-location.patch")

    def meson_args(self):
        # spec = self.spec
        args = []

        # if '+docbook' in spec:
        #     args.append('-Ddocbook_docs=enabled')
        # else:
        #     args.append('-Ddocbook_docs=disabled')
        args.append("-Ddocbook_docs=disabled")

        # if self.run_tests:
        #     args.append('-Dtests=true')
        # else:
        #     args.append('-Dtests=false')
        args.append("-Dtests=false")

        # if '+gtkdoc' in spec:
        #     args.append('-Dgtk_doc=true')
        # else:
        #     args.append('-Dgtk_doc=false')
        args.append("-Dgtk_doc=false")

        return args
