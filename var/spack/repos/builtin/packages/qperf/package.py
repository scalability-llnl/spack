# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qperf(AutotoolsPackage):
    """
    The qperf measures bandwidth and latency between two nodes. It can work
    over TCP/IP as well as the RDMA transports.
    """

    homepage = "https://github.com/linux-rdma/qperf"
    url = "https://github.com/linux-rdma/qperf/archive/v0.4.10.tar.gz"

    license("GPL-2.0")

    version("0.4.11", sha256="b0ef2ffe050607566d06102b4ef6268aad08fdc52898620d429096e7b0767e75")
    version("0.4.10", sha256="94e26725b4f962eacca36d8ef48cd1fb5043721ac82c3f44018319e47a96cf6b")

    depends_on("c", type="build")  # generated

    variant("verbs", default=True, description="Build with verbs support")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("rdma-core", when="+verbs")

    def autoreconf(self, spec, prefix):
        sh = which("sh")
        sh("autogen.sh")
