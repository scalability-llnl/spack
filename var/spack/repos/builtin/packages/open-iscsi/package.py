# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OpenIscsi(MakefilePackage):
    """The Open-iSCSI project is a high-performance, transport independent,
    multi-platform implementation of RFC3720 iSCSI."""

    homepage = "https://github.com/open-iscsi/"
    url = "https://github.com/open-iscsi/open-iscsi/archive/2.1.1.tar.gz"

    license("GPL-2.0-only")

    version("2.1.1", sha256="dfc1ea37f230f9d116f5b39c795b35be43002d65c81330ccd3878786532b811b")
    version("2.1.0", sha256="5b381b6a74bef3ca57cd8d5fa7a3ff07d45c8009b0e4aac5ba3a811ff0c48ee4")
    version("2.0.878", sha256="5aeef0069c4a9d7f288269bcf56588d09a3c529a35f865f16dd8119ab8672208")
    version("2.0.877", sha256="69eb95b0c39dee2da9d0d751bfdcdb8d11f9d37390de15c1a0b4558f9d0c4a57")
    version("2.0.876", sha256="9f01327d5e100ed794dc5083fc18dc4a06a0c29c77b252e21abd1b8f56edd9a7")

    depends_on("c", type="build")

    depends_on("gettext")
    depends_on("uuid")
    depends_on("util-linux")
    depends_on("kmod")
    depends_on("open-isns")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    def setup_build_environment(self, env):
        env.set("CFLAGS", "-DNO_SYSTEMD")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)

    def install(self, spec, prefix):
        etc_dir = join_path(prefix, "etc")
        make("install", f"prefix={prefix}", f"exec_prefix={prefix}", f"etcdir={etc_dir}")
