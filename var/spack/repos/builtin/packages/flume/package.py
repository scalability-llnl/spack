# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flume(Package):
    """
    Apache Flume is a distributed, reliable, and available service for
    efficiently collecting, aggregating, and moving large amounts of log
    data. It has a simple and flexible architecture based on streaming
    data flows. It is robust and fault tolerant with tunable reliability
    mechanisms and many failover and recovery mechanisms. The system is
    centrally managed and allows for intelligent dynamic management. It
    uses a simple extensible data model that allows for online analytic
    application.
    """

    homepage = "https://flume.apache.org"
    url = "https://www.apache.org/dist/flume/1.9.0/apache-flume-1.9.0-bin.tar.gz"

    license("Apache-2.0", checked_by="wdconinc")

    version("1.11.0", sha256="6eb7806076bdc3dcadb728275eeee7ba5cb12b63a2d981de3da9063008dba678")
    version("1.9.0", sha256="0373ed5abfd44dc4ab23d9a02251ffd7e3b32c02d83a03546e97ec15a7b23619")
    version("1.8.0", sha256="be1b554a5e23340ecc5e0b044215bf7828ff841f6eabe647b526d31add1ab5fa")
    version("1.7.0", sha256="b97254cf37c36b6e5045f764095d86fc6d9a8043dda169e950547fcae35681ec")
    version("1.6.0", sha256="0f7cef2f0128249893498a23401a0c8cb261e4516bc60f1885f8a3ae4475ed80")
    version("1.5.2", sha256="649f07c41d0e77acd661c683146a0c5e395bfb3f23df198196fe8058a7b01426")

    depends_on("java@8:", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix)
