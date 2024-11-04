# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Freeglut(CMakePackage, SourceforgePackage):
    """FreeGLUT is a free-software/open-source alternative to the OpenGL
    Utility Toolkit (GLUT) library"""

    homepage = "https://freeglut.sourceforge.net/"
    sourceforge_mirror_path = "freeglut/freeglut-3.2.1.tar.gz"

    license("MIT")

    version("3.2.2", sha256="c5944a082df0bba96b5756dddb1f75d0cd72ce27b5395c6c1dde85c2ff297a50")
    version("3.2.1", sha256="d4000e02102acaf259998c870e25214739d1f16f67f99cb35e4f46841399da68")
    version("3.0.0", sha256="2a43be8515b01ea82bcfa17d29ae0d40bd128342f0930cd1f375f1ff999f76a2")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared libs instead of static")

    depends_on("gl")
    depends_on("glu")

    # FreeGLUT does not support OSMesa
    conflicts("^osmesa")

    # FreeGLUT only works with GLX on linux
    with when("platform=linux"):
        depends_on("glx")
        depends_on("libx11")
        depends_on("libxi")
        depends_on("libxxf86vm")

    # freeglut 3.2.1 fails to build with -fno-common (default with newer compilers)
    # see https://bugs.gentoo.org/705840 and https://github.com/dcnieho/FreeGLUT/pull/76
    patch(
        "https://gitweb.gentoo.org/repo/gentoo.git/plain/media-libs/freeglut/files/freeglut-3.2.1-gcc10-fno-common.patch?id=f9102571b69d9fc05471a592fda252681fdfdef1",
        sha256="898e8fb314cbe728d791e9ea69829313143cda039c008f0ca06c1b5730922aa7",
        when="@3.2.1 %gcc@10.0:",
    )
    patch(
        "https://gitweb.gentoo.org/repo/gentoo.git/plain/media-libs/freeglut/files/freeglut-3.2.1-gcc10-fno-common.patch?id=f9102571b69d9fc05471a592fda252681fdfdef1",
        sha256="898e8fb314cbe728d791e9ea69829313143cda039c008f0ca06c1b5730922aa7",
        when="@3.2.1 %clang@11.0:",
    )
    patch(
        "https://gitweb.gentoo.org/repo/gentoo.git/plain/media-libs/freeglut/files/freeglut-3.2.1-gcc10-fno-common.patch?id=f9102571b69d9fc05471a592fda252681fdfdef1",
        sha256="898e8fb314cbe728d791e9ea69829313143cda039c008f0ca06c1b5730922aa7",
        when="@3.2.1 %aocc@2.3.0:",
    )

    def cmake_args(self):
        spec = self.spec
        args = [
            self.define("FREEGLUT_BUILD_DEMOS", False),
            self.define("FREEGLUT_GLES", False),
            self.define("FREEGLUT_WAYLAND", False),
            self.define("FREEGLUT_BUILD_SHARED_LIBS", "+shared" in spec),
            self.define("FREEGLUT_BUILD_STATIC_LIBS", "~shared" in spec),
            self.define("OpenGL_GL_PREFERENCE", "LEGACY"),
            self.define("OPENGL_INCLUDE_DIR", spec["gl"].headers.directories[0]),
            self.define("OPENGL_gl_LIBRARY", spec["gl"].libs[0]),
            self.define("OPENGL_opengl_LIBRARY", "IGNORE"),
            self.define("OPENGL_glx_LIBRARY", "IGNORE"),
            self.define("OPENGL_egl_LIBRARY", "IGNORE"),
        ]

        return args

    @property
    def libs(self):
        return find_libraries(["libglut"], root=self.prefix, recursive=True)
