# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class RdmaCore(CMakePackage):
    """RDMA core userspace libraries and daemons"""

    homepage = "https://github.com/linux-rdma/rdma-core"
    url = "https://github.com/linux-rdma/rdma-core/releases/download/v17.1/rdma-core-17.1.tar.gz"
    libraries = ["librdmacm.so"]
    keep_werror = "all"

    license("GPL-2.0-only OR BSD-2-Clause")

    version("52.0", sha256="1f0ce5f2462c982b20d21156707076278807a7adf4d10e9142f3be4bec1b2b83")
    version("51.0", sha256="0a4a55b1351356c2750f26ec9010e8c7370402a13c95799cb8b447cf0134dd61")
    version("50.0", sha256="405b9dd551120da9d1b8944c5ad24ab1f478fb13caedf5bf0d47053a6d6e20cc")
    version("49.1", sha256="2e531d398073dd7ed28d95c94fa698e1a831952b508e9af93e36644dcd399936")
    version("49.0", sha256="953546ad2b179f9ce68dc21eb1eb26003098ea1bf0f87a4baed45bcea134b2b4")
    version("47.1", sha256="5d92058473b90be231c17220ce456837cb6da9975de498bd63b9660baa25afd6")
    version("46.2", sha256="c59c3c79fbae6038d7c6d16b37132e433e19f4a86d41341c6b7974b830b0d4fa")
    version("45.3", sha256="6cb2bf25927dfbaf5acba9ae755f11beabc2983720d2eb2c4547a490bbf2ba81")
    version("44.4", sha256="7de3f50d3e11a519494efc88250ca6aef992c072d772113eb81b64e69d03e46b")
    version("43.4", sha256="2a3155774947ef602f50a3d41d642d09348e4c55411633743985bf8c83d0b9bf")
    version("42.5", sha256="d6f8976d4cc295ad6eba09a3dcad8cdb26f36556dbee81f41965f3761f3ac093")
    version("41.5", sha256="70e2a5f1d552398c09c02e660fa63c476c05c47c8b47b3fd2f8661503f35aed8")
    version("41.0", sha256="e0b7deb8a71f229796a0cfe0fa25192c530cd3d86b755b6b28d1a5986a77507b")
    version("40.0", sha256="8844edb71311e3212e55e28fa4bdc6e06dd6c7b839ed56ee4b606e4220d94ee8")
    version("39.1", sha256="32ccd5c990d34605b6e996de991528ef01d278ad06bcf62ccf8a32edb118c335")
    version("39.0", sha256="f6eaf0de9fe386e234e00a18a553f591143f50e03342c9fdd703fa8747bf2378")
    version("38.2", sha256="34ed8e51512fae1597421931751dcf7119da501bcf8291c1bd18e4f9e0f2efd5")
    version("37.3", sha256="b7455ed0f71661ef4bce3e8e7a6b608a48e1e946b01dad612308d68e846c5bd2")
    version("36.4", sha256="0eb177093bf38995904e1edcf214460679c639a5bdcf5ece8bf1fa7201c92ac5")
    version("35.4", sha256="cae64afdad6fca65eb6fb07c6ea6e7e513482e452a7840548e682d822b6731e4")
    version("34.5", sha256="d1431b090b528525715eecce849d506a7bbabc0bb6996d4c413e1256df90d8ad")
    version("34.0", sha256="3d9ccf66468cf78f4c39bebb8bd0c5eb39150ded75f4a88a3455c4f625408be8")
    version("33.6", sha256="f4e3d84c78bfef99d7968e8847fe9f33922e574ddf77a7f9e340a6e64bfc68d1")
    version("33.1", sha256="d179b102bec551ce62265ed463d1095fb2ae9baff604261ad63327fcd20650e5")
    version("32.5", sha256="8c51dcd015fd1207b0e0aada9711737be380e746528cd408872f584a6c0901ba")
    version("32.0", sha256="8197e20a59990b9b06a2e4c83f4a96802fc080ec1669392b643b59b6023931fc")
    version("31.7", sha256="1d5d824b3dfaefbd513ffd3ce080c46ed9c6e4aff36336048745e4a99ec5f230")
    version("31.0", sha256="51ae9a3ab81cd6834436813fafc310c8b7007feae9d09a53fdd5c169e648d50b")
    version("30.6", sha256="2eaa0a8c7fd8ef63148645c16ef675f8269784eda5f266f826bbade8b50e6160")
    version("30.0", sha256="23e1bd2d7b38149a1621ee577a3428ac652e305adb8e0eee923cbe71356a9bf9")
    version("29.6", sha256="3d31cbd61dcfc5d343dc1259cb0f56765bc677da41fca8a62a89ba0c3097a743")
    version("28.7", sha256="0264f9a7475652e4338718f87d7ee82e772fd4c373b8b338b983852c48489913")
    version("28.1", sha256="d9961fd9b0867f17cb6a30a728562f00528b63dd72d1168d838220ab44e5c713")
    version("27.7", sha256="2703c2f8b5c348f383aa9b876e784553c6cc28cfa711709159fb9d7c1726e9e4")
    version("27.1", sha256="39eeb3ab5f868ef3a5f7623d1ee69adca04efabe2a37de8080f354b8f4ef0ad7")
    version("26.8", sha256="291700ba03df7d2fd9341eab2580842ba67b5a45ef13e9cd80eb39e2913016e3")
    version("26.2", sha256="115087ab438bea3530a0d520640f1eeb5872b902ee2263acf83dcc7835d296c6")
    version("25.10", sha256="f19987fbc048dadac6be769f8b0a4e04e3e152d82ef5715a156cf576ae17c941")
    version("25.4", sha256="f622491b0aac819f05c73174e0c7a9e630cc02fc0914d5ba1bb1d87fc4d313fd")
    version("24.9", sha256="523377f51357aac032926feb9aa4905dc128b4f6cb31e9fb3e9c6d13ca940221")
    version("24.3", sha256="3a02d2d864258acc763849c635c815e3fa6a798a1464511cd3a2a370ddd6ee89")
    version("23.9", sha256="8329cf13c3d4a422caf51c6aa9059c969ad9b9a3242b5452fd33baf3052fdce7")
    version("23.4", sha256="6bfe009e9a382085def3b004d9396f7255a2e0c90c36647d1df0b86773d21a79")
    version("22.4", sha256="efffaf1df775fae3e06109da7c62f6a25beee40865a2dce4911e923c40d752a6")
    version("20.11", sha256="24534237ee8857f612ee43e840f938c4af3d73593a54d8cc7097ea6583095b48")
    version("20", sha256="bc846989f807cd2b03643927d2b99fbf6f849cb1e766ab49bc9e81ce769d5421")
    version("19.11", sha256="c4f6f5741c38e1ea2b7e3d02fa8190cd31dadf9d9a7d4dfdf024e31fcbd4f528")
    version("18.12", sha256="024159919b6586d6fbe447d6a1d7601e402a7ffb428d68e88672aff1bcc12e3f")
    version("17.11", sha256="47db6d611c39e6655bfd808222caab925ac6ff9a245e24da9156254dd5813032")
    version("17.1", sha256="b47444b7c05d3906deb8771eec3e634984dd83f5e620d5e37d3a83f74f0cc1ba")
    version("13", sha256="e5230fd7cda610753ad1252b40a28b1e9cf836423a10d8c2525b081527760d97")

    depends_on("c", type="build")  # generated

    patch("libdrm.patch", when="@34:")

    variant(
        "static",
        default=True,
        description="Produce static libraries along with usual shared libraries.",
    )
    variant("pyverbs", default=True, description="Build with support for pyverbs")
    variant("man_pages", default=True, description="Build with support for man pages")

    depends_on("pkgconfig", type="build")
    depends_on("py-docutils", when="+man_pages", type="build")
    depends_on("libnl")
    conflicts("platform=darwin", msg="rdma-core requires FreeBSD or Linux")
    conflicts("%intel", msg="rdma-core cannot be built with intel (use gcc instead)")

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d+(?:\.\d+)?)", lib)
        if match and match.group(1) == "0":
            # On some systems there is a truncated shared library name that does not
            # sufficient version information, return a clear indicator of that
            return "unknown_ver"

        return match.group(1) if match else None

    # NOTE: specify CMAKE_INSTALL_RUNDIR explicitly to prevent rdma-core from
    #       using the spack staging build dir (which may be a very long file
    #       system path) as a component in compile-time static strings such as
    #       IBACM_SERVER_PATH.
    def cmake_args(self):
        cmake_args = [
            "-DCMAKE_INSTALL_SYSCONFDIR={0}".format(self.spec.prefix.etc),
            "-DCMAKE_INSTALL_RUNDIR=/var/run",
        ]

        cmake_args.append(self.define_from_variant("ENABLE_STATIC", "static"))

        if self.spec.satisfies("~pyverbs"):
            cmake_args.append("-DNO_PYVERBS=1")
        if self.spec.satisfies("~man_pages"):
            cmake_args.append("-DNO_MAN_PAGES=1")

        return cmake_args
