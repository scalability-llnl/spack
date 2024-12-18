# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nextflow(Package):
    """Data-driven computational pipelines."""

    homepage = "https://www.nextflow.io"
    url = "https://github.com/nextflow-io/nextflow/releases/download/v21.04.3/nextflow"

    maintainers("dialvarezs", "marcodelapierre")

    version(
        "24.10.3",
        sha256="01110949bb3256bf6cbf1d4b3ea17369491b3f693b6d86a0c9ab8171b1619ba0",
        expand=False,
    )
    version(
        "24.10.2",
        sha256="e12bf1fc1e11629f2aef22a9a6ddecc31522bcd5988d1c48d263de699b4e5289",
        expand=False,
    )
    version(
        "24.10.0",
        sha256="e848918fb9b85762822c078435d9ff71979a88cccff81ce5babd75d5eee52fe6",
        expand=False,
    )
    version(
        "24.04.3",
        sha256="e258f6395a38f044eb734cba6790af98b561aa521f63e2701fe95c050986e11c",
        expand=False,
    )
    version(
        "24.04.1",
        sha256="d1199179e31d0701d86e6c38afa9ccade93f62d545e800824be7767a130510ba",
        expand=False,
    )
    version(
        "23.10.1",
        sha256="9abc54f1ffb2b834a8135d44300404552d1e27719659cbb635199898677b660a",
        expand=False,
    )
    version(
        "23.10.0",
        sha256="4b7fba61ecc6d53a6850390bb435455a54ae4d0c3108199f88b16b49e555afdd",
        expand=False,
    )
    version(
        "23.04.3",
        sha256="258714c0772db3cab567267e8441c5b72102381f6bd58fc6957c2972235be7e0",
        expand=False,
    )
    version(
        "23.04.1",
        sha256="5de3e09117ca648b2b50778d3209feb249b35de0f97cdbcf52c7d92c7a96415c",
        expand=False,
    )
    version(
        "22.10.4",
        sha256="612a085e183546688e0733ebf342fb73865f560ad1315d999354048fbca5954d",
        expand=False,
    )
    version(
        "22.10.3",
        sha256="8d67046ca3b645fab2642d90848550a425c9905fd7dfc2b4753b8bcaccaa70dd",
        expand=False,
    )
    version(
        "22.10.1",
        sha256="fa6b6faa8b213860212da413e77141a56a5e128662d21ea6603aeb9717817c4c",
        expand=False,
    )
    version(
        "22.10.0",
        sha256="6acea8bd21f7f66b1363eef900cd696d9523d2b9edb53327940f093189c1535e",
        expand=False,
    )
    version(
        "22.04.4",
        sha256="e5ebf9942af4569db9199e8528016d9a52f73010ed476049774a76b201cd4b10",
        expand=False,
    )
    version(
        "22.04.3",
        sha256="a1a79c619200b9f2719e8467cd5b8fbcb427f43adf945233ba9e03cd2f2d814e",
        expand=False,
    )
    version(
        "22.04.1",
        sha256="89ef482a53d2866a3cee84b3576053278b53507bde62db4ad05b1fcd63a9368a",
        expand=False,
    )
    version(
        "22.04.0",
        sha256="8eba475aa395438ed222ff14df8fbe93928c14ffc68727a15b8308178edf9056",
        expand=False,
    )
    version(
        "21.10.6",
        sha256="104c0352c592924233ea7897cbfb2ece41795be348f97d6dfbc8d66e6271e4ad",
        expand=False,
        deprecated=True,
    )
    version(
        "21.10.1",
        sha256="05c8b9f3d2f5eded737fdd0a13b84e3bc442cc6355ba95e21118cb624f8176da",
        expand=False,
        deprecated=True,
    )
    version(
        "21.10.0",
        sha256="e938e53f43f0f00c8d5adf2dc104c4ce0c6d834aa84a4a3918ac8bec6eee6b9c",
        expand=False,
        deprecated=True,
    )
    version(
        "21.04.3",
        sha256="80c7ecd94b55da8eb0e17040dbd0c43ee80e252cd999374e16c00d54d3d3abf3",
        expand=False,
        deprecated=True,
    )
    version(
        "20.10.0",
        sha256="54f76c83cbabe8ec68d6a878dcf921e647284499f4ae917356e594d873cb78dd",
        expand=False,
        deprecated=True,
    )
    version(
        "20.07.1",
        sha256="de4db5747a801af645d9b021c7b36f4a25c3ce1a8fda7705a5f37e8f9357443a",
        expand=False,
        deprecated=True,
    )
    version(
        "20.04.1",
        sha256="b46833ad75b9b7db72668235b53d5c295a9ab02b50d36506bbbe53f383239bde",
        expand=False,
        deprecated=True,
    )
    version(
        "20.01.0",
        sha256="fe1900284fd658c0781e6d8048839541afe5818d0b53f6ee8ae81f59d47ad662",
        expand=False,
        deprecated=True,
    )
    version(
        "19.10.0",
        sha256="45497eb4bea62dd5477ebe75a6dabfd6905554c46321ca40aec6edfec61c59f4",
        expand=False,
        deprecated=True,
    )
    version(
        "19.07.0",
        sha256="e6e7ba4770cd6230bd5410a6fd8c071d6c6dde7a7765880ecabc820b84d38fe5",
        expand=False,
        deprecated=True,
    )
    version(
        "19.04.1",
        sha256="21318d8b64095a548f6baf0ef2811f33452e4f9f8a502a46a0aab7815ee34c69",
        expand=False,
        deprecated=True,
    )
    version(
        "0.25.6",
        sha256="9498806596c96ba87396194fa6f1d7d1cdb739990f83e7e89d1d055366c5a943",
        expand=False,
        deprecated=True,
    )
    version(
        "0.24.1",
        sha256="0bfde5335b385e3cff99bf4aab619e583de5dc0849767240f675037a2e7c1d83",
        expand=False,
        deprecated=True,
    )
    version(
        "0.23.3",
        sha256="ffe1c314962ff97ebf47b0567883e152522acfbf6fd5800200b1a7a0ca2896d2",
        expand=False,
        deprecated=True,
    )
    version(
        "0.21.0",
        sha256="076089079479da0d91fe1ad7aad06816164ecbcf17f73c55e795b1db8462b28d",
        expand=False,
        deprecated=True,
    )
    version(
        "0.20.1",
        sha256="02635f3371f76a10e12f7366508c90bacf532ab7c23ae03c895317a150a39bd4",
        expand=False,
        deprecated=True,
    )
    version(
        "0.17.3",
        sha256="05563ee1474fbef22f65fa3080792dcb08d218dd1b1561c517ebff4346559dbe",
        expand=False,
        deprecated=True,
    )

    depends_on("java", type="run")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(self.stage.archive_file, join_path(prefix.bin, "nextflow"))
        set_executable(join_path(prefix.bin, "nextflow"))
