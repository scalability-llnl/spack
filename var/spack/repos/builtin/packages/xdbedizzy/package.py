# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xdbedizzy(AutotoolsPackage, XorgPackage):
    """xdbedizzy is a demo of the X11 Double Buffer Extension (DBE)
    creating a double buffered spinning scene."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xdbedizzy"
    xorg_mirror_path = "app/xdbedizzy-1.1.0.tar.gz"

    version("1.1.0", sha256="810e88b087b76f8b5993db4fc5165de3e5d29b0d4bf0e893750ee408fc7a5c0a")

    depends_on("c", type="build")  # generated

    depends_on("libx11")
    depends_on("libxext")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
