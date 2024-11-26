# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class UtilLinux(AutotoolsPackage):
    """Util-linux is a suite of essential utilities for any Linux system."""

    homepage = "https://github.com/util-linux/util-linux"
    url = "https://www.kernel.org/pub/linux/utils/util-linux/v2.29/util-linux-2.29.2.tar.gz"
    list_url = "https://www.kernel.org/pub/linux/utils/util-linux"
    list_depth = 1

    license("GPL-2.0-only", checked_by="wdconinc")

    version("2.40.2", sha256="7bec316b713a14c6be1a5721aa0e56a3b6170277329e6e1f1a56013cc91eece0")
    version("2.40", sha256="2a51d08cb71fd8e491e0cf633032c928f9a2848417f8441cb8cf7ef9971de916")
    version("2.39.3", sha256="40ea07584d56c310455471afa92c119ec259776a561af7159cc802344c2c370d")
    version("2.39.1", sha256="d7c8a58eb2c7248a32754eb3a3b6772e368b984d9907ada834c2cf3e13024270")
    version("2.38.1", sha256="0820eb8eea90408047e3715424bc6be771417047f683950fecb4bdd2e2cbbc6e")
    version("2.38", sha256="c31d4e54f30b56b0f7ec8b342658c07de81378f2c067941c2b886da356f8ad42")
    version("2.37.4", sha256="c8b7b4fa541f974cc32c1c6559d9bfca33651020a456ad6ee5fc9b0cacd00151")
    version("2.37.2", sha256="15db966474e459b33fa390a6b892190a92079a73ca45384cde4c86e6ed265a86")
    version("2.37.1", sha256="0fe9ee8ee7f157be8abcfc2902ec8de9fe30b39173b84e4c458675cef4709b35")
    version("2.37", sha256="faa8b46d080faa6f32c57da81eda871e38e1e27ba4e9b61cb2589334671aba50")
    version("2.36.2", sha256="f5dbe79057e7d68e1a46fc04083fc558b26a49499b1b3f50e4f4893150970463")
    version("2.36", sha256="82942cd877a989f6d12d4ce2c757fb67ec53d8c5cd9af0537141ec5f84a2eea3")
    version("2.35.1", sha256="37ac05d82c6410d89bc05d43cee101fefc8fe6cf6090b3ce7a1409a6f35db606")
    version("2.35", sha256="98acab129a8490265052e6c1e033ca96d68758a13bb7fcd232c06bf16cc96238")
    version("2.34", sha256="b62c92e5e1629642113cd41cec1ee86d1ee7e36b8ffe8ec3ac89c11797e9ac25")
    version("2.33.1", sha256="e15bd3142b3a0c97fffecaed9adfdef8ab1d29211215d7ae614c177ef826e73a")
    version("2.33", sha256="952fb0d3498e81bd67b3c48e283c80cb12c719bc2357ec5801e7d420991ad319")
    version("2.29.2", sha256="29ccdf91d2c3245dc705f0ad3bf729ac41d8adcdbeff914e797c552ecb04a4c7")
    version("2.29.1", sha256="a6a7adba65a368e6dad9582d9fbedee43126d990df51266eaee089a73c893653")
    version("2.25", sha256="7e43273a9e2ab99b5a54ac914fddf5d08ba7ab9b114c550e9f03474672bd23a1")

    depends_on("c", type="build")  # generated

    depends_on("python@2.7:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("ncurses", type="link")
    depends_on("zlib-api", type="link")  # sbin/mkfs.cramfs
    depends_on("libxcrypt", type="link")  # sbin/sulogin

    variant("bash", default=False, description="Install bash completion scripts")

    depends_on("bash", when="+bash", type="run")

    def url_for_version(self, version):
        url = "https://www.kernel.org/pub/linux/utils/util-linux/v{0}/util-linux-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    def configure_args(self):
        config_args = [
            "--disable-use-tty-group",
            "--disable-makeinstall-chown",
            "--without-systemd",
            "--disable-libuuid",
        ]
        if "+bash" in self.spec:
            config_args.extend(
                [
                    "--enable-bash-completion",
                    "--with-bashcompletiondir="
                    + os.path.join(
                        self.spec["bash"].prefix, "share", "bash-completion", "completions"
                    ),
                ]
            )
        else:
            config_args.append("--disable-bash-completion")

        if self.spec.satisfies("platform=darwin"):
            # Does not build on macOS
            config_args.extend(
                ["--disable-ipcs", "--disable-ipcrm", "--disable-wall", "--disable-libmount"]
            )

        if self.spec.satisfies("@2.40:"):
            # Disable liblastlog2, which depends on sqlite
            config_args.append("--disable-liblastlog2")

        return config_args

    def install(self, spec, prefix):
        make("install", parallel=False)
