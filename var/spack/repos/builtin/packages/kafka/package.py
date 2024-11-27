# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kafka(Package):
    """
    Kafka is used for building real-time data pipelines and streaming apps.
    It is horizontally scalable, fault-tolerant, wicked fast, and runs in
    production in thousands of companies.
    """

    homepage = "https://www-eu.apache.org/dist/kafka"
    url = "https://www-eu.apache.org/dist/kafka/2.3.1/kafka_2.12-2.3.1.tgz"
    list_url = "https://www-eu.apache.org/dist/kafka/"
    list_depth = 1

    license("EPL-2.0")

    version(
        "2.13-3.8.0", sha256="e0297cc6fdb09ef9d9905751b25d2b629c17528f8629b60561eeff87ce29099c"
    )
    version(
        "2.13-3.7.1", sha256="62acae4a143dd983dc7eb4804d5744ba0c50b199b508f599ef001020e2558fc9"
    )
    version(
        "2.13-3.7.0",
        sha256="65f26e5937bbb76dfe78dfb416730dfa7e3378b27e13fd1e204f1a1099bfaf9c",
        deprecated=True,
    )
    version(
        "2.13-3.5.1", sha256="f7b74d544023f2c0ec52a179de59975cb64e34ea03650d829328b407b560e4da"
    )
    version(
        "2.13-3.5.0", sha256="2a3a468e069be570f16d612a8196c2f7a9207b7eac865be934d20ce1252eb2f8"
    )
    version(
        "2.13-3.4.1", sha256="a76f17a52b8f2cd31de11571ff366a714820b6e4e02893b0159d09db0edaf998"
    )
    version(
        "2.13-2.4.0", sha256="c1c5246c7075459687b3160b713a001f5cd1cc563b9a3db189868d2f22aa9110"
    )
    version(
        "2.12-2.4.0", sha256="b9582bab0c3e8d131953b1afa72d6885ca1caae0061c2623071e7f396f2ccfee"
    )
    version(
        "2.12-2.3.1", sha256="5a3ddd4148371284693370d56f6f66c7a86d86dd96c533447d2a94d176768d2e"
    )
    version(
        "2.12-2.3.0", sha256="d86f5121a9f0c44477ae6b6f235daecc3f04ecb7bf98596fd91f402336eee3e7"
    )
    version(
        "2.12-2.2.2", sha256="7a1713d2ee929e54b1c889a449d77006513e59afb3032366368b2ebccd9e9ec0"
    )

    depends_on("java@8:", type="run")

    def url_for_version(self, version):
        url = "https://www-eu.apache.org/dist/kafka/{0}/kafka_{1}.tgz"
        parent_dir = str(version).split("-")[1]
        return url.format(parent_dir, version)

    def install(self, spec, prefix):
        install_tree(".", prefix)
