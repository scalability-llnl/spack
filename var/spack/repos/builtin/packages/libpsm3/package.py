# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Libpsm3(AutotoolsPackage):
    """PSM3 provider for the PSM3 OFI provider"""

    homepage = "https://ofiwg.github.io/libfabric/v1.12.0/man/fi_psm3.7.html"
    url = "https://github.com/intel/eth-psm3-fi/archive/refs/tags/v11.4.1.0.tar.gz"
    git = "https://github.com/intel/eth-psm3-fi.git"

    version(
        "11.5.1.1",
        sha256="59fe731f4dd2cfcd90c8274df1c6ca9014a45cdebfdf1f1a830fcb8fcb65bb79",
        preferred=True,
    )
    version("11.4.1.0", sha256="272adb9ec10edf709bfcfccc6b6e9296d25d892c36b845ad577caeb82b70c9ac")

    depends_on("c", type="build")  # generated

    variant("atomics", default=True, description="Enable atomics")
    variant("debug", default=False, description="Enable debugging")
    variant("sockets", default=True, description="Enable PSM3 sockets")
    variant("verbs", default=False, description="Enable PSM3 verbs")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("numactl")
    depends_on("uuid")

    maintainers("dodecatheon", "douglasjacobsen")

    def configure_args(self):
        config_args = []
        config_args.extend(self.enable_or_disable("atomics"))
        config_args.extend(self.enable_or_disable("debug"))
        config_args += self.enable_or_disable("psm3-sockets", variant="sockets")
        config_args += self.enable_or_disable("psm3-verbs", variant="verbs")
        return config_args

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        install_tree("src/.libs", prefix.lib)
        os.unlink("%s/libpsm3-fi.la" % prefix.lib)
        install("src/libpsm3-fi.la", prefix.lib)

    def setup_run_environment(self, env):
        env.prepend_path("FI_PROVIDER_PATH", self.prefix.lib)
        env.set("FI_PROVIDER", "psm3")
        env.set("PSM3_ALLOW_ROUTERS", "1")
        if self.spec.satisfies("+sockets ~verbs"):
            env.set("PSM3_HAL", "sockets")
        env.set("FI_PSM3_NAME_SERVER", "1")
        if self.spec.satisfies("+debug"):
            env.set("PSM3_IDENTIFY", "1")
