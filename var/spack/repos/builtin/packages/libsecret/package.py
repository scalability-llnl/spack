# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libsecret(AutotoolsPackage):
    """libsecret is a library for storing and retrieving passwords and other
    secrets. It communicates with the "Secret Service" using D-Bus.
    gnome-keyring and ksecretservice are both implementations of a Secret
    Service.

    libsecret replaces libgnome-keyring
    """

    homepage = "https://wiki.gnome.org/Projects/Libsecret"
    url = "http://ftp.gnome.org/pub/gnome/sources/libsecret/0.18/libsecret-0.18.8.tar.xz"

    license("LGPL-2.1-or-later")

    version("0.18.8", sha256="3bfa889d260e0dbabcf5b9967f2aae12edcd2ddc9adc365de7a5cc840c311d15")

    depends_on("c", type="build")  # generated

    variant("gcrypt", default=True, description="Build with libgcrypt")
    variant("gobj", default=False, description="Build with gobject-introspection")
    # Optional Vala support is not implemented yet
    # variant('vala', default=False, descript='Build with Vala support')

    depends_on("pkgconfig", type="build")
    #    depends_on('mesa')
    # https://gitlab.gnome.org/GNOME/libsecret/blob/master/meson.build
    depends_on("glib@2.44:")
    depends_on("libgcrypt@1.2.2:", when="+gcrypt")
    depends_on("gobject-introspection", when="+gobj")
    # depends_on('vala', when='+vala') # Package doesn't exist yet

    def url_for_version(self, version):
        url = "http://ftp.gnome.org/pub/gnome/sources/libsecret"
        return url + "/%s/libsecret-%s.tar.xz" % (version.up_to(2), version)

    # https://www.linuxfromscratch.org/blfs/view/svn/gnome/libsecret.html
    def configure_args(self):
        args = []
        args.append("--disable-static")
        args.append("--disable-manpages")
        if "+gcrypt" not in self.spec:
            args.append("--disable-gcrypt")
        return args
