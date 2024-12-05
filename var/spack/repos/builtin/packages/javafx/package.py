# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *

_versions = {
    "20.0.1": {
        "linux": {
            "aarch64": (
                "https://download2.gluonhq.com/openjfx/20.0.1/openjfx-20.0.1_linux-aarch64_bin-sdk.zip",
                "ded4555c2fa097b3c0307ed3b338956ea1052d1693864c7594ec7ebb7e9486e2",
            ),
            "x86_64": (
                "https://download2.gluonhq.com/openjfx/20.0.1/openjfx-20.0.1_linux-x64_bin-sdk.zip",
                "882082b01a7f46792074cbe58e90136b81413438de184a941e051b836cbe90a2",
            ),
        },
        "darwin": {
            "arm64": (
                "https://download2.gluonhq.com/openjfx/20.0.1/openjfx-20.0.1_osx-aarch64_bin-sdk.zip",
                "baebdbbe283c17df62fc4c0bdc2bde4415f2253f99ba41437f9336e2272c255e",
            ),
            "x86_64": (
                "https://download2.gluonhq.com/openjfx/20.0.1/openjfx-20.0.1_osx-x64_bin-sdk.zip",
                "aa01f301bc611997f60ac86c2d9a7d7d1f652fd7092745720ae49cf7bb2935e4",
            ),
        },
    }
}


class Javafx(Package):
    """JavaFX allows you to create Java applications with a
    modern, hardware-accelerated user interface that is
    highly portable.
    """

    homepage = "https://openjfx.io/"
    for i in _versions:
        try:
            url, sha256 = _versions[i][platform.system().lower()][platform.machine()]
            version(i, url=url, sha256=sha256)
        except KeyError:
            continue

    skip_version_audit = ["platform=windows"]

    maintainers("snehring")

    extends("openjdk")

    conflicts("target=ppc64le:", msg="JavaFX is not available for ppc64le")
    conflicts("target=ppc64:", msg="JavaFX is not available for ppc64")
    conflicts("target=riscv64:", msg="JavaFX is not available for riscv64")
    conflicts("target=x86", msg="JavaFX is not available for x86")

    def install(self, spec, prefix):
        install_tree("legal", prefix.legal)
        install_tree("lib", prefix.lib)

    def setup_run_environment(self, env):
        env.set("JAVAFX_HOME", self.prefix.lib)
