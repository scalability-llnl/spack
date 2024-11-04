# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gl2ps(CMakePackage):
    """GL2PS is a C library providing high quality vector output for any
    OpenGL application."""

    homepage = "https://www.geuz.org/gl2ps/"
    url = "https://geuz.org/gl2ps/src/gl2ps-1.3.9.tgz"

    license("LGPL-2.0-only")

    version("1.4.2", sha256="8d1c00c1018f96b4b97655482e57dcb0ce42ae2f1d349cd6d4191e7848d9ffe9")
    version("1.4.0", sha256="03cb5e6dfcd87183f3b9ba3b22f04cd155096af81e52988cc37d8d8efe6cf1e2")
    version("1.3.9", sha256="8a680bff120df8bcd78afac276cdc38041fed617f2721bade01213362bcc3640")

    depends_on("c", type="build")  # generated

    variant("png", default=True, description="Enable PNG support")
    variant("zlib", default=True, description="Enable compression using ZLIB")
    variant("doc", default=False, description="Generate documentation using pdflatex")

    depends_on("cmake@2.8.6:", type="build")

    depends_on("gl")

    depends_on("libpng", when="+png")
    depends_on("zlib-api", when="+zlib")
    depends_on("texlive", type="build", when="+doc")

    # gl2ps tries to build static and shared libs at once with the same
    # target name. This causes ninja to fail the build
    # This patch defines a new CL opt to toggle shared vs static
    # and renames all lib target refs
    # Patch derived from https://gitlab.onelab.info/gl2ps/gl2ps/-/issues/30
    # and fixes a few additional places that solution misses.
    with when("platform=windows"):
        variant("shared", default=True, description="Enable building shared libraries")
        patch("prevent-ninja-target-clash.patch")

    def cmake_args(self):
        spec = self.spec
        options = [
            self.define("CMAKE_DISABLE_FIND_PACKAGE_GLUT", True),
            self.define_from_variant("ENABLE_PNG", "png"),
            self.define_from_variant("ENABLE_ZLIB", "zlib"),
            self.define("OpenGL_GL_PREFERENCE", "LEGACY"),
            self.define("OPENGL_INCLUDE_DIR", spec["gl"].headers.directories[0]),
            self.define("OPENGL_gl_LIBRARY", spec["gl"].libs[0]),
            self.define("OPENGL_opengl_LIBRARY", "IGNORE"),
            self.define("OPENGL_glx_LIBRARY", "IGNORE"),
            self.define("OPENGL_egl_LIBRARY", "IGNORE"),
            self.define("OPENGL_glu_LIBRARY", "IGNORE"),
        ]
        if spec.satisfies("platform=darwin"):
            options.append(self.define("CMAKE_MACOSX_RPATH", True))

        if spec.satisfies("platform=windows"):
            options.append(self.define_from_variant("BUILD_SHARED_LIBS", "shared"))

        if spec.satisfies("~doc"):
            # Make sure we don't look.
            options.append(self.define("CMAKE_DISABLE_FIND_PACKAGE_LATEX", True))

        return options
