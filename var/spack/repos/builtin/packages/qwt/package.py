# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qwt(QMakePackage):
    """The Qwt library contains GUI Components and utility classes which are
    primarily useful for programs with a technical background. Beside a
    framework for 2D plots it provides scales, sliders, dials, compasses,
    thermometers, wheels and knobs to control or display values, arrays, or
    ranges of type double.
    """

    homepage = "https://qwt.sourceforge.net/"
    url = "https://sourceforge.net/projects/qwt/files/qwt/6.1.3/qwt-6.1.3.tar.bz2"

    license("custom")

    version("6.1.6", sha256="99460d31c115ee4117b0175d885f47c2c590d784206f09815dc058fbe5ede1f6")
    version("6.1.4", sha256="1529215329e51fc562e0009505a838f427919a18b362afff441f035b2d9b5bd9")
    version("6.1.3", sha256="f3ecd34e72a9a2b08422fb6c8e909ca76f4ce5fa77acad7a2883b701f4309733")
    version("5.2.2", sha256="36bf2ee51ca9c74fde1322510ffd39baac0db60d5d410bb157968a78d9c1464b")

    depends_on("cxx", type="build")  # generated

    variant("designer", default=False, description="Build extensions to QT designer")
    variant("opengl", default=False, description="Build OpenGL plot canvas")

    patch("no-designer.patch", when="~designer")
    patch("no-opengl_6_1.patch", when="@6.1 ~opengl")

    depends_on("qt+tools", when="+designer")
    depends_on("qt+opengl", when="+opengl")

    # Qwt does not support Qt6; this picks the right qmake provider
    conflicts("^qt-base", msg="Qwt requires Qt5")

    # the qt@5.14.2 limitation was lifted in qwt@6.1.5
    # https://sourceforge.net/p/qwt/code/HEAD/tree/tags/qwt-6.1.6/CHANGES-6.1
    depends_on("qt@:5.14.2", when="@:6.1.4")
    # Qwt 6.1.1 and older use a constant that was removed in Qt 5.4
    # https://bugs.launchpad.net/ubuntu/+source/qwt-qt5/+bug/1485213
    depends_on("qt@:5.3", when="@:6.1.1")

    def patch(self):
        # Subvert hardcoded prefix
        filter_file(r"/usr/local/qwt-\$\$(QWT_)?VERSION.*", self.prefix, "qwtconfig.pri")
