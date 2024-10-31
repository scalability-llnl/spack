# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxfixes(AutotoolsPackage, XorgPackage):
    """This package contains header files and documentation for the XFIXES
    extension.  Library and server implementations are separate."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXfixes"
    xorg_mirror_path = "lib/libXfixes-5.0.2.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    # Newer versions are blocked by https://github.com/spack/spack/issues/41688
    # version("6.0.1", sha256="e69eaa321173c748ba6e2f15c7cf8da87f911d3ea1b6af4b547974aef6366bec")
    # version("6.0.0", sha256="82045da5625350838390c9440598b90d69c882c324ca92f73af9f0e992cb57c7")
    version("5.0.3", sha256="9ab6c13590658501ce4bd965a8a5d32ba4d8b3bb39a5a5bc9901edffc5666570")
    version("5.0.2", sha256="ad8df1ecf3324512b80ed12a9ca07556e561b14256d94216e67a68345b23c981")

    depends_on("c", type="build")

    depends_on("libx11@1.6:")

    depends_on("xproto", type=("build", "link"))
    depends_on("fixesproto@5.0:", type=("build", "link"), when="@5")
    # depends_on("fixesproto@6.0:", type=("build", "link"), when="@6")
    depends_on("xextproto", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
