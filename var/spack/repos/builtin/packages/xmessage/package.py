# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xmessage(AutotoolsPackage, XorgPackage):
    """xmessage displays a message or query in a window.  The user can click
    on an "okay" button to dismiss it or can select one of several buttons
    to answer a question.  xmessage can also exit after a specified time."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xmessage"
    xorg_mirror_path = "app/xmessage-1.0.4.tar.gz"

    license("MIT")

    version("1.0.6", sha256="46acfb25c531f59a24abc85b14b956c9c03c870757dddae4d6d083833924a071")
    version("1.0.5", sha256="99533a90ab66e268180a8400796950a7f560ea9421e2c3f32284cabc1858806b")
    version("1.0.4", sha256="883099c3952c8cace5bd11d3df2e9ca143fc07375997435d5ff4f2d50353acca")

    depends_on("c", type="build")  # generated

    depends_on("libxaw")
    depends_on("libxt")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
