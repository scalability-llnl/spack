# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Libqglviewer(QMakePackage):
    """libQGLViewer is a C++ library based on Qt that eases the creation of
    OpenGL 3D viewers."""

    homepage = "http://libqglviewer.com/"
    url = "http://libqglviewer.com/src/libQGLViewer-2.7.2.tar.gz"
    git = "https://github.com/GillesDebunne/libQGLViewer.git"

    license("GPL-2.0-or-later")

    version("2.7.2", sha256="e2d2799dec5cff74548e951556a1fa06a11d9bcde2ce6593f9c27a17543b7c08")

    # http://libqglviewer.com/installUnix.html

    depends_on("qt+gui+opengl")
    depends_on("freeglut", when="^qt@:3.0")
    depends_on("glu", type="link")

    build_directory = "QGLViewer"

    def patch(self):
        # Build dylib instead of Framework on macOS
        if self.spec.satisfies("platform=darwin"):
            filter_file(
                "!staticlib: CONFIG *= lib_bundle",
                "",
                join_path("QGLViewer", "QGLViewer.pro"),
                string=True,
            )

    def qmake_args(self):
        return ["PREFIX=" + self.prefix]

    @run_after("install")
    def darwin_fix(self):
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(self.prefix.lib)
