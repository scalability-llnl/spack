# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xplsprinters(AutotoolsPackage, XorgPackage):
    """List Xprint printers."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xplsprinters"
    xorg_mirror_path = "app/xplsprinters-1.0.1.tar.gz"

    version("1.0.1", sha256="33377e499429ce3e100fbd7b59153c87ad79bf55872561db08419f69cac4fbfd")

    depends_on("c", type="build")  # generated

    depends_on("libxp")
    depends_on("libxprintutil")
    depends_on("libx11")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
