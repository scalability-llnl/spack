# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CaCertificatesMozilla(Package):
    """The Mozilla CA certificate store in PEM format"""

    homepage = "https://curl.se/docs/caextract.html"
    url = "https://curl.se/ca/cacert-2021-04-13.pem"

    maintainers("haampie")

    version(
        "2023-05-30",
        sha256="5fadcae90aa4ae041150f8e2d26c37d980522cdb49f923fc1e1b5eb8d74e71ad",
        expand=False,
    )
    version(
        "2023-01-10",
        sha256="fb1ecd641d0a02c01bc9036d513cb658bbda62a75e246bedbc01764560a639f0",
        expand=False,
    )
    version(
        "2022-10-11",
        sha256="2cff03f9efdaf52626bd1b451d700605dc1ea000c5da56bd0fc59f8f43071040",
        expand=False,
    )
    version(
        "2022-07-19",
        sha256="6ed95025fba2aef0ce7b647607225745624497f876d74ef6ec22b26e73e9de77",
        expand=False,
    )
    version(
        "2022-04-26",
        sha256="08df40e8f528ed283b0e480ba4bcdbfdd2fdcf695a7ada1668243072d80f8b6f",
        expand=False,
    )
    version(
        "2022-03-29",
        sha256="1979e7fe618c51ed1c9df43bba92f977a0d3fe7497ffa2a5e80dfc559a1e5a29",
        expand=False,
    )
    version(
        "2022-03-18",
        sha256="2d0575e481482551a6a4f9152e7d2ab4bafaeaee5f2606edb829c2fdb3713336",
        expand=False,
    )
    version(
        "2022-02-01",
        sha256="1d9195b76d2ea25c2b5ae9bee52d05075244d78fcd9c58ee0b6fac47d395a5eb",
        expand=False,
    )
    version(
        "2021-10-26",
        sha256="ae31ecb3c6e9ff3154cb7a55f017090448f88482f0e94ac927c0c67a1f33b9cf",
        expand=False,
    )
    version(
        "2021-09-30",
        sha256="f524fc21859b776e18df01a87880efa198112214e13494275dbcbd9bcb71d976",
        expand=False,
    )
    version(
        "2021-07-05",
        sha256="a3b534269c6974631db35f952e8d7c7dbf3d81ab329a232df575c2661de1214a",
        expand=False,
    )
    version(
        "2021-05-25",
        sha256="3a32ad57e7f5556e36ede625b854057ac51f996d59e0952c207040077cbe48a9",
        expand=False,
    )
    version(
        "2021-04-13",
        sha256="533610ad2b004c1622a40622f86ced5e89762e1c0e4b3ae08b31b240d863e91f",
        expand=False,
    )
    version(
        "2021-01-19",
        sha256="e010c0c071a2c79a76aa3c289dc7e4ac4ed38492bfda06d766a80b707ebd2f29",
        expand=False,
    )
    version(
        "2020-12-08",
        sha256="313d562594ebd07846ad6b840dd18993f22e0f8b3f275d9aacfae118f4f00fb7",
        expand=False,
    )
    version(
        "2020-10-14",
        sha256="bb28d145ed1a4ee67253d8ddb11268069c9dafe3db25a9eee654974c4e43eee5",
        expand=False,
    )
    version(
        "2020-07-22",
        sha256="2782f0f8e89c786f40240fc1916677be660fb8d8e25dede50c9f6f7b0c2c2178",
        expand=False,
    )
    version(
        "2020-06-24",
        sha256="726889705b00f736200ed7999f7a50021b8735d53228d679c4e6665aa3b44987",
        expand=False,
    )
    version(
        "2020-01-01",
        sha256="adf770dfd574a0d6026bfaa270cb6879b063957177a991d453ff1d302c02081f",
        expand=False,
    )
    version(
        "2019-11-27",
        sha256="0d98a1a961aab523c9dc547e315e1d79e887dea575426ff03567e455fc0b66b4",
        expand=False,
    )
    version(
        "2019-10-16",
        sha256="5cd8052fcf548ba7e08899d8458a32942bf70450c9af67a0850b4c711804a2e4",
        expand=False,
    )
    version(
        "2019-08-28",
        sha256="38b6230aa4bee062cd34ee0ff6da173250899642b1937fc130896290b6bd91e3",
        expand=False,
    )

    # Make spack checksum work
    def url_for_version(self, version):
        return "https://curl.se/ca/cacert-{0}.pem".format(version)

    def setup_dependent_package(self, module, dep_spec):
        """Returns the absolute path to the bundled certificates"""
        self.spec.pem_path = join_path(self.prefix.share, "cacert.pem")

    # Install the the pem file as share/cacert.pem
    def install(self, spec, prefix):
        share = join_path(prefix, "share")
        # https://github.com/spack/spack/issues/32948
        mkdirp(share)
        install("cacert-{0}.pem".format(spec.version), join_path(share, "cacert.pem"))
