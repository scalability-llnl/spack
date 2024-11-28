# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Netdata(AutotoolsPackage):
    """Real-time performance monitoring, done right!"""

    homepage = "https://www.netdata.cloud/"
    url = "https://github.com/netdata/netdata/releases/download/v1.30.1/netdata-v1.30.1.tar.gz"

    license("GPL-3.0-or-later")

    version("1.44.2", sha256="9b9267b03af90fe8754f2fb5d16f7f6c60f770d2e890dbc55fd9dcdfd2a4179a")
    version("1.38.1", sha256="e32a5427f0c00550210dbbf0046c2621313955256edf836db686e2bc270b8d10")
    version("1.31.0", sha256="ca68f725224e8bbec041b493891376fbf41aedb47c4ac06161c2eda990089c9f")
    version("1.30.1", sha256="3df188ac04f17094cb929e2990841ba77f68aa6af484e0509b99db298fa206c9")
    version("1.22.1", sha256="f169c8615a6823448c2f1923c87c286d798132ea29d26f366e96d26e0aec3697")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("json-c")
    depends_on("judy")
    depends_on("libelf")
    depends_on("libmnl")
    depends_on("libuv")
    depends_on("lz4")
    depends_on("openssl")
    depends_on("python@3:", type=("build", "run"))
    depends_on("uuid")
    depends_on("zlib-api")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)

    @run_after("install")
    def setup_dirs(self):
        # netdata requires the following directories to be able to run.
        mkdirp(self.prefix.var.cache.netdata)
        mkdirp(self.prefix.var.lib.netdata)
        mkdirp(self.prefix.var.log.netdata)
