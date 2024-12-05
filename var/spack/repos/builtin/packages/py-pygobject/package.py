# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygobject(PythonPackage):
    """bindings for the GLib, and GObject,
    to be used in Python."""

    homepage = "https://pygobject.readthedocs.io/en/latest/"

    license("LGPL-2.1-or-later")

    version("3.46.0", sha256="426008b2dad548c9af1c7b03b59df0440fde5c33f38fb5406b103a43d653cafc")
    version(
        "3.38.0",
        sha256="0372d1bb9122fc19f500a249b1f38c2bb67485000f5887497b4b205b3e7084d5",
        deprecated=True,
    )
    version(
        "3.28.3",
        sha256="3dd3e21015d06e00482ea665fc1733b77e754a6ab656a5db5d7f7bfaf31ad0b0",
        deprecated=True,
    )
    version(
        "2.28.6",
        sha256="fb8a1d4f665130a125011659bd347c7339c944232163dbb9a34fd0686577adb8",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    extends("python")

    depends_on("py-setuptools", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("gtkplus")

    # meson.build
    depends_on("python@3.8:3", type=("build", "run"), when="@3.46.0")
    depends_on("glib@2.64.0:", when="@3.46.0")
    depends_on("gobject-introspection@1.64.0:", when="@3.46.0")
    depends_on("py-pycairo@1.16:1", type=("build", "run"), when="@3.46.0")
    depends_on("libffi@3.0.0:", when="@3.46.0")

    depends_on("glib", when="@:3.46.0")
    depends_on("gobject-introspection", when="@:3.46.0")
    depends_on("py-pycairo", type=("build", "run"), when="@:3.46.0")
    depends_on("libffi", when="@:3.46.0")

    # pygobject links directly using the compiler, not spack's wrapper.
    # This causes it to fail to add the appropriate rpaths. This patch modifies
    # pygobject's setup.py file to add -Wl,-rpath arguments for dependent
    # libraries found with pkg-config.
    patch("pygobject-3.28.3-setup-py.patch", when="@3.28.3")

    def url_for_version(self, version):
        url = "http://ftp.gnome.org/pub/GNOME/sources/pygobject"
        return url + "/%s/pygobject-%s.tar.xz" % (version.up_to(2), version)

    def patch(self):
        filter_file(r"Pycairo_IMPORT", r"//Pycairo_IMPORT", "gi/pygi-foreign-cairo.c")
