# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xtrans(AutotoolsPackage, XorgPackage):
    """xtrans is a library of code that is shared among various X packages to
    handle network protocol transport in a modular fashion, allowing a
    single place to add new transport types.  It is used by the X server,
    libX11, libICE, the X font server, and related components."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libxtrans"
    xorg_mirror_path = "lib/xtrans-1.3.5.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.5.0", sha256="a806f8a92f879dcd0146f3f1153fdffe845f2fc0df9b1a26c19312b7b0a29c86")
    version("1.4.0", sha256="48ed850ce772fef1b44ca23639b0a57e38884045ed2cbb18ab137ef33ec713f9")
    version("1.3.5", sha256="b7a577c1b6c75030145e53b4793db9c88f9359ac49e7d771d4385d21b3e5945d")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
