# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import spack.build_systems.makefile
from spack.package import *


class Glvis(MakefilePackage):
    """GLVis: an OpenGL tool for visualization of FEM meshes and functions"""

    homepage = "https://glvis.org"
    git = "https://github.com/glvis/glvis.git"
    tags = ["radiuss"]

    maintainers("v-dobrev", "tzanio", "tomstitt", "goxberry")

    # glvis (like mfem) is downloaded from a URL shortener at request
    # of upstream author Tzanio Kolev <tzanio@llnl.gov>.  See here:
    # https://github.com/mfem/mfem/issues/53
    #
    # The following procedure should be used to verify security when a
    # new version is added:
    #
    # 1. Verify that no checksums on old versions have changed.
    #
    # 2. Verify that the shortened URL for the new version is listed at:
    #    https://glvis.org/download/
    #
    # 3. Use http://getlinkinfo.com or similar to verify that the
    #    underling download link for the latest version comes has the
    #    prefix: http://glvis.github.io/releases
    #
    # If this quick verification procedure fails, additional discussion
    # will be required to verify the new version.
    #
    # glvis does not need mfem+mpi but will build that by default, to just build
    # a serial mfem: `spack install glvis ^mfem~mpi~metis'

    license("BSD-3-Clause")

    version("develop", branch="master")

    version(
        "4.2",
        sha256="314fb04040cd0a8128d6dac62ba67d7067c2c097364e5747182ee8371049b42a",
        url="https://bit.ly/glvis-4-2",
        extension=".tar.gz",
    )

    version(
        "4.1",
        sha256="7542c2942167533eec10d59b8331d18241798bbd86a7efbe51dc479db4127407",
        url="https://bit.ly/glvis-4-1",
        extension=".tar.gz",
    )

    version(
        "4.0",
        sha256="68331eaea8b93968ed6bf395388c2730b27bbcb4b7809ce44277726edccd9f08",
        url="https://bit.ly/glvis-4-0",
        extension=".tar.gz",
    )

    version(
        "3.4",
        sha256="289fbd2e09d4456e5fee6162bdc3e0b4c8c8d54625f3547ad2a69fef319279e7",
        url="https://bit.ly/glvis-3-4",
        extension=".tar.gz",
    )

    version(
        "3.3",
        sha256="e24d7c5cb53f208b691c872fe82ea898242cfdc0fd68dd0579c739e070dcd800",
        url="http://goo.gl/C0Oadw",
        extension=".tar.gz",
    )

    version(
        "3.2",
        sha256="c82cb110396e63b6436a770c55eb6d578441eaeaf3f9cc20436c242392e44e80",
        url="http://goo.gl/hzupg1",
        extension=".tar.gz",
    )

    version(
        "3.1",
        sha256="793e984ddfbf825dcd13dfe1ca00eccd686cd40ad30c8789ba80ee175a1b488c",
        url="http://goo.gl/gQZuu9",
        extension="tar.gz",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "screenshots",
        default="png",
        values=("xwd", "png", "tiff"),
        description="Backend used for screenshots",
    )
    variant("fonts", default=True, description="Use antialiased fonts via freetype & fontconfig")

    depends_on("mfem@develop", when="@develop")
    depends_on("mfem@4.4.0:", when="@4.2")
    depends_on("mfem@4.3.0:", when="@4.1")
    depends_on("mfem@4.0.0:", when="@4.0")
    depends_on("mfem@3.4.0", when="@3.4")
    depends_on("mfem@3.3", when="@3.3")
    depends_on("mfem@3.2", when="@3.2")
    depends_on("mfem@3.1", when="@3.1")

    with when("@:3"):
        depends_on("gl")
        depends_on("glu")
        depends_on("libx11")

    with when("@4.0:"):
        # On Mac, we use the OpenGL framework
        if sys.platform.startswith("linux"):
            depends_on("gl")
        depends_on("sdl2")
        depends_on("glm")
        # On Mac, use external glew, e.g. from Homebrew
        depends_on("glew")
        # On Mac, use external freetype and fontconfig, e.g. from /opt/X11
        depends_on("freetype")
        depends_on("fontconfig")
        depends_on("xxd", type="build")

    with when("+fonts"):
        depends_on("freetype")
        depends_on("fontconfig")

    depends_on("libpng", when="screenshots=png")
    depends_on("libtiff", when="screenshots=tiff")


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):
    @property
    def build_targets(self):
        return self.common_args()

    @property
    def install_targets(self):
        return ["install"] + self.common_args()

    def common_args(self):
        spec = self.spec
        result = [
            "CC={0}".format(env["CC"]),
            "PREFIX={0}".format(self.spec.prefix.bin),
            "MFEM_DIR={0}".format(self.spec["mfem"].prefix),
            "CONFIG_MK={0}".format(self.spec["mfem"].package.config_mk),
        ]

        # https://github.com/spack/spack/issues/42839
        result.append("CPPFLAGS=-DGLEW_NO_GLU")

        if self.spec.satisfies("@4.0:"):
            # Spack will inject the necessary include dirs and link paths via
            # its compiler wrapper, so we can skip them:
            result += ["GLM_DIR=", "SDL_DIR=", "GLEW_DIR=", "FREETYPE_DIR=", "OPENGL_DIR="]
            # Spack will not inject include dirs like /usr/include/freetype2,
            # so we need to do it ourselves:
            if spec["freetype"].external:
                result += ["GL_OPTS={0}".format(spec["freetype"].headers.cpp_flags)]

        else:
            gl_libs = spec["glu"].libs + spec["gl"].libs + spec["libx11"].libs

            result += [
                "GL_OPTS=-I{0} -I{1} -I{2}".format(
                    spec["libx11"].prefix.include,
                    spec["gl"].home.include,
                    spec["glu"].prefix.include,
                ),
                "GL_LIBS={0}".format(gl_libs.ld_flags),
            ]
            result.extend(self.fonts_args())

        if self.spec.satisfies("screenshots=png"):
            result.extend(self.png_args())
        elif self.spec.satisfies("screenshots=tiff"):
            result.extend(self.tiff_args())
        else:
            result.extend(self.xwd_args())

        return result

    def fonts_args(self):
        if not self.spec.satisfies("+fonts"):
            return ["USE_FREETYPE=NO"]

        freetype = self.spec["freetype"]
        fontconfig = self.spec["fontconfig"]
        return [
            "USE_FREETYPE=YES",
            "FT_OPTS=-DGLVIS_USE_FREETYPE {0} -I{1}".format(
                freetype.headers.include_flags, fontconfig.prefix.include
            ),
            "FT_LIBS={0} {1}".format(freetype.libs.ld_flags, fontconfig.libs.ld_flags),
        ]

    def xwd_args(self):
        if self.spec.satisfies("@4.0:"):
            return ["GLVIS_USE_LIBPNG=NO", "GLVIS_USE_LIBTIFF=NO"]
        return ["USE_LIBPNG=NO", "USE_LIBTIFF=NO"]

    def png_args(self):
        prefix_args = ["USE_LIBPNG=YES", "USE_LIBTIFF=NO"]
        if self.spec.satisfies("@4.0:"):
            prefix_args = ["GLVIS_USE_LIBPNG=YES", "GLVIS_USE_LIBTIFF=NO"]

        libpng = self.spec["libpng"]
        return prefix_args + [
            "PNG_OPTS=-DGLVIS_USE_LIBPNG -I{0}".format(libpng.prefix.include),
            "PNG_LIBS={0}".format(libpng.libs.ld_flags),
        ]

    def tiff_args(self):
        prefix_args = ["USE_LIBPNG=NO", "USE_LIBTIFF=YES"]
        if self.spec.satisfies("@4.0:"):
            prefix_args = ["GLVIS_USE_LIBPNG=NO", "GLVIS_USE_LIBTIFF=YES"]

        libtiff = self.spec["libtiff"]
        return prefix_args + [
            "TIFF_OPTS=-DGLVIS_USE_LIBTIFF -I{0}".format(libtiff.prefix.include),
            "TIFF_LIBS={0}".format(libtiff.libs.ld_flags),
        ]
