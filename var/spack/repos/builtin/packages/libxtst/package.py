# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxtst(AutotoolsPackage, XorgPackage):
    """libXtst provides the Xlib-based client API for the XTEST & RECORD
    extensions.

    The XTEST extension is a minimal set of client and server extensions
    required to completely test the X11 server with no user intervention.
    This extension is not intended to support general journaling and
    playback of user actions.

    The RECORD extension supports the recording and reporting of all
    core X protocol and arbitrary X extension protocol."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXtst"
    xorg_mirror_path = "lib/libXtst-1.2.2.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.2.4", sha256="01366506aeb033f6dffca5326af85f670746b0cabbfd092aabefb046cf48c445")
    version("1.2.3", sha256="a0c83acce02d4923018c744662cb28eb0dbbc33b4adc027726879ccf68fbc2c2")
    version("1.2.2", sha256="221838960c7b9058cd6795c1c3ee8e25bae1c68106be314bc3036a4f26be0e6c")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxext@1.0.99.4:")
    depends_on("libxi")

    depends_on("recordproto@1.13.99.1:", type=("build", "link"))
    depends_on("xextproto@7.0.99.3:", type="build")
    depends_on("inputproto", type="build")
    depends_on("fixesproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
