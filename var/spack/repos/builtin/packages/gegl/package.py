# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gegl(MesonPackage):
    """GEGL (Generic Graphics Library) is a data flow based image
    processing framework, providing floating point processing and
    non-destructive image processing capabilities to GNU Image
    Manipulation Program and other projects (imgflo, GNOME Photos,
    iconographer, ...)"""

    homepage = "https://gegl.org/"
    url = "https://download.gimp.org/gegl/0.4/gegl-0.4.40.tar.xz"

    maintainers("benkirk")

    license("GPL-3.0-or-later AND LGPL-3.0-or-later")

    version("0.4.44", sha256="0a4cdb41635e406a0849cd0d3f03caf7d97cab8aa13d28707d532d0089d56126")
    version("0.4.42", sha256="aba83a0cbaa6c56edc29ea22f2e8172950a53b96daa51592083d59222bdde02d")
    version("0.4.40", sha256="cdde80d15a49dab9a614ef98f804c8ce6e4cfe1339a3c240c34f3fb45436b85d")
    version("0.4.38", sha256="e4a33c8430a5042fba8439b595348e71870f0d95fbf885ff553f9020c1bed750")
    version("0.4.36", sha256="6fd58a0cdcc7702258adaeffb573a389228ae8f0eff47578efda2309b61b2ca6")
    version("0.4.34", sha256="ef63f0bca5b431c6119addd834ca7fbb507c900c4861c57b3667b6f4ccfcaaaa")
    version("0.4.32", sha256="668e3c6b9faf75fb00512701c36274ab6f22a8ba05ec62dbf187d34b8d298fa1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("cmake@3.4:", type="build")
    depends_on("babl")
    depends_on("glib")
    depends_on("gobject-introspection")
    depends_on("json-glib")

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path("XDG_DATA_DIRS", self.prefix.share)
        env.prepend_path("GI_TYPELIB_PATH", join_path(self.prefix.lib, "girepository-1.0"))
