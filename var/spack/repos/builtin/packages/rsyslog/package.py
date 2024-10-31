# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rsyslog(AutotoolsPackage):
    """The rocket-fast Syslog Server."""

    homepage = "https://www.rsyslog.com/"
    url = "https://github.com/rsyslog/rsyslog/archive/v8.2006.0.tar.gz"

    license("Apache-2.0 AND GPL-3.0-or-later AND LGPL-3.0-or-later", checked_by="tgamblin")

    version("8.2006.0", sha256="dc30a2ec02d5fac91d3a4f15a00641e0987941313483ced46592ab0b0d68f324")
    version("8.2004.0", sha256="b56b985fec076a22160471d389b7ff271909dfd86513dad31e401a775a6dfdc2")
    version("8.2002.0", sha256="b31d56311532335212ef2ea7be4501508224cb21f1bef9d262c6d78e21959ea1")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("libestr")
    depends_on("libfastjson")
    depends_on("zlib-api")
    depends_on("uuid")
    depends_on("libgcrypt")
    depends_on("curl")
    depends_on("byacc", type="build")
    depends_on("flex", type="build")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)

    def configure_args(self):
        args = ["--with-systemdsystemunitdir=" + self.spec["rsyslog"].prefix.lib.systemd.system]
        return args
