# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xev(AutotoolsPackage, XorgPackage):
    """xev creates a window and then asks the X server to send it X11 events
    whenever anything happens to the window (such as it being moved,
    resized, typed in, clicked in, etc.).  You can also attach it to an
    existing window.  It is useful for seeing what causes events to occur
    and to display the information that they contain; it is essentially a
    debugging and development tool, and should not be needed in normal
    usage."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xev"
    xorg_mirror_path = "app/xev-1.2.2.tar.gz"

    license("MIT")

    version("1.2.6", sha256="e2e3527023017af3a9bfbef0a90f8e46ac354c506b51f0ee3834b30823e43b25")
    version("1.2.5", sha256="a948974ede621a8402ed9ea64f1ec83992285aa4fbb9d40b52985156c61a358a")
    version("1.2.4", sha256="6b1f94813f008a4ba45e0a2d4e1b64deaab1def56fabd7fac3621106cbaa3383")
    version("1.2.3", sha256="a3c5fbf339f43ba625a6d84e52ab1a7170581505ef498be6aa4e7bdfbd8d5cef")
    version("1.2.2", sha256="e4c0c7b6f411e8b9731f2bb10d729d167bd00480d172c28b62607a6ea9e45c57")

    depends_on("c", type="build")  # generated

    depends_on("libxrandr@1.2:")
    depends_on("libx11")

    depends_on("xproto@7.0.17:")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
