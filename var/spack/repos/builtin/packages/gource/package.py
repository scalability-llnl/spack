# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Gource(AutotoolsPackage):
    """Software version control visualization."""

    homepage = "https://gource.io"
    url = "https://github.com/acaudwell/Gource/releases/download/gource-0.44/gource-0.44.tar.gz"

    license("GPL-3.0")

    version("0.44", sha256="2604ca4442305ffdc5bb1a7bac07e223d59c846f93567be067e8dfe2f42f097c")

    depends_on("cxx", type="build")  # generated

    depends_on("automake", type="build")
    depends_on("autoconf", type="build")
    depends_on("libtool", type="build")
    depends_on("glm", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("freetype@2.0:")
    depends_on("pcre")
    depends_on("boost@1.46:+filesystem+system")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("glew")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("pcre")
    depends_on("sdl2")
    depends_on("sdl2-image")

    parallel = False
    force_autoreconf = True

    def configure_args(self):
        spec = self.spec
        return [
            "--disable-dependency-tracking",
            "--without-x",
            "--with-boost=%s" % spec["boost"].prefix,
        ]
