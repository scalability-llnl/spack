# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flink(Package):
    """
    Apache Flink is an open source stream processing framework with
    powerful stream- and batch-processing capabilities.
    """

    homepage = "https://flink.apache.org/"
    url = "https://archive.apache.org/dist/flink/flink-1.20.0/flink-1.20.0-bin-scala_2.12.tgz"

    license("Apache-2.0", checked_by="wdconinc")

    version("1.20.0", sha256="708fd544ccf9ddc0d4b192fe035797ce16de2c26f1d764c55907305efe140af0")
    version("1.9.1", sha256="f69de344cd593e92f8261e19ae8a47b3910e9a70a7cd1ccfb1ecd1ff000b93ea")
    version("1.9.0", sha256="a2245f68309e94ed54d86a680232a518aed9c5ea030bcc0b298bc8f27165eeb7")
    version("1.8.3", sha256="1ba90e99f70ad7e2583d48d1404d1c09e327e8fb8fa716b1823e427464cc8dc0")
    version("1.8.2", sha256="1a315f4f1fab9d651702d177b1741439ac98e6d06e9e13f9d410b34441eeda1c")
    version("1.8.1", sha256="4fc0d0f163174ec43e160fdf21a91674979b978793e60361e2fce5dddba4ddfa")

    depends_on("java@8:", type="run")

    def url_for_version(self, version):
        scala = "2.12" if version >= Version("1.15") else "2.11"
        return f"https://archive.apache.org/dist/flink/flink-{version}/flink-{version}-bin-scala_{scala}.tgz"

    def install(self, spec, prefix):
        install_tree(".", prefix)
