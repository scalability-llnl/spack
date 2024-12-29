# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxres(AutotoolsPackage, XorgPackage):
    """libXRes - X-Resource extension client library."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXRes"
    xorg_mirror_path = "lib/libXres-1.0.7.tar.gz"

    license("custom")

    maintainers("wdconinc")

    version("1.2.2", sha256="8abce597ced4a7ab89032aee91f6f784d9960adc772b2b59f17e515cd4127950")
    version("1.2.1", sha256="918fb33c3897b389a1fbb51571c5c04c6b297058df286d8b48faa5af85e88bcc")
    version("1.2.0", sha256="5b62feee09f276d74054787df030fceb41034de84174abec6d81c591145e043a")
    version("1.0.7", sha256="488c9fa14b38f794d1f019fe62e6b06514a39f1a7538e55ece8faf22482fefcd")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxext")

    depends_on("xextproto", type="build")
    depends_on("resourceproto@1.0:", type="build", when="@1.0")
    depends_on("resourceproto@1.2:", type="build", when="@1.2")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
