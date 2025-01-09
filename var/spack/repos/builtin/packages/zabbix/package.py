# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Zabbix(AutotoolsPackage):
    """Real-time monitoring of IT components and services,
    such as networks, servers, VMs, applications and the cloud."""

    homepage = "https://www.zabbix.com"
    url = "https://github.com/zabbix/zabbix/archive/refs/tags/5.0.3.tar.gz"

    license("AGPL-3.0-only", when="@7:", checked_by="wdconinc")
    license("GPL-2.0-or-later", when="@:6", checked_by="wdconinc")

    version("7.0.4", sha256="73aa6b47bd4078587589b30f09671fb30c7743f5b57e81ea8e9bd5a7c5f221c7")
    version("6.0.34", sha256="e60558911230d27ffad98850e414b46e318c9d41591a6ff65a255c0810cfcb8b")
    version("5.0.44", sha256="f8ee86fd21f0f57e7fad68387271b995c1e5cc402d517cd7df5d5221fd6129fd")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2023-32724
        version("5.0.3", sha256="d579c5fa4e9065e8041396ace24d7132521ef5054ce30dfd9d151cbb7f0694ec")
        # https://nvd.nist.gov/vuln/detail/CVE-2019-17382
        version(
            "4.0.24", sha256="c7e4962d745277d67797d90e124555ce27d198822a7e65c55d86aee45d3e93fc"
        )
        version(
            "4.0.23", sha256="652143614f52411cad47db64e93bf3ba1cd547d6ca9591296223b5f0528b3b61"
        )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("autoconf", type="build")
    depends_on("autoconf-archive", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("mysql-client")
    # Older versions of mysql use openssl-1.x, causing build issues:
    depends_on("mysql@8.0.35:", when="^[virtuals=mysql-client] mysql")
    depends_on("libevent")
    depends_on("pcre")
    depends_on("go")

    def autoreconf(self, spec, prefix):
        Executable("./bootstrap.sh")()

    def configure_args(self):
        mysql_prefix = self.spec["mysql-client"].prefix
        if self.spec.satisfies("^[virtuals=mysql-client] mysql"):
            mysql_config = mysql_prefix.bin.mysql_config
        else:
            mysql_config = mysql_prefix.bin.mariadb_config

        args = [
            "--enable-server",
            "--enable-proxy",
            "--enable-agent",
            "--enable-agent2",
            f"--with-mysql={mysql_config}",
            f"--with-libevent={self.spec['libevent'].prefix}",
            f"--with-libpcre={self.spec['pcre'].prefix}",
        ]

        return args

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
