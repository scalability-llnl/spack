# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Xfsprogs(AutotoolsPackage):
    """XFS User Tools."""

    homepage = "https://github.com/mtanski/xfsprogs"
    url = "http://kernel.org/pub/linux/utils/fs/xfs/xfsprogs/xfsprogs-4.17.0.tar.xz"

    license("LGPL-2.1-or-later")

    version("6.11.0", sha256="dae3bb432196f7b183b2e6bd5dc44bf33edbd7d0e85bd37d25c235df81b8100a")
    version("6.10.1", sha256="6cb839be1a9535f8352441b3f6eea521ead5c5c7c913e8106cdfac96aa117041")
    version("6.10.0", sha256="a16e7caa5d8fea1c9652f1a45c8e5f2acc13fc632cf2066fe364ab13bd9df82d")
    version("6.9.0", sha256="975284783fb3fbc4e1ae640bd804d788e4237a86b07582acee86b6e48f6521b7")
    version("6.8.0", sha256="78b6ab776eebe5ab52e0884a70fa1b3633e64a282b1ecfae91f5dd1d9ec5f07d")
    version("6.7.0", sha256="e75d1e012853e11597411cfcb80e26c811881cf0ca03715e852b42946cc61e1f")
    version("6.6.0", sha256="50ca2f4676df8fab4cb4c3ef3dd512d5551e6844d40a65a31d5b8e03593d22df")
    version("6.5.0", sha256="8db81712b32756b97d89dd9a681ac5e325bbb75e585382cd4863fab7f9d021c6")
    version("6.4.0", sha256="c31868418bfbf49a3a9c47fc70cdffde9d96f4ff0051bd04a0881e6654648104")
    version("6.3.0", sha256="ec987c9f0bcb2db2991bffb80d353150b389c3a2b79b6830411f7042adf6990c")
    version("6.2.0", sha256="d67dcba5a28e0904b60886b6e5f752bc7c9c3a5c7096153855b5adca9db86c51")
    version("6.1.1", sha256="05e8a137870db1d6182df72dda98ab7a7100deb376947e854b9d59c914c2c7bb")
    version("6.1.0", sha256="eceb9015c4ebefa56fa85faff756ccb51ed2cf9c39ba239767f8e78705e85251")
    version("6.0.0", sha256="b77cec2364aab0b8ae8d8c67daac7fdb3801e0979f1d8328d9c3469e57ca9ca0")
    version("5.11.0", sha256="0e9c390fcdbb8a79e1b8f5e6e25fd529fc9f9c2ef8f2d5e647b3556b82d1b353")
    version("5.8.0", sha256="8ef46ed9e6bb927f407f541dc4324857c908ddf1374265edc910d23724048c6b")
    version("5.7.0", sha256="8f2348a68a686a3f4491dda5d62dd32d885fbc52d32875edd41e2c296e7b4f35")
    version("5.6.0", sha256="0aba2aac5d80d07646dde868437fc337af2c7326edadcc6d6a7c0bfd3190c1e6")

    version("4.20.0", sha256="beafdfd080352a8c9d543491e0874d0e8809cb643a3b9d352d5feed38d77022a")

    depends_on("c", type="build")  # generated

    depends_on("libinih")
    depends_on("gettext")
    depends_on("gettext@:0.21.1", when="@:6.3")
    depends_on("uuid")
    depends_on("util-linux")
    depends_on("liburcu", when="@6:")

    def flag_handler(self, name, flags):
        if name == "cflags":
            if self.spec.satisfies("@:5.4.0 %gcc@10:"):
                flags.append("-fcommon")
        elif name == "ldlibs" or name == "ldflags":
            if "intl" in self.spec["gettext"].libs.names:
                flags.append("-lintl")
        return build_system_flags(name, flags)

    def setup_build_environment(self, env):
        env.append_path("C_INCLUDE_PATH", self.spec["util-linux"].prefix.include.blkid)

    def configure_args(self):
        args = ["--with-systemd-unit-dir=" + self.spec["xfsprogs"].prefix.lib.systemd.system]
        if self.spec.satisfies("@6.5.0:"):
            args.append("--with-udev-rule-dir=" + self.spec["xfsprogs"].prefix)
        return args

    def install(self, spec, prefix):
        make("install")
        make("install-dev")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
