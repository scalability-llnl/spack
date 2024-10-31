# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zabbix(AutotoolsPackage):
    """Real-time monitoring of IT components and services,
    such as networks, servers, VMs, applications and the cloud."""

    homepage = "https://www.zabbix.com"
    url = "https://github.com/zabbix/zabbix/archive/5.0.3.tar.gz"

    license("GPL-2.0-or-later")

    version("5.0.3", sha256="d579c5fa4e9065e8041396ace24d7132521ef5054ce30dfd9d151cbb7f0694ec")
    version("4.0.24", sha256="c7e4962d745277d67797d90e124555ce27d198822a7e65c55d86aee45d3e93fc")
    version("4.0.23", sha256="652143614f52411cad47db64e93bf3ba1cd547d6ca9591296223b5f0528b3b61")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("mysql")
    depends_on("libevent")
    depends_on("pcre")
    depends_on("go")

    def configure_args(self):
        args = [
            "--enable-server",
            "--enable-proxy",
            "--enable-agent",
            "--enable-agent2",
            "--with-mysql",
            "--with-libevent=%s" % self.spec["libevent"].prefix,
            "--with-libpcre=%s" % self.spec["pcre"].prefix,
        ]

        return args

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
