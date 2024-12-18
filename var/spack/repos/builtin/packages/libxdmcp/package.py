# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxdmcp(AutotoolsPackage, XorgPackage):
    """libXdmcp - X Display Manager Control Protocol library."""

    homepage = "https://gitlab.freedesktop.org/xorg/lib/libXdmcp"
    xorg_mirror_path = "lib/libXdmcp-1.1.2.tar.gz"

    license("MIT")

    maintainers("wdconinc")

    version("1.1.5", sha256="31a7abc4f129dcf6f27ae912c3eedcb94d25ad2e8f317f69df6eda0bc4e4f2f3")
    version("1.1.4", sha256="55041a8ff8992ab02777478c4b19c249c0f8399f05a752cb4a1a868a9a0ccb9a")
    version("1.1.3", sha256="2ef9653d32e09d1bf1b837d0e0311024979653fe755ad3aaada8db1aa6ea180c")
    version("1.1.2", sha256="6f7c7e491a23035a26284d247779174dedc67e34e93cc3548b648ffdb6fc57c0")

    depends_on("c", type="build")

    depends_on("xproto", type=("build", "link"))
    depends_on("pkgconfig", type="build")
    depends_on("util-macros", type="build")
    depends_on("libbsd", when="platform=linux")
