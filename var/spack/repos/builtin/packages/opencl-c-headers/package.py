# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class OpenclCHeaders(CMakePackage):
    """OpenCL (Open Computing Language) C header files"""

    homepage = "https://www.khronos.org/registry/OpenCL/"
    url = "https://github.com/KhronosGroup/OpenCL-Headers/archive/v2020.06.16.tar.gz"
    maintainers("lorddavidiii")

    license("Apache-2.0")

    version(
        "2024.05.08", sha256="3c3dd236d35f4960028f4f58ce8d963fb63f3d50251d1e9854b76f1caab9a309"
    )
    version(
        "2023.12.14", sha256="407d5e109a70ec1b6cd3380ce357c21e3d3651a91caae6d0d8e1719c69a1791d"
    )
    version(
        "2023.04.17", sha256="0ce992f4167f958f68a37918dec6325be18f848dee29a4521c633aae3304915d"
    )
    version(
        "2023.02.06", sha256="464d1b04a5e185739065b2d86e4cebf02c154c416d63e6067a5060d7c053c79a"
    )
    version(
        "2022.09.30", sha256="0ae857ecb28af95a420c800b21ed2d0f437503e104f841ab8db249df5f4fbe5c"
    )
    version(
        "2022.09.23", sha256="dfaded8acf44473e47e7829373c6bb5fba148dc36a38ccd6ef7b6c1ebb78ae68"
    )
    version(
        "2022.05.18", sha256="88a1177853b279eaf574e2aafad26a84be1a6f615ab1b00c20d5af2ace95c42e"
    )
    version(
        "2022.01.04", sha256="6e716e2b13fc8d363b40a165ca75021b102f9328e2b38f8054d7db5884de29c9"
    )
    version(
        "2021.06.30", sha256="6640d590c30d90f89351f5e3043ae6363feeb19ac5e64bc35f8cfa1a6cd5498e"
    )
    version(
        "2021.04.29", sha256="477e2b26125d99a9b2f20c68262f27ca3f3ca7899593a8af2b7fe077bdce18d1"
    )
    version(
        "2020.12.18", sha256="5dad6d436c0d7646ef62a39ef6cd1f3eba0a98fc9157808dfc1d808f3705ebc2"
    )
    version(
        "2020.06.16", sha256="2f5a60e5ac4b127650618c58a7e3b35a84dbf23c1a0ac72eb5e7baf221600e06"
    )
    version(
        "2020.03.13", sha256="664bbe587e5a0a00aac267f645b7c413586e7bc56dca9ff3b00037050d06f476"
    )

    depends_on("c", type="build")  # generated

    def cmake_args(self):
        # Disable testing the headers. They definitely work.
        return ["-DBUILD_TESTING=OFF"]
