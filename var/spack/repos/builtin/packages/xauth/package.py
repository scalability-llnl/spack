# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xauth(AutotoolsPackage, XorgPackage):
    """The xauth program is used to edit and display the authorization
    information used in connecting to the X server."""

    homepage = "https://gitlab.freedesktop.org/xorg/app/xauth"
    xorg_mirror_path = "app/xauth-1.0.9.tar.gz"

    license("custom")

    version("1.1.2", sha256="84d27a1023d8da524c134f424b312e53cb96e08871f96868aa20316bfcbbc054")
    version("1.1.1", sha256="0f558ef33e76843cf16a78cd3910ef8ec0809bea85d14e091c559dcec092c671")
    version("1.1", sha256="e9fce796c8c5c9368594b9e8bbba237fb54b6615f5fd60e8d0a5b3c52a92c5ef")
    version("1.0.10", sha256="5196821221d824b9bc278fa6505c595acee1d374518a52217d9b64d3c63dedd0")
    version("1.0.9", sha256="0709070caf23ba2fb99536907b75be1fe31853999c62d3e87a6a8d26ba8a8cdb")

    depends_on("c", type="build")

    depends_on("libx11")
    depends_on("libxau")
    depends_on("libxext")
    depends_on("libxmu")

    depends_on("xproto@7.0.17:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")

    # TODO: add package for cmdtest test dependency
