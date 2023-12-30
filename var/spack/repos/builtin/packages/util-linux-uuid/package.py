# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UtilLinuxUuid(AutotoolsPackage):
    """Util-linux is a suite of essential utilities for any Linux system."""

    homepage = "https://github.com/util-linux/util-linux"
    url = "https://www.kernel.org/pub/linux/utils/util-linux/v2.29/util-linux-2.29.2.tar.gz"
    list_url = "https://www.kernel.org/pub/linux/utils/util-linux"
    list_depth = 1

    license("GPL-2.0-or-later")

    version("2.38.1", sha256="0820eb8eea90408047e3715424bc6be771417047f683950fecb4bdd2e2cbbc6e")
    version("2.37.4", sha256="c8b7b4fa541f974cc32c1c6559d9bfca33651020a456ad6ee5fc9b0cacd00151")
    version("2.36.2", sha256="f5dbe79057e7d68e1a46fc04083fc558b26a49499b1b3f50e4f4893150970463")
    version("2.36", sha256="82942cd877a989f6d12d4ce2c757fb67ec53d8c5cd9af0537141ec5f84a2eea3")

    conflicts("%gcc@:4", when="@2.37:")

    depends_on("pkgconfig", type="build")

    provides("uuid")

    def url_for_version(self, version):
        url = "https://www.kernel.org/pub/linux/utils/util-linux/v{0}/util-linux-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    @property
    def libs(self):
        return find_libraries("libuuid", self.prefix, recursive=True)

    @property
    def headers(self):
        return find_headers("uuid", self.prefix, recursive=True)

    def configure_args(self):
        config_args = [
            "--disable-use-tty-group",
            "--disable-makeinstall-chown",
            "--without-systemd",
            "--disable-all-programs",
            "--without-python",
            "--enable-libuuid",
            "--disable-bash-completion",
        ]
        # Fixes #31123.
        if self.spec.satisfies("%intel"):
            config_args.append("CFLAGS=-restrict")
        return config_args
