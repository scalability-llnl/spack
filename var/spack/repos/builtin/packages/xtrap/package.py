# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xtrap(AutotoolsPackage, XorgPackage):
    """XTrap sample clients."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xtrap"
    xorg_mirror_path = "app/xtrap-1.0.2.tar.gz"

    version("1.0.3", sha256="c6b86b921a748acbf1d82590fbd9c4575f970220760088f0e0efac6fd93d6dc3")
    version("1.0.2", sha256="e8916e05bfb0d72a088aaaac0feaf4ad7671d0f509d1037fb3c0c9ea131b93d2")

    depends_on("c", type="build")  # generated

    depends_on("libx11")
    depends_on("libxtrap")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
