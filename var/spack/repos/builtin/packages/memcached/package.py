# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Memcached(AutotoolsPackage):
    """
    Memcached is a high performance multithreaded event-based key/value
    cache store intended to be used in a distributed system.
    """

    homepage = "https://github.com/memcached/memcached"
    url = "https://github.com/memcached/memcached/archive/1.5.20.tar.gz"

    license("BSD-3-Clause")

    version("1.5.20", sha256="ee93aff47123e0b464e9f007b651b14c89c19e0c20352d8d1c399febbb038cb6")
    version("1.5.19", sha256="7af7a2e9b1f468d7f6056f23ce21c04936ce6891f8cb8cd54e133f489a8226e8")
    version("1.5.18", sha256="0bf8154f53d2781164421acd195a1665ac2f77316263c3526206c38e402c4b0d")
    version("1.5.17", sha256="cb30ad851e95c0190e6b7e59695f1ed2e51d65a9e6c82c893e043dc066053377")
    version("1.5.16", sha256="a0c1a7e72186722d7c0e9d5527a63beb339b933d768687f183e163adf935c662")
    version("1.5.15", sha256="4ef8627308e99bdd4200ef4f260fbcdd65a4ba634bd593ca02dbbfd71222e9f7")
    version("1.5.14", sha256="ae8ed2ed853b840a8430d8575d4e91b87c550b111874b416c551001403ac6a74")
    version("1.5.13", sha256="ae59a8b49be17afb344e57c8a8d64f9ae38b6efbc3f9115a422dbcb2b23795fc")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("libevent", type="build")

    def autoreconf(self, spec, prefix):
        sh = which("sh")
        sh("./autogen.sh")
        autoreconf("--install", "--verbose", "--force")

    def configure_args(self):
        args = ["--with-libevent={0}".format(self.spec["libevent"].prefix)]
        return args
