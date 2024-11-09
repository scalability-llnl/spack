# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Luit(AutotoolsPackage, XorgPackage):
    """Luit is a filter that can be run between an arbitrary application and
    a UTF-8 terminal emulator such as xterm.  It will convert application
    output from the locale's encoding into UTF-8, and convert terminal
    input from UTF-8 into the locale's encoding."""

    homepage = "https://cgit.freedesktop.org/xorg/app/luit"
    xorg_mirror_path = "app/luit-1.1.1.tar.gz"

    license("MIT")

    version("1.1.1", sha256="87b0be0bd01f3b857a53e6625bdd31cef18418c95394b7f4387f8ecef78e45da")

    depends_on("c", type="build")  # generated

    depends_on("libfontenc")
    depends_on("libx11")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    # see https://www.linuxquestions.org/questions/linux-from-scratch-13/can't-compile-luit-xorg-applications-4175476308/
    def configure_args(self):
        return ["CFLAGS=-U_XOPEN_SOURCE -D_XOPEN_SOURCE=600"]
