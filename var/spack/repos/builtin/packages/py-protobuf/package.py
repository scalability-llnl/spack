# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyProtobuf(PythonPackage):
    """Protocol buffers are Google's language-neutral, platform-neutral,
    extensible mechanism for serializing structured data - think XML, but
    smaller, faster, and simpler. You define how you want your data to be
    structured once, then you can use special generated source code to easily
    write and read your structured data to and from a variety of data streams
    and using a variety of languages."""

    homepage = "https://developers.google.com/protocol-buffers/"
    pypi = "protobuf/protobuf-3.11.0.tar.gz"

    version("5.28.2", sha256="59379674ff119717404f7454647913787034f03fe7049cbef1d74a97bb4593f0")
    version("5.27.5", sha256="7fa81bc550201144a32f4478659da06e0b2ebe4d5303aacce9a202a1c3d5178d")
    version("5.26.1", sha256="8ca2a1d97c290ec7b16e4e5dff2e5ae150cc1582f55b5ab300d45cb0dfa90e51")
    version("4.25.3", sha256="25b5d0b42fd000320bd7830b349e3b696435f3b329810427a6bcce6a5492cc5c")
    version("4.24.3", sha256="12e9ad2ec079b833176d2921be2cb24281fa591f0b119b208b788adc48c2561d")
    version("4.23.3", sha256="7a92beb30600332a52cdadbedb40d33fd7c8a0d7f549c440347bc606fb3fe34b")
    version("4.21.9", sha256="61f21493d96d2a77f9ca84fefa105872550ab5ef71d21c458eb80edcf4885a99")
    version("4.21.7", sha256="71d9dba03ed3432c878a801e2ea51e034b0ea01cf3a4344fb60166cb5f6c8757")
    version("4.21.5", sha256="eb1106e87e095628e96884a877a51cdb90087106ee693925ec0a300468a9be3a")
    version("3.20.3", sha256="2e3427429c9cffebf259491be0af70189607f365c2f41c7c3764af6f337105f2")
    version("3.20.2", sha256="712dca319eee507a1e7df3591e639a2b112a2f4a62d40fe7832a16fd19151750")
    version("3.20.1", sha256="adc31566d027f45efe3f44eeb5b1f329da43891634d61c75a5944e9be6dd42c9")
    version("3.20.0", sha256="71b2c3d1cd26ed1ec7c8196834143258b2ad7f444efff26fdc366c6f5e752702")
    version("3.19.4", sha256="9df0c10adf3e83015ced42a9a7bd64e13d06c4cf45c340d2c63020ea04499d0a")
    version("3.19.3", sha256="d975a6314fbf5c524d4981e24294739216b5fb81ef3c14b86fb4b045d6690907")
    version("3.19.2", sha256="392f928e57054520276fdad412e045910268224b9446c218702e577d26eaf557")
    version("3.19.1", sha256="62a8e4baa9cb9e064eb62d1002eca820857ab2138440cb4b3ea4243830f94ca7")
    version("3.19.0", sha256="6a1dc6584d24ef86f5b104bcad64fa0fe06ed36e5687f426e0445d363a041d18")
    version("3.18.1", sha256="1c9bb40503751087300dd12ce2e90899d68628977905c76effc48e66d089391e")
    version("3.17.3", sha256="72804ea5eaa9c22a090d2803813e280fb273b62d5ae497aaf3553d141c4fdd7b")
    version("3.17.2", sha256="5a3450acf046716e4a4f02a3f7adfb7b86f1b5b3ae392cec759915e79538d40d")
    version("3.17.1", sha256="25bc4f1c23aced9b3a9e70eef7f03e63bcbd6cfbd881a91b5688412dce8992e1")
    version("3.17.0", sha256="05dfe9319939a8473c21b469f34f6486646e54fb8542637cf7ed8e2fbfe21538")
    version("3.16.0", sha256="228eecbedd46d75010f1e0f8ce34dbcd11ae5a40c165a9fc9d330a58aa302818")
    version("3.15.8", sha256="0277f62b1e42210cafe79a71628c1d553348da81cbd553402a7f7549c50b11d0")
    version("3.15.7", sha256="2d03fc2591543cd2456d0b72230b50c4519546a8d379ac6fd3ecd84c6df61e5d")
    version("3.15.6", sha256="2b974519a2ae83aa1e31cff9018c70bbe0e303a46a598f982943c49ae1d4fcd3")
    version("3.15.5", sha256="be8a929c6178bb6cbe9e2c858be62fa08966a39ae758a8493a88f0ed1efb6097")
    version("3.15.1", sha256="824dbae3390fcc3ea1bf96748e6da951a601802894cf7e1465e72b4732538cab")
    version("3.13.0", sha256="6a82e0c8bb2bf58f606040cc5814e07715b2094caeba281e2e7d0b0e2e397db5")
    version("3.12.2", sha256="49ef8ab4c27812a89a76fa894fe7a08f42f2147078392c0dee51d4a444ef6df5")
    version("3.11.2", sha256="3d7a7d8d20b4e7a8f63f62de2d192cfd8b7a53c56caba7ece95367ca2b80c574")
    version("3.11.1", sha256="aecdf12ef6dc7fd91713a6da93a86c2f2a8fe54840a3b1670853a2b7402e77c9")
    version("3.11.0", sha256="97b08853b9bb71512ed52381f05cf2d4179f4234825b505d8f8d2bb9d9429939")
    version("3.10.0", sha256="db83b5c12c0cd30150bb568e6feb2435c49ce4e68fe2d7b903113f0e221e58fe")
    version("3.9.2", sha256="843f498e98ad1469ad54ecb4a7ccf48605a1c5d2bd26ae799c7a2cddab4a37ec")
    version("3.9.1", sha256="d831b047bd69becaf64019a47179eb22118a50dd008340655266a906c69c6417")
    version("3.8.0", sha256="8c61cc8a76e9d381c665aecc5105fa0f1878cf7db8b5cd17202603bcb386d0fc")
    version("3.7.1", sha256="21e395d7959551e759d604940a115c51c6347d90a475c9baf471a1a86b5604a9")
    version("3.6.1", sha256="1489b376b0f364bcc6f89519718c057eb191d7ad6f1b395ffd93d1aa45587811")
    version("3.6.0", sha256="a37836aa47d1b81c2db1a6b7a5e79926062b5d76bd962115a0e615551be2b48d")
    version("3.5.2", sha256="09879a295fd7234e523b62066223b128c5a8a88f682e3aff62fb115e4a0d8be0")
    version("3.5.1", sha256="95b78959572de7d7fafa3acb718ed71f482932ddddddbd29ba8319c10639d863")
    version("3.4.0", sha256="ef02609ef445987976a3a26bff77119c518e0915c96661c3a3b17856d0ef6374")
    version("3.3.0", sha256="1cbcee2c45773f57cb6de7ee0eceb97f92b9b69c0178305509b162c0160c1f04")
    version("3.0.0", sha256="ecc40bc30f1183b418fe0ec0c90bc3b53fa1707c4205ee278c6b90479e5b6ff5")

    depends_on("c", type="build")

    depends_on("python", type=("build", "link", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-six@1.9:", when="@3.0:3.17", type=("build", "run"))

    # Minor version must match protobuf
    for ver in range(26, 29):
        depends_on(f"protobuf@3.{ver}", when=f"@5.{ver}")
    for ver in range(21, 26):
        depends_on(f"protobuf@3.{ver}", when=f"@4.{ver}")
    for ver in range(0, 21):
        depends_on(f"protobuf@3.{ver}", when=f"@3.{ver}")

    conflicts("%gcc@14:", when="@:4.24.3")
