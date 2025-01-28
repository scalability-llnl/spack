# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import platform
import re

from spack.package import *
from spack.util.prefix import Prefix

# If you need to add a new version, please be aware that:
#  - versions in the following dict are automatically added to the package
#  - version tuple must be in the form (checksum, url)
#  - checksum must be sha256
#  - package key must be in the form '{os}-{arch}' where 'os' is in the
#    format returned by platform.system() and 'arch' by platform.machine()

_versions = {
    "21.0.3_9": {
        "Linux-x86_64": (
            "fffa52c22d797b715a962e6c8d11ec7d79b90dd819b5bc51d62137ea4b22a340",
            "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.3%2B9/OpenJDK21U-jdk_x64_linux_hotspot_21.0.3_9.tar.gz",
        ),
        "Linux-aarch64": (
            "7d3ab0e8eba95bd682cfda8041c6cb6fa21e09d0d9131316fd7c96c78969de31",
            "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.3%2B9/OpenJDK21U-jdk_aarch64_linux_hotspot_21.0.3_9.tar.gz",
        ),
        "Darwin-arm64": (
            "b6be6a9568be83695ec6b7cb977f4902f7be47d74494c290bc2a5c3c951e254f",
            "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21.0.3%2B9/OpenJDK21U-jdk_aarch64_mac_hotspot_21.0.3_9.tar.gz",
        ),
    },
    "21.0.0_35": {
        "Linux-x86_64": (
            "82f64c53acaa045370d6762ebd7441b74e6fda14b464d54d1ff8ca941ec069e6",
            "https://github.com/adoptium/temurin21-binaries/releases/download/jdk-21%2B35/OpenJDK21U-jdk_x64_linux_hotspot_21_35.tar.gz",
        )
    },
    "17.0.11_9": {
        "Linux-x86_64": (
            "aa7fb6bb342319d227a838af5c363bfa1b4a670c209372f9e6585bd79da6220c",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.11%2B9/OpenJDK17U-jdk_x64_linux_hotspot_17.0.11_9.tar.gz",
        ),
        "Linux-aarch64": (
            "a900acf3ae56b000afc35468a083b6d6fd695abec87a8abdb02743d5c72f6d6d",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.11%2B9/OpenJDK17U-jdk_aarch64_linux_hotspot_17.0.11_9.tar.gz",
        ),
        "Darwin-arm64": (
            "09a162c58dd801f7cfacd87e99703ed11fb439adc71cfa14ceb2d3194eaca01c",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.11%2B9/OpenJDK17U-jdk_aarch64_mac_hotspot_17.0.11_9.tar.gz",
        ),
    },
    "17.0.8.1_1": {
        "Linux-x86_64": (
            "c25dfbc334068a48c19c44ce39ad4b8427e309ae1cfa83f23c102e78b8a6dcc0",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.8.1%2B1/OpenJDK17U-jdk_x64_linux_hotspot_17.0.8.1_1.tar.gz",
        ),
        "Linux-aarch64": (
            "eefd3cf3b3dd47ff269fa5b5c10b5e096b163f4e9c1810023abdbc00dc6cc304",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.8.1%2B1/OpenJDK17U-jdk_aarch64_linux_hotspot_17.0.8.1_1.tar.gz",
        ),
        "Darwin-x86_64": (
            "18be56732c1692ef131625d814dcb02ee091a43fdd6f214a33d87cc14842fc3f",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.8.1%2B1/OpenJDK17U-jdk_x64_mac_hotspot_17.0.8.1_1.tar.gz",
        ),
        "Darwin-arm64": (
            "2e95eed48650f00650e963c8213b6c6ecda54458edf8d254ebc99d6a6966ffad",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.8.1%2B1/OpenJDK17U-jdk_aarch64_mac_hotspot_17.0.8.1_1.tar.gz",
        ),
    },
    "17.0.5_8": {
        "Linux-x86_64": (
            "482180725ceca472e12a8e6d1a4af23d608d78287a77d963335e2a0156a020af",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.5%2B8/OpenJDK17U-jdk_x64_linux_hotspot_17.0.5_8.tar.gz",
        ),
        "Linux-aarch64": (
            "1c26c0e09f1641a666d6740d802beb81e12180abaea07b47c409d30c7f368109",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.5%2B8/OpenJDK17U-jdk_aarch64_linux_hotspot_17.0.5_8.tar.gz",
        ),
    },
    "17.0.4.1_1": {
        "Linux-x86_64": (
            "5fbf8b62c44f10be2efab97c5f5dbf15b74fae31e451ec10abbc74e54a04ff44",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.4.1%2B1/OpenJDK17U-jdk_x64_linux_hotspot_17.0.4.1_1.tar.gz",
        ),
        "Linux-aarch64": (
            "3c7460de77421284b38b4e57cb1bd584a6cef55c34fc51a12270620544de2b8a",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.4.1%2B1/OpenJDK17U-jdk_aarch64_linux_hotspot_17.0.4.1_1.tar.gz",
        ),
        "Linux-ppc64le": (
            "cbedd0a1428b3058d156e99e8e9bc8769e0d633736d6776a4c4d9136648f2fd1",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.4.1%2B1/OpenJDK17U-jdk_ppc64le_linux_hotspot_17.0.4.1_1.tar.gz",
        ),
        "Darwin-x86_64": (
            "ac21a5a87f7cfa00212ab7c41f7eb80ca33640d83b63ad850be811c24095d61a",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.4.1%2B1/OpenJDK17U-jdk_x64_mac_hotspot_17.0.4.1_1.tar.gz",
        ),
        "Darwin-arm64": (
            "3a976943a9e6a635e68e2b06bd093fc096aad9f5894acda673d3bea0cb3a6f38",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.4.1%2B1/OpenJDK17U-jdk_aarch64_mac_hotspot_17.0.4.1_1.tar.gz",
        ),
    },
    "17.0.3_7": {
        "Linux-x86_64": (
            "81f5bed21077f9fbb04909b50391620c78b9a3c376593c0992934719c0de6b73",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.3%2B7/OpenJDK17U-jdk_x64_linux_hotspot_17.0.3_7.tar.gz",
        ),
        "Linux-aarch64": (
            "2e3c19c1707205c6b90cc04b416e8d83078ed98417d5a69dce3cf7dc0d7cfbca",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.3%2B7/OpenJDK17U-jdk_aarch64_linux_hotspot_17.0.3_7.tar.gz",
        ),
        "Linux-ppc64le": (
            "a04587018c9719dca21073f19d56b335c4985f41afe7d99b24852c1a94b917e5",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.3%2B7/OpenJDK17U-jdk_ppc64le_linux_hotspot_17.0.3_7.tar.gz",
        ),
        "Darwin-x86_64": (
            "a5db5927760d2864316354d98ff18d18bec2e72bfac59cd25a416ed67fa84594",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.3%2B7/OpenJDK17U-jdk_x64_mac_hotspot_17.0.3_7.tar.gz",
        ),
        "Darwin-arm64": (
            "ff42be4d7a348d0d7aee07749e4daec9f427dcc7eb46b343f8131e8f3906c05b",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.3%2B7/OpenJDK17U-jdk_aarch64_mac_hotspot_17.0.3_7.tar.gz",
        ),
    },
    "17.0.2_8": {
        "Linux-x86_64": (
            "288f34e3ba8a4838605636485d0365ce23e57d5f2f68997ac4c2e4c01967cd48",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.2%2B8/OpenJDK17U-jdk_x64_linux_hotspot_17.0.2_8.tar.gz",
        ),
        "Linux-aarch64": (
            "302caf29f73481b2b914ba2b89705036010c65eb9bc8d7712b27d6e9bedf6200",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.2%2B8/OpenJDK17U-jdk_aarch64_linux_hotspot_17.0.2_8.tar.gz",
        ),
        "Linux-ppc64le": (
            "532d831d6a977e821b7331ecf9ed995e5bbfe76f18a1b00ffa8dbb3a4e2887de",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.2%2B8/OpenJDK17U-jdk_ppc64le_linux_hotspot_17.0.2_8.tar.gz",
        ),
        "Darwin-x86_64": (
            "3630e21a571b7180876bf08f85d0aac0bdbb3267b2ae9bd242f4933b21f9be32",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.2%2B8/OpenJDK17U-jdk_x64_mac_hotspot_17.0.2_8.tar.gz",
        ),
        "Darwin-arm64": (
            "157518e999d712b541b883c6c167f8faabbef1d590da9fe7233541b4adb21ea4",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17.0.2%2B8/OpenJDK17U-jdk_aarch64_mac_hotspot_17.0.2_8.tar.gz",
        ),
    },
    "17.0.0_35": {
        "Linux-x86_64": (
            "6f1335d9a7855159f982dac557420397be9aa85f3f7bc84e111d25871c02c0c7",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17%2B35/OpenJDK17-jdk_x64_linux_hotspot_17_35.tar.gz",
        ),
        "Linux-aarch64": (
            "e08e6d8c84da28a2c49ccd511f8835c329fbdd8e4faff662c58fa24cca74021d",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17%2B35/OpenJDK17-jdk_aarch64_linux_hotspot_17_35.tar.gz",
        ),
        "Linux-ppc64le": (
            "2e58f76fd332b73f323e47c73d0a81b76739debab067e7a32ed6abd73fd64c57",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17%2B35/OpenJDK17-jdk_ppc64le_linux_hotspot_17_35.tar.gz",
        ),
        "Darwin-x86_64": (
            "e9de8b1b62780fe99270a5b30f0645d7a91eded60438bcf836a05fa7b93c182f",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17%2B35/OpenJDK17-jdk_x64_mac_hotspot_17_35.tar.gz",
        ),
        "Darwin-arm64": (
            "910bb88543211c63298e5b49f7144ac4463f1d903926e94a89bfbf10163bbba1",
            "https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17%2B35/OpenJDK17-jdk_aarch64_mac_hotspot_17_35.tar.gz",
        ),
    },
    "16.0.2": {
        "Linux-x86_64": (
            "6c714ded7d881ca54970ec949e283f43d673a142fda1de79b646ddd619da9c0c",
            "https://download.java.net/java/GA/jdk16.0.2/d4a915d82b4c4fbb9bde534da945d746/7/GPL/openjdk-16.0.2_linux-x64_bin.tar.gz",
        ),
        "Linux-aarch64": (
            "1ffb9c7748334945d9056b3324de3f797d906fce4dad86beea955153aa1e28fe",
            "https://download.java.net/java/GA/jdk16.0.2/d4a915d82b4c4fbb9bde534da945d746/7/GPL/openjdk-16.0.2_linux-aarch64_bin.tar.gz",
        ),
    },
    "15.0.2": {
        "Linux-x86_64": (
            "91ac6fc353b6bf39d995572b700e37a20e119a87034eeb939a6f24356fbcd207",
            "https://download.java.net/java/GA/jdk15.0.2/0d1cfde4252546c6931946de8db48ee2/7/GPL/openjdk-15.0.2_linux-x64_bin.tar.gz",
        ),
        "Linux-aarch64": (
            "3958f01858f9290c48c23e7804a0af3624e8eca6749b085c425df4c4f2f7dcbc",
            "https://download.java.net/java/GA/jdk15.0.2/0d1cfde4252546c6931946de8db48ee2/7/GPL/openjdk-15.0.2_linux-aarch64_bin.tar.gz",
        ),
    },
    "11.0.23_9": {
        "Linux-x86_64": (
            "23e47ea7a3015be3240f21185fd902adebdcf76530757c9b482c7eb5bd3417c2",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.23%2B9/OpenJDK11U-jdk_x64_linux_hotspot_11.0.23_9.tar.gz",
        ),
        "Linux-aarch64": (
            "e00476a7be3c4adfa9b3d55d30768967fd246a8352e518894e183fa444d4d3ce",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.23%2B9/OpenJDK11U-jdk_aarch64_linux_hotspot_11.0.23_9.tar.gz",
        ),
        "Darwin-arm64": (
            "49122443bdeab2c9f468bd400f58f85a9ea462846faa79084fd6fd786d9b492d",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.23%2B9/OpenJDK11U-jdk_aarch64_mac_hotspot_11.0.23_9.tar.gz",
        ),
    },
    "11.0.20.1_1": {
        "Linux-x86_64": (
            "398a64bff002f0e3b0c01ecd24a1a32c83cb72a5255344219e9757d4ddd9f857",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.20.1%2B1/OpenJDK11U-jdk_x64_linux_hotspot_11.0.20.1_1.tar.gz",
        ),
        "Linux-aarch64": (
            "69d39682c4a2fac294a9eaacbf62c26d3c8a2f9123f1b5d287498a5472c6b672",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.20.1%2B1/OpenJDK11U-jdk_aarch64_linux_hotspot_11.0.20.1_1.tar.gz",
        ),
        "Darwin-x86_64": (
            "42fd1373ee3f7c24f13551be20c8a5ae7ade778f83c45476ea333b2e3e025267",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.20.1%2B1/OpenJDK11U-jdk_x64_mac_hotspot_11.0.20.1_1.tar.gz",
        ),
        "Darwin-arm64": (
            "d36abd2f8a8cd2c73a7893306d65a5ae03eaa73565c1fc197a69d1d6fb02405e",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.20.1%2B1/OpenJDK11U-jdk_aarch64_mac_hotspot_11.0.20.1_1.tar.gz",
        ),
    },
    "11.0.17_8": {
        "Linux-x86_64": (
            "b8d46ed08ef4859476fe6421a7690d899ed83dce63f13fd894f994043177ef3c",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.17%2B8/OpenJDK11U-jdk_x64_linux_hotspot_11.0.17_8.tar.gz",
        ),
        "Linux-aarch64": (
            "d18b5dd73fce9edd5c58f623a1173f9ee2d45023836b8753b96beae51673a432",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.17%2B8/OpenJDK11U-jdk_aarch64_linux_hotspot_11.0.17_8.tar.gz",
        ),
        "Linux-ppc64le": (
            "18c636bd103e240d29cdb30d7867720ea9fb9ff7c645738bfb4d5b8027269263",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.17%2B8/OpenJDK11U-jdk_ppc64le_linux_hotspot_11.0.17_8.tar.gz",
        ),
        "Darwin-arm64": (
            "79b18cbd398b67a52ebaf033dfca15c7af4c1a84ec5fa68a88f3bf742bb082f7",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.17%2B8/OpenJDK11U-jdk_aarch64_mac_hotspot_11.0.17_8.tar.gz",
        ),
    },
    "11.0.16.1_1": {
        "Linux-x86_64": (
            "5f6b513757d386352cf91514ed5859d1ab59364b4453e1f1c57152ba2039b8e2",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.16.1%2B1/OpenJDK11U-jdk_x64_linux_hotspot_11.0.16.1_1.tar.gz",
        ),
        "Linux-aarch64": (
            "2b89cabf0ce1c2cedadd92b798d6e9056bc27c71a06f5ba24ede5dc9c316e3e8",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.16.1%2B1/OpenJDK11U-jdk_aarch64_linux_hotspot_11.0.16.1_1.tar.gz",
        ),
        "Linux-ppc64le": (
            "b18877871eda801ccb99bb34c5d7d77fccf6adad02514110c21389632ec91024",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.16.1%2B1/OpenJDK11U-jdk_ppc64le_linux_hotspot_11.0.16.1_1.tar.gz",
        ),
        "Darwin-x86_64": (
            "723548e36e0b3e0a5a2f36a38b22ea825d3004e26054a0e254854adc57045352",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.16.1%2B1/OpenJDK11U-jdk_x64_mac_hotspot_11.0.16.1_1.tar.gz",
        ),
        "Darwin-arm64": (
            "1953f06702d45eb54bae3ccf453b57c33de827015f5623a2dfc16e1c83e6b0a1",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.16.1%2B1/OpenJDK11U-jdk_aarch64_mac_hotspot_11.0.16.1_1.tar.gz",
        ),
    },
    "11.0.15_10": {
        "Linux-x86_64": (
            "5fdb4d5a1662f0cca73fec30f99e67662350b1fa61460fa72e91eb9f66b54d0b",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.15%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.15_10.tar.gz",
        ),
        "Linux-aarch64": (
            "999fbd90b070f9896142f0eb28354abbeb367cbe49fd86885c626e2999189e0a",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.15%2B10/OpenJDK11U-jdk_aarch64_linux_hotspot_11.0.15_10.tar.gz",
        ),
        "Linux-ppc64le": (
            "a8fba686f6eb8ae1d1a9566821dbd5a85a1108b96ad857fdbac5c1e4649fc56f",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.15%2B10/OpenJDK11U-jdk_ppc64le_linux_hotspot_11.0.15_10.tar.gz",
        ),
        "Darwin-x86_64": (
            "ebd8b9553a7b4514599bc0566e108915ce7dc95d29d49a9b10b8afe4ab7cc9db",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.15%2B10/OpenJDK11U-jdk_x64_mac_hotspot_11.0.15_10.tar.gz",
        ),
        "Darwin-arm64": (
            "e84143a6c633a26aeefcb1fd5ad8dfb9e952cfec2a1af5c9d9b69f2390990dac",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.15%2B10/OpenJDK11U-jdk_aarch64_mac_hotspot_11.0.15_10.tar.gz",
        ),
    },
    "11.0.14.1_1": {
        "Linux-x86_64": (
            "43fb84f8063ad9bf6b6d694a67b8f64c8827552b920ec5ce794dfe5602edffe7",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.14.1%2B1/OpenJDK11U-jdk_x64_linux_hotspot_11.0.14.1_1.tar.gz",
        ),
        "Linux-aarch64": (
            "79572f5172c6a040591d34632f98a20ed148702bbce2f57649e8ac01c0d2e3db",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.14.1%2B1/OpenJDK11U-jdk_aarch64_linux_hotspot_11.0.14.1_1.tar.gz",
        ),
        "Linux-ppc64le": (
            "9750e11721282a9afd18a07743f19c699b2b71ce20d02f3f0a906088b9ae6d9a",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.14.1%2B1/OpenJDK11U-jdk_ppc64le_linux_hotspot_11.0.14.1_1.tar.gz",
        ),
        "Darwin-x86_64": (
            "8c69808f5d9d209b195575e979de0e43cdf5d0f1acec1853a569601fe2c1f743",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.14.1%2B1/OpenJDK11U-jdk_x64_mac_hotspot_11.0.14.1_1.tar.gz",
        ),
    },
    "11.0.12_7": {
        "Linux-x86_64": (
            "8770f600fc3b89bf331213c7aa21f8eedd9ca5d96036d1cd48cb2748a3dbefd2",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.12%2B7/OpenJDK11U-jdk_x64_linux_hotspot_11.0.12_7.tar.gz",
        ),
        "Linux-aarch64": (
            "105bdc12fcd54c551e8e8ac96bc82412467244c32063689c41cee29ceb7452a2",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.12%2B7/OpenJDK11U-jdk_aarch64_linux_hotspot_11.0.12_7.tar.gz",
        ),
        "Linux-ppc64le": (
            "234a9bafe029ea6cab5d46f9617b5d016a29faa187a42081d0e066f23647b7e5",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.12%2B7/OpenJDK11U-jdk_ppc64le_linux_hotspot_11.0.12_7.tar.gz",
        ),
        "Darwin-x86_64": (
            "13d056ee9a57bf2d5b3af4504c8f8cf7a246c4dff78f96b70dd05dad98075855",
            "https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.12%2B7/OpenJDK11U-jdk_x64_mac_hotspot_11.0.12_7.tar.gz",
        ),
    },
    "11.0.9.1_1": {
        "Linux-ppc64le": (
            "d94b6b46a14ab0974b1c1b89661741126d8cf8a0068b471b8f5fa286a71636b1",
            "https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.9.1%2B1/OpenJDK11U-jdk_ppc64le_linux_hotspot_11.0.9.1_1.tar.gz",
        )
    },
    "11.0.8_10": {
        "Linux-x86_64": (
            "6e4cead158037cb7747ca47416474d4f408c9126be5b96f9befd532e0a762b47",
            "https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk-11.0.8%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.8_10.tar.gz",
        )
    },
    "11.0.0-2020-01-01": {
        "Linux-aarch64": (
            "05c7d9c90edacd853850fbb0f52f8aa482809d0452c599cb9fe0b28b3b4bf329",
            "https://github.com/AdoptOpenJDK/openjdk11-binaries/releases/download/jdk11u-2020-01-01-06-13/OpenJDK11U-jdk_aarch64_linux_hotspot_2020-01-01-06-13.tar.gz",
        )
    },
    "11.0.2": {
        "Linux-x86_64": (
            "99be79935354f5c0df1ad293620ea36d13f48ec3ea870c838f20c504c9668b57",
            "https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz",
        ),
        "Darwin-x86_64": (
            "f365750d4be6111be8a62feda24e265d97536712bc51783162982b8ad96a70ee",
            "https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_osx-x64_bin.tar.gz",
        ),
    },
    "11.0.1": {
        "Linux-x86_64": (
            "7a6bb980b9c91c478421f865087ad2d69086a0583aeeb9e69204785e8e97dcfd",
            "https://download.java.net/java/GA/jdk11/13/GPL/openjdk-11.0.1_linux-x64_bin.tar.gz",
        ),
        "Darwin-x86_64": (
            "fa07eee08fa0f3de541ee1770de0cdca2ae3876f3bd78c329f27e85c287cd070",
            "https://download.java.net/java/GA/jdk11/13/GPL/openjdk-11.0.1_osx-x64_bin.tar.gz",
        ),
    },
    "1.8.0_265-b01": {
        "Linux-x86_64": (
            "1285da6278f2d38a790a21148d7e683f20de0799c44b937043830ef6b57f58c4",
            "https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u265-b01/OpenJDK8U-jdk_x64_linux_hotspot_8u265b01.tar.gz",
        )
    },
    "1.8.0_191-b12": {
        "Linux-aarch64": (
            "8eee0aede947b804f9a5f49c8a38b52aace8a30a9ebd9383b7d06042fb5a237c",
            "https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u191-b12/OpenJDK8U-jdk_aarch64_linux_hotspot_8u191b12.tar.gz",
        )
    },
    "1.8.0_222-b10": {
        "Linux-x86_64": (
            "20cff719c6de43f8bb58c7f59e251da7c1fa2207897c9a4768c8c669716dc819",
            "https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u222-b10_openj9-0.15.1/OpenJDK8U-jdk_x64_linux_openj9_8u222b10_openj9-0.15.1.tar.gz",
        )
    },
    "1.8.0_202-b08": {
        "Linux-x86_64": (
            "533dcd8d9ca15df231a1eb392fa713a66bca85a8e76d9b4ee30975f3823636b7",
            "https://github.com/AdoptOpenJDK/openjdk8-binaries/releases/download/jdk8u202-b08/OpenJDK8U-jdk_x64_linux_openj9_8u202b08_openj9-0.12.0.tar.gz",
        )
    },
    "1.8.0_40-b25": {
        "Linux-x86_64": (
            "79e96dce03a14271040023231a7d0ae374b755d48adf68bbdaec30294e4e2b88",
            "https://download.java.net/openjdk/jdk8u40/ri/jdk_ri-8u40-b25-linux-x64-10_feb_2015.tar.gz",
        )
    },
}


