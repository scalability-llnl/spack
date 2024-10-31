# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.build_systems import autotools, cmake
from spack.package import *


class Expat(AutotoolsPackage, CMakePackage):
    """Expat is an XML parser library written in C."""

    homepage = "https://libexpat.github.io/"
    url = "https://github.com/libexpat/libexpat/releases/download/R_2_2_9/expat-2.2.9.tar.bz2"

    license("MIT")

    version("2.6.3", sha256="b8baef92f328eebcf731f4d18103951c61fa8c8ec21d5ff4202fb6f2198aeb2d")
    # deprecate all releases before 2.6.3 because of security issues
    # CVE-2024-45490 (fixed in 2.6.3)
    # CVE-2024-45491 (fixed in 2.6.3)
    # CVE-2024-45492 (fixed in 2.6.3)
    version(
        "2.6.2",
        sha256="9c7c1b5dcbc3c237c500a8fb1493e14d9582146dd9b42aa8d3ffb856a3b927e0",
        deprecated=True,
    )
    # CVE-2024-28757 (fixed in 2.6.2)
    version(
        "2.6.1",
        sha256="4677d957c0c6cb2a3321101944574c24113b637c7ab1cf0659a27c5babc201fd",
        deprecated=True,
    )
    version(
        "2.6.0",
        sha256="ff60e6a6b6ce570ae012dc7b73169c7fdf4b6bf08c12ed0ec6f55736b78d85ba",
        deprecated=True,
    )
    # CVE-2023-52425 (fixed in 2.6.0)
    # CVE-2023-52426 (fixed in 2.6.0)
    version(
        "2.5.0",
        sha256="6f0e6e01f7b30025fa05c85fdad1e5d0ec7fd35d9f61b22f34998de11969ff67",
        deprecated=True,
    )
    # CVE-2022-43680 (fixed in 2.5.0)
    # CVE-2022-40674 (fixed in 2.4.9)
    version(
        "2.4.8",
        sha256="a247a7f6bbb21cf2ca81ea4cbb916bfb9717ca523631675f99b3d4a5678dcd16",
        deprecated=True,
    )
    version(
        "2.4.7",
        sha256="e149bdd8b90254c62b3d195da53a09bd531a4d63a963b0d8a5268d48dd2f6a65",
        deprecated=True,
    )
    # CVE-2022-25236 (fixed in 2.4.7)
    version(
        "2.4.6",
        sha256="ce317706b07cae150f90cddd4253f5b4fba929607488af5ac47bf2bc08e31f09",
        deprecated=True,
    )
    version(
        "2.4.5",
        sha256="fbb430f964c7a2db2626452b6769e6a8d5d23593a453ccbc21701b74deabedff",
        deprecated=True,
    )
    # CVE-2022-25235 (fixed in 2.4.5)
    # CVE-2022-25236 (fixed in 2.4.5)
    # CVE-2022-25313 (fixed in 2.4.5)
    # CVE-2022-25314 (fixed in 2.4.5)
    # CVE-2022-25315 (fixed in 2.4.5)
    version(
        "2.4.4",
        sha256="14c58c2a0b5b8b31836514dfab41bd191836db7aa7b84ae5c47bc0327a20d64a",
        deprecated=True,
    )
    # CVE-2022-23852 (fixed in 2.4.4)
    # CVE-2022-23990 (fixed in 2.4.4)
    version(
        "2.4.3",
        sha256="6f262e216a494fbf42d8c22bc841b3e117c21f2467a19dc4c27c991b5622f986",
        deprecated=True,
    )
    # CVE-2021-45960 (fixed in 2.4.3)
    # CVE-2021-46143 (fixed in 2.4.3)
    # CVE-2022-22822 (fixed in 2.4.3)
    # CVE-2022-22823 (fixed in 2.4.3)
    # CVE-2022-22824 (fixed in 2.4.3)
    # CVE-2022-22825 (fixed in 2.4.3)
    # CVE-2022-22826 (fixed in 2.4.3)
    # CVE-2022-22827 (fixed in 2.4.3)
    version(
        "2.4.1",
        sha256="2f9b6a580b94577b150a7d5617ad4643a4301a6616ff459307df3e225bcfbf40",
        deprecated=True,
    )
    version(
        "2.4.0",
        sha256="8c59142ef88913bc0a8b6e4c58970c034210ca552e6271f52f6cd6cce3708424",
        deprecated=True,
    )
    # CVE-2013-0340 (fixed in 2.4.0)
    version(
        "2.3.0",
        sha256="f122a20eada303f904d5e0513326c5b821248f2d4d2afbf5c6f1339e511c0586",
        deprecated=True,
    )
    version(
        "2.2.10",
        sha256="b2c160f1b60e92da69de8e12333096aeb0c3bf692d41c60794de278af72135a5",
        deprecated=True,
    )
    version(
        "2.2.9",
        sha256="f1063084dc4302a427dabcca499c8312b3a32a29b7d2506653ecc8f950a9a237",
        deprecated=True,
    )
    # CVE-2019-15903 (fixed in 2.2.8)
    # CVE-2018-20843 (fixed in 2.2.7)
    version(
        "2.2.6",
        sha256="17b43c2716d521369f82fc2dc70f359860e90fa440bea65b3b85f0b246ea81f2",
        deprecated=True,
    )
    version(
        "2.2.5",
        sha256="d9dc32efba7e74f788fcc4f212a43216fc37cf5f23f4c2339664d473353aedf6",
        deprecated=True,
    )
    # CVE-2017-11742 (fixed in 2.2.3)
    version(
        "2.2.2",
        sha256="4376911fcf81a23ebd821bbabc26fd933f3ac74833f74924342c29aad2c86046",
        deprecated=True,
    )
    # CVE-2017-9233 (fixed in 2.2.1)
    # CVE-2016-9063 (fixed in 2.2.1)
    # CVE-2016-5300 (fixed in 2.2.1, in part fixed earlier)
    # CVE-2012-0876 (fixed in 2.2.1, improved fix)
    version(
        "2.2.0",
        sha256="d9e50ff2d19b3538bd2127902a89987474e1a4db8e43a66a4d1a712ab9a504ff",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    build_system("autotools", "cmake", default="autotools")

    # Version 2.2.2 introduced a requirement for a high quality
    # entropy source.  "Older" linux systems (aka CentOS 7) do not
    # support get_random so we'll provide a high quality source via
    # libbsd.
    # There's no need for it in earlier versions, so 'conflict' if
    # someone's asking for an older version and also libbsd.
    # In order to install an older version, you'll need to add
    # `~libbsd`.
    variant(
        "libbsd",
        default=sys.platform == "linux",
        description="Use libbsd (for high quality randomness)",
    )

    variant(
        "shared",
        default=True,
        description="Build expat as shared if true, static if false",
        when="build_system=cmake",
    )

    depends_on("libbsd", when="@2.2.1:+libbsd")

    def url_for_version(self, version):
        url = "https://github.com/libexpat/libexpat/releases/download/R_{0}/expat-{1}.tar.bz2"
        return url.format(version.underscored, version.dotted)


class AutotoolsBuilder(autotools.AutotoolsBuilder):
    def configure_args(self):
        spec = self.spec
        args = ["--without-docbook", "--enable-static"]
        if spec.satisfies("+libbsd") and spec.satisfies("@2.2.1:"):
            args.append("--with-libbsd")
        return args


class CMakeBuilder(cmake.CMakeBuilder):
    def cmake_args(self):
        args = [
            self.define("EXPAT_BUILD_DOCS", False),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

        if self.spec.satisfies("+libbsd") and self.spec.satisfies("@2.2.1:"):
            args.append(self.define_from_variant("EXPAT_WITH_LIBBSD", "libbsd"))

        return args
