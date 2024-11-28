# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libnftnl(AutotoolsPackage):
    """A library for low-level interaction with nftables Netlink's API
    over libmnl."""

    homepage = "https://netfilter.org/projects/libmnl/"
    url = "https://netfilter.org/projects/libnftnl/files/libnftnl-1.2.7.tar.xz"

    license("GPL-2.0-or-later", checked_by="wdconinc")

    version("1.2.7", sha256="9122774f968093d5c0bacddd67de480f31fa4073405a7fc058a34b0f387aecb3")
    version("1.1.6", sha256="c1eb5a696fc1d4b3b412770586017bc01af93da3ddd25233d34a62979dee1eca")
    version("1.1.5", sha256="66de4d05227c0a1a731c369b193010d18a05b1185c2735211e0ecf658eeb14f3")
    version("1.1.4", sha256="c8c7988347adf261efac5bba59f8e5f995ffb65f247a88cc144e69620573ed20")

    depends_on("c", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("libmnl@1.0.0:")
    depends_on("libmnl@1.0.3:", when="@1.1.1:")
    depends_on("libmnl@1.0.4:", when="@1.1.7:")

    def url_for_version(self, version):
        if version >= Version("1.2.5"):
            return f"https://netfilter.org/projects/libnftnl/files/libnftnl-{version}.tar.xz"
        else:
            return f"https://netfilter.org/projects/libnftnl/files/libnftnl-{version}.tar.bz2"
