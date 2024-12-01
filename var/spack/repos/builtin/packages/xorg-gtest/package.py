# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XorgGtest(AutotoolsPackage, XorgPackage):
    """Provides a Google Test environment for starting and stopping
    a X server for testing purposes."""

    homepage = "https://people.freedesktop.org/~cndougla/xorg-gtest/"
    xorg_mirror_path = "test/xorg-gtest-0.7.1.tar.bz2"

    version("0.7.1", sha256="6cedc7904c698472783203bd686e777db120b808bb4052e451a822e437b72682")

    depends_on("cxx", type="build")  # generated

    depends_on("libx11")
    depends_on("libxi")
    depends_on("xorg-server")

    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    # TODO: may be missing evemu package?
    # TODO: what is the difference between xorg-gtest and googletest packages?
