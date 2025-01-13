# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rocketmq(Package):
    """
    Apache RocketMQ is a distributed messaging and streaming platform
    with low latency, high performance and reliability, trillion-level
    capacity and flexible scalability.
    """

    homepage = "https://rocketmq.apache.org/"
    url = "https://archive.apache.org/dist/rocketmq/4.5.2/rocketmq-all-4.5.2-bin-release.zip"

    license("Apache-2.0", checked_by="wdconinc")

    version("5.3.1", sha256="251d7261fa26d35eaffef6a2fce30880054af7a5883d578dd31574bf908a8b97")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2023-37582
        version("4.6.0", sha256="584910d50639297808dd0b86fcdfaf431efd9607009a44c6258d9a0e227748fe")
        version("4.5.2", sha256="f7711ef9c203d7133e70e0e1e887025d7dd80d29f6d5283ca6022b12576b8aba")
        version("4.5.1", sha256="0c46e4b652b007d07e9c456eb2e275126b9210c27cd56bee518809f33c8ed437")
        version("4.5.0", sha256="d75dc26291b47413f7c565bc65499501e3499f01beb713246586f72844e31042")
        version("4.4.0", sha256="8a948e240e8d2ebbf4c40c180105d088a937f82a594cd1f2ae527b20349f1d34")
        version("4.3.2", sha256="e31210a86266ee218eb6ff4f8ca6e211439895459c3bdad162067b573d9e3415")

    depends_on("java@8:", type="run")

    # UseBiasedLocking deprecated in java@15:, removed in java@21:
    # https://openjdk.org/jeps/374, https://github.com/apache/rocketmq/pull/8809
    depends_on("java@:20", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix)
