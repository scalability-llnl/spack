# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Plplot(CMakePackage):
    """PLplot is a cross-platform package for creating scientific plots."""

    homepage = "https://plplot.sourceforge.net/"
    url = "https://sourceforge.net/projects/plplot/files/plplot/5.13.0%20Source/plplot-5.13.0.tar.gz/download"

    license("LGPL-2.0-or-later")

    version("5.15.0", sha256="b92de4d8f626a9b20c84fc94f4f6a9976edd76e33fb1eae44f6804bdcc628c7b")
    version("5.14.0", sha256="331009037c9cad9fcefacd7dbe9c7cfae25e766f5590f9efd739a294c649df97")
    version("5.13.0", sha256="ec36bbee8b03d9d1c98f8fd88f7dc3415560e559b53eb1aa991c2dcf61b25d2b")
    version("5.12.0", sha256="8dc5da5ef80e4e19993d4c3ef2a84a24cc0e44a5dade83201fca7160a6d352ce")
    version("5.11.0", sha256="bfa8434e6e1e7139a5651203ec1256c8581e2fac3122f907f7d8d25ed3bd5f7e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("java", default=False, description="Enable Java binding")
    variant("lua", default=False, description="Enable Lua binding")
    variant("pango", default=False, description="Enable Pango")
    variant("qt", default=False, description="Enable QT binding")
    variant("tcl", default=True, description="Enable Tcl binding")
    variant("wx", default=False, description="Enable WxWidgets")
    variant("wxold", default=False, description="Use WxWidgets old interface")

    conflicts("~wx", when="+wxold")
    conflicts("+wxold", when="@:5.11")

    depends_on("java", when="+java")
    depends_on("lua", when="+lua")
    depends_on("pango", when="+pango")
    depends_on("qt", when="+qt")
    depends_on("tcl", when="+tcl")
    depends_on("wxwidgets", when="+wx")
    depends_on("libsm", type="link")

    depends_on("freetype")
    depends_on("gtkplus")
    depends_on("libx11")
    depends_on("qhull")
    depends_on("swig")

    def cmake_args(self):
        args = []
        # needs 'tk with wish'
        args += ["-DENABLE_tk=OFF"]

        if "+java" in self.spec:
            args += ["-DENABLE_java=ON"]
        else:
            args += ["-DENABLE_java=OFF"]

        if "+lua" in self.spec:
            args += ["-DENABLE_lua=ON"]
        else:
            args += ["-DENABLE_lua=OFF"]

        if "+qt" in self.spec:
            args += ["-DENABLE_qt=ON"]
        else:
            args += ["-DENABLE_qt=OFF"]

        if "+tcl" in self.spec:
            args += ["-DENABLE_tcl=ON"]
            # could also be addressed by creating the links within tcl
            # as is done for the tclsh executable
            args += [
                "-DTCL_INCLUDE_PATH={0}/include".format(self.spec["tcl"].headers.directories[0]),
                "-DTCL_LIBRARY={0}".format(
                    LibraryList(
                        find_libraries(
                            "libtcl*", self.spec["tcl"].prefix, shared=True, recursive=True
                        )
                    )
                ),
                "-DTCL_STUB_LIBRARY={0}".format(
                    LibraryList(
                        find_libraries(
                            "libtclstub*", self.spec["tcl"].prefix, shared=False, recursive=True
                        )
                    )
                ),
            ]
        else:
            args += ["-DENABLE_tcl=OFF"]

        if "+wx" in self.spec:
            args += ["-DENABLE_wxwidgets=ON"]
            if "+wxold" in self.spec:
                args += ["-DOLD_WXWIDGETS=ON"]
        else:
            args += ["-DENABLE_wxwidgets=OFF"]

        return args
