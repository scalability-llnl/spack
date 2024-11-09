# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gexiv2(MesonPackage):
    """gexiv2 is a GObject wrapper around the Exiv2 photo metadata library.

    It allows for GNOME applications to easily inspect and update EXIF, IPTC,
    and XMP metadata in photo and video files of various formats."""

    homepage = "https://gitlab.gnome.org/GNOME/gexiv2"
    url = "https://download.gnome.org/sources/gexiv2/0.12/gexiv2-0.12.3.tar.xz"

    maintainers("benkirk")

    license("GPL-2.0-or-later")

    version("0.12.3", sha256="d23b7972a2fc6f840150bad1ed79c1cbec672951e180c1e1ec33ca6c730c59f3")
    version("0.12.2", sha256="2322b552aca330eef79724a699c51a302345d5e074738578b398b7f2ff97944c")
    version("0.12.1", sha256="8aeafd59653ea88f6b78cb03780ee9fd61a2f993070c5f0d0976bed93ac2bd77")
    version("0.12.0", sha256="58f539b0386f36300b76f3afea3a508de4914b27e78f58ee4d142486a42f926a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("cmake@3.4:", type="build")
    depends_on("ninja@1.8.2:", type="build")
    depends_on("exiv2")
    depends_on("vala")
    depends_on("gobject-introspection")
    depends_on("glib")
    depends_on("python")

    def meson_args(self):
        # disable python2
        args = ["-Dpython2_girdir=no"]
        return args
