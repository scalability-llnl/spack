# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xfsprogs(AutotoolsPackage):
    """XFS User Tools."""

    homepage = "https://github.com/mtanski/xfsprogs"
    url = "http://kernel.org/pub/linux/utils/fs/xfs/xfsprogs/xfsprogs-4.17.0.tar.xz"

    license("LGPL-2.1-or-later")

    version("5.11.0", sha256="0e9c390fcdbb8a79e1b8f5e6e25fd529fc9f9c2ef8f2d5e647b3556b82d1b353")
    version("5.8.0", sha256="8ef46ed9e6bb927f407f541dc4324857c908ddf1374265edc910d23724048c6b")
    version("5.7.0", sha256="8f2348a68a686a3f4491dda5d62dd32d885fbc52d32875edd41e2c296e7b4f35")
    version("5.6.0", sha256="0aba2aac5d80d07646dde868437fc337af2c7326edadcc6d6a7c0bfd3190c1e6")

    version("4.20.0", sha256="beafdfd080352a8c9d543491e0874d0e8809cb643a3b9d352d5feed38d77022a")

    depends_on("c", type="build")  # generated

    depends_on("libinih")
    depends_on("gettext")
    depends_on("uuid")
    depends_on("util-linux")

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("@:5.4.0 %gcc@10:"):
                flags.append("-fcommon")
        elif name == "ldlibs":
            if "intl" in self.spec["gettext"].libs.names:
                flags.append("-lintl")
        return build_system_flags(name, flags)

    def setup_build_environment(self, env):
        env.append_path("C_INCLUDE_PATH", self.spec["util-linux"].prefix.include.blkid)

    def configure_args(self):
        return ["--with-systemd-unit-dir=" + self.spec["xfsprogs"].prefix.lib.systemd.system]

    def install(self, spec, prefix):
        make("install")
        make("install-dev")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
