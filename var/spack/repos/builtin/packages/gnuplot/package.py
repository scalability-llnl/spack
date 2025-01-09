# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Gnuplot(AutotoolsPackage):
    """Gnuplot is a portable command-line driven graphing utility for Linux,
    OS/2, MS Windows, OSX, VMS, and many other platforms. The source
    code is copyrighted but freely distributed (i.e., you don't have
    to pay for it). It was originally created to allow scientists and
    students to visualize mathematical functions and data
    interactively, but has grown to support many non-interactive uses
    such as web scripting. It is also used as a plotting engine by
    third-party applications like Octave. Gnuplot has been supported
    and under active development since 1986

    """

    homepage = "http://www.gnuplot.info"
    url = "https://downloads.sourceforge.net/project/gnuplot/gnuplot/5.0.6/gnuplot-5.0.6.tar.gz"

    # There is a conflict in term.h between gnuplot and ncurses, which is a
    # dependency of readline. Fix it with a small patch
    patch("term_include.patch")

    license("MIT")

    version("6.0.0", sha256="635a28f0993f6ab0d1179e072ad39b8139d07f51237f841d93c6c2ff4b1758ec")
    version("5.4.10", sha256="975d8c1cc2c41c7cedc4e323aff035d977feb9a97f0296dd2a8a66d197a5b27c")
    version("5.4.3", sha256="51f89bbab90f96d3543f95235368d188eb1e26eda296912256abcd3535bd4d84")
    version("5.4.2", sha256="e57c75e1318133951d32a83bcdc4aff17fed28722c4e71f2305cfc2ae1cae7ba")
    version("5.2.8", sha256="60a6764ccf404a1668c140f11cc1f699290ab70daa1151bb58fed6139a28ac37")
    version("5.2.7", sha256="97fe503ff3b2e356fe2ae32203fc7fd2cf9cef1f46b60fe46dc501a228b9f4ed")
    version("5.2.5", sha256="039db2cce62ddcfd31a6696fe576f4224b3bc3f919e66191dfe2cdb058475caa")
    version("5.2.2", sha256="a416d22f02bdf3873ef82c5eb7f8e94146795811ef808e12b035ada88ef7b1a1")
    version("5.2.0", sha256="7dfe6425a1a6b9349b1fb42dae46b2e52833b13e807a78a613024d6a99541e43")
    version("5.0.7", sha256="0ad760ff013b4a9cf29853fa9b50c50030a33cd8fb86220a23abb466655136fc")
    version("5.0.6", sha256="5bbe4713e555c2e103b7d4ffd45fca69551fff09cf5c3f9cb17428aaacc9b460")
    version("5.0.5", sha256="25f3e0bf192e01115c580f278c3725d7a569eb848786e12b455a3fda70312053")
    version("5.0.1", sha256="7cbc557e71df581ea520123fb439dea5f073adcc9010a2885dc80d4ed28b3c47")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("wx", default=False, description="Activates wxWidgets terminal")
    variant("gd", default=True, description="Activates gd based terminal")
    variant("cairo", default=True, description="Activates cairo based terminal")
    variant("X", default=False, description="Build with X11")
    variant("libcerf", default=True, description="Build with libcerf support")
    variant(
        "pbm",
        default=False,
        description="Enable PBM (Portable Bit Map) and other older bitmap terminals",
    )
    variant("qt", default=False, description="Build with QT")
    variant("readline", default=True, description="Build with readline")

    # required dependencies
    depends_on("readline", when="+readline")
    depends_on("pkgconfig", type="build")
    depends_on("libxpm")
    depends_on("iconv")

    # optional dependencies:
    depends_on("libcerf", when="+libcerf")
    depends_on("libgd", when="+gd")
    depends_on("cairo@1.2:", when="+cairo")
    depends_on("wxwidgets", when="+wx")
    depends_on("pango@1.10:", when="+wx")
    depends_on("libsm", when="+wx")
    depends_on("pango@1.10:", when="+cairo")
    depends_on("libx11", when="+X")
    depends_on("qt@5.7:+opengl", when="+qt")
    depends_on("qt+framework", when="+qt platform=darwin")

    def configure_args(self):
        # see https://github.com/Homebrew/homebrew-core/blob/master/Formula/gnuplot.rb
        # and https://github.com/macports/macports-ports/blob/master/math/gnuplot/Portfile
        spec = self.spec
        options = [
            "--disable-dependency-tracking",
            "--disable-silent-rules",
            # Per upstream: "--with-tutorial is horribly out of date."
            "--without-tutorial",
        ]

        options += self.with_or_without("readline", "prefix")

        if spec.satisfies("+pbm"):
            options.append("--with-bitmap-terminals")
        else:
            options.append("--without-bitmap-terminals")

        if spec.satisfies("+X"):
            # It seems there's an open bug for wxWidgets support
            # See : http://sourceforge.net/p/gnuplot/bugs/1694/
            os.environ["TERMLIBS"] = "-lX11"
            options.append("--with-x")
        else:
            options.append("--without-x")

        if spec.satisfies("+qt"):
            options.append("--with-qt=qt5")
            # QT needs C++11 compiler:
            os.environ["CXXFLAGS"] = "{0}".format(self.compiler.cxx11_flag)

            if spec.satisfies("platform=darwin"):
                qt_path = spec["qt"].prefix
                # see
                # http://gnuplot.10905.n7.nabble.com/Building-with-Qt-depends-on-pkg-config-Qt-5-term-doesn-t-work-on-OS-X-td18063.html
                os.environ["QT_LIBS"] = (
                    "-F{0}/lib "
                    + "-framework QtCore "
                    + "-framework QtGui "
                    + "-framework QtWidgets "
                    + "-framework QtNetwork "
                    + "-framework QtSvg "
                    + "-framework QtPrintSupport"
                ).format(qt_path)

                os.environ["QT_CFLAGS"] = (
                    "-F{0}/lib "
                    + "-I{0}/lib/QtCore.framework/Headers "
                    + "-I{0}/lib/QtGui.framework/Headers "
                    + "-I{0}/lib/QtWidgets.framework/Headers "
                    + "-I{0}/lib/QtNetwork.framework/Headers "
                    + "-I{0}/lib/QtSvg.framework/Headers"
                ).format(qt_path)
        else:
            options.append("--with-qt=no")

        if spec.satisfies("+wx"):
            options.append("--with-wx=%s" % spec["wxwidgets"].prefix)
        else:
            options.append("--disable-wxwidgets")

        if spec.satisfies("+gd"):
            options.append("--with-gd=%s" % spec["libgd"].prefix)
        else:
            options.append("--without-gd")

        if spec.satisfies("+cairo"):
            options.append("--with-cairo")
        else:
            options.append("--without-cairo")

        if spec.satisfies("+libcerf"):
            options.append("--with-libcerf")
        else:
            options.append("--without-libcerf")

        # TODO: Enable pdflib-based pdf terminal
        # '--with-pdf=%s' % spec['pdflib-lite'].prefix  (or pdflib)
        options.append("--without-pdf")

        # TODO: Enable lua-based terminals
        options.append("--without-lua")

        # TODO: --with-latex
        options.append("--without-latex")

        # TODO: --with-aquaterm  depends_on('aquaterm')
        options.append("--without-aquaterm")

        if spec.satisfies("%gcc@8:"):
            os.environ["LDFLAGS"] = "-Wl,--copy-dt-needed-entries"

        return options
