# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.build_systems.makefile
from spack.package import *


class Glvis(MakefilePackage):
    """GLVis: an OpenGL tool for visualization of FEM meshes and functions"""

    homepage = "https://glvis.org"
    git = "https://github.com/glvis/glvis.git"
    tags = ["radiuss"]

    maintainers = ["goxberry", "v-dobrev", "tzanio", "tomstitt"]

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

    version("develop", branch="master")

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

    variant(
        "screenshots",
        default="png",
        values=("xwd", "png", "tiff"),
        description="Backend used for screenshots",
    )
    variant("fonts", default=True, description="Use antialiased fonts via freetype & fontconfig")

    depends_on("mfem@develop", when="@develop")
    depends_on("mfem@4.0.0:", when="@4.0")
    depends_on("mfem@3.4.0", when="@3.4")
    depends_on("mfem@3.3", when="@3.3")
    depends_on("mfem@3.2", when="@3.2")
    depends_on("mfem@3.1", when="@3.1")

    depends_on("gl")
    depends_on("glu")
    depends_on("libx11", when="@:3.5")

    with when("@4.0:,develop"):
        depends_on("sdl2")
        depends_on("glm")
        depends_on("glew")
        depends_on("freetype")
        depends_on("fontconfig")

    with when("+fonts"):
        depends_on("freetype")
        depends_on("fontconfig")

    depends_on("libpng", when="screenshots=png")
    depends_on("libtiff", when="screenshots=tiff")
    depends_on("uuid", when="platform=linux")


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder):
    def edit(self, pkg, spec, prefix):

        args = [
            "CC={0}".format(env["CC"]),
            "PREFIX={0}".format(prefix.bin),
            "MFEM_DIR={0}".format(self.spec["mfem"].prefix),
            "CONFIG_MK={0}".format(self.spec["mfem"].package.config_mk),
        ]

        if self.spec.satisfies("@4.0:") or self.spec.satisfies("@develop"):
            # TODO: glu and fontconfig dirs
            args += [
                "GLM_DIR={0}".format(spec["glm"].prefix),
                "SDL_DIR={0}".format(spec["sdl2"].prefix),
                "GLEW_DIR={0}".format(spec["glew"].prefix),
                "FREETYPE_DIR={0}".format(spec["freetype"].prefix),
                "OPENGL_DIR={0}".format(spec["gl"].home),
            ]

        else:
            gl_libs = spec["glu"].libs + spec["gl"].libs + spec["libx11"].libs

            args += [
                "GL_OPTS=-I{0} -I{1} -I{2}".format(
                    spec["libx11"].prefix.include,
                    spec["gl"].home.include,
                    spec["glu"].prefix.include,
                ),
                "GL_LIBS={0}".format(gl_libs.ld_flags),
            ]

            args.append("USE_FREETYPE={0}".format("YES" if self.spec.satisfies("+fonts") else "NO"))
            if "+fonts" in spec:
                args += [
                    "FT_OPTS=-DGLVIS_USE_FREETYPE {0} -I{1}".format(
                        spec["freetype"].headers.include_flags, spec["fontconfig"].prefix.include
                    ),
                    "FT_LIBS={0} {1}".format(
                        spec["freetype"].libs.ld_flags, spec["fontconfig"].libs.ld_flags
                    ),
                ]

        if "screenshots=png" in spec:
            args.extend(self.png_args())
        elif "screenshots=tiff" in spec:
            args.extend(self.tiff_args())
        else:
            args.extend(self.xwd_args())

        self.build_targets = args
        self.install_targets += args

    def xwd_args(self):
        if self.spec.satisfies("@4.0:") or self.spec.satisfies("@develop"):
            return ["GLVIS_USE_LIBPNG=NO", "GLVIS_USE_LIBTIFF=NO"]
        return ["USE_LIBPNG=NO", "USE_LIBTIFF=NO"]

    def png_args(self):
        prefix_args = ["USE_LIBPNG=YES", "USE_LIBTIFF=NO"]
        if self.spec.satisfies("@4.0:") or self.spec.satisfies("@develop"):
            prefix_args = ["GLVIS_USE_LIBPNG=YES", "GLVIS_USE_LIBTIFF=NO"]

        libpng = self.spec["libpng"]
        return prefix_args + [
            "PNG_OPTS=-DGLVIS_USE_LIBPNG -I{0}".format(libpng.prefix.include),
            "PNG_LIBS={0}".format(libpng.libs.ld_flags),
        ]

    def tiff_args(self):
        prefix_args = ["USE_LIBPNG=NO", "USE_LIBTIFF=YES"]
        if self.spec.satisfies("@4.0:") or self.spec.satisfies("@develop"):
            prefix_args = ["GLVIS_USE_LIBPNG=NO", "GLVIS_USE_LIBTIFF=YES"]

        libtiff = self.spec["libtiff"]
        return prefix_args + [
            "TIFF_OPTS=-DGLVIS_USE_LIBTIFF -I{0}".format(libtiff.prefix.include),
            "TIFF_LIBS={0}".format(libtiff.libs.ld_flags),
        ]