class Openjdk(Package):
    """The free and opensource java implementation"""

    homepage = "https://openjdk.org/"
    preferred_prefix = "17."

    preferred_defined = False
    for ver, packages in _versions.items():
        key = "{0}-{1}".format(platform.system(), platform.machine())
        pkg = packages.get(key)
        if pkg:
            is_preferred = not preferred_defined and ver.startswith(preferred_prefix)
            if is_preferred:
                preferred_defined = True

            version(ver, sha256=pkg[0], url=pkg[1], preferred=is_preferred)

    variant(
        "certs",
        default="none",
        values=("system", "none"),
        multi=False,
        description=("symlink system certs if requested, otherwise use default package version"),
    )

    provides("java@21", when="@21.0:21")
    provides("java@17", when="@17.0:17")
    provides("java@16", when="@16.0:16")
    provides("java@15", when="@15.0:15")
    provides("java@11", when="@11.0:11")
    provides("java@10", when="@10.0:10")
    provides("java@9", when="@9.0:9")
    provides("java@8", when="@1.8.0:1.8")

    conflicts("target=ppc64:", msg="openjdk is not available for ppc64 (big endian)")

    # FIXME:
    # 1. `extends('java')` doesn't work, you need to use `extends('openjdk')`
    # 2. Packages cannot extend multiple packages, see #987
    # 3. Update `YamlFilesystemView.merge` to allow a Package to completely
    #    override how it is symlinked into a view prefix. Then, spack activate
    #    can symlink all *.jar files to `prefix.lib.ext`
    extendable = True

    executables = ["^java$"]

    skip_version_audit = ["platform=windows"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("-version", output=str, error=str)

        # Make sure this is actually OpenJDK, not Oracle JDK
        if "openjdk" not in output:
            return None

        match = re.search(r"\(build (\S+)\)", output)
        return match.group(1).replace("+", "_") if match else None

    @property
    def home(self):
        """Most of the time, ``JAVA_HOME`` is simply ``spec['java'].prefix``.
        However, if the user is using an externally installed JDK, it may be
        symlinked. For example, on macOS, the ``java`` executable can be found
        in ``/usr/bin``, but ``JAVA_HOME`` is actually
        ``/Library/Java/JavaVirtualMachines/jdk-10.0.1.jdk/Contents/Home``.
        Users may not know the actual installation directory and add ``/usr``
        to their ``packages.yaml`` unknowingly. Run ``java_home`` if it exists
        to determine exactly where it is installed. Specify which version we
        are expecting in case multiple Java versions are installed.
        See ``man java_home`` for more details."""

        prefix = self.prefix
        java_home = prefix.libexec.java_home
        if os.path.exists(java_home):
            java_home = Executable(java_home)
            version = str(self.version.up_to(2))
            prefix = java_home("--version", version, output=str).strip()
            prefix = Prefix(prefix)

        return prefix

    @property
    def libs(self):
        """Depending on the version number and whether the full JDK or just
        the JRE was installed, Java libraries can be in several locations:

        * ``lib/libjvm.so``
        * ``jre/lib/libjvm.dylib``

        Search recursively to find the correct library location."""

        return find_libraries(["libjvm"], root=self.home, recursive=True)

    def install(self, spec, prefix):
        top_dir = "Contents/Home/" if platform.system() == "Darwin" else "."
        install_tree(top_dir, prefix)

    @run_after("install")
    def link_system_certs(self):
        if self.spec.variants["certs"].value != "system":
            return

        system_dirs = [
            # CentOS, Fedora, RHEL
            "/etc/pki/java",
            # Ubuntu
            "/etc/ssl/certs/java",
            # OpenSUSE
            "/var/lib/ca-certificates/java-certs",
        ]

        for directory in system_dirs:
            # Link configuration file
            sys_certs = join_path(directory, "cacerts")

            # path for 1.8.0 versions
            pkg_dir = join_path(self.prefix, "jre", "lib", "security")
            if not os.path.exists(pkg_dir):
                # path for version 11 and newer
                pkg_dir = join_path(self.prefix, "lib", "security")
            if not os.path.exists(pkg_dir):
                break
            pkg_conf = join_path(pkg_dir, "cacerts")
            if os.path.exists(sys_certs):
                if os.path.exists(pkg_conf):
                    os.remove(pkg_conf)
                os.symlink(sys_certs, pkg_conf)

    def setup_run_environment(self, env):
        """Set JAVA_HOME."""

        env.set("JAVA_HOME", self.home)

    def setup_dependent_build_environment(self, env, dependent_spec):
        """Set JAVA_HOME and CLASSPATH.

        CLASSPATH contains the installation prefix for the extension and any
        other Java extensions it depends on."""

        env.set("JAVA_HOME", self.home)

        class_paths = []
        for d in dependent_spec.traverse(deptype=("build", "run", "test")):
            if d.package.extends(self.spec):
                class_paths.extend(find(d.prefix, "*.jar"))

        classpath = os.pathsep.join(class_paths)
        env.set("CLASSPATH", classpath)

    def setup_dependent_run_environment(self, env, dependent_spec):
        """Set CLASSPATH.

        CLASSPATH contains the installation prefix for the extension and any
        other Java extensions it depends on."""
        # For runtime environment set only the path for
        # dependent_spec and prepend it to CLASSPATH
        if dependent_spec.package.extends(self.spec):
            class_paths = find(dependent_spec.prefix, "*.jar")
            classpath = os.pathsep.join(class_paths)
            env.prepend_path("CLASSPATH", classpath)

    # Since we provide openjdk as a binary, we can't remove an obsolete glibc
    # fix that prevents us from modifying the soname of libjvm.so. If we move
    # to source builds this should be possible.
    non_bindable_shared_objects = ["libjvm.so"]

    # contains precompiled binaries without rpaths
    unresolved_libraries = ["*"]
