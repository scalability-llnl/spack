# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MsrSafe(MakefilePackage):
    """msr_safe provides controlled userspace access to model-specific registers (MSRs).
    It allows system administrators to give register-level read access and bit-level write
    access to trusted users in production environments. This access is useful where kernel
    drivers have not caught up with new processor features, or performance constraints
    requires batch access across dozens or hundreds of registers."""

    homepage = "https://github.com/LLNL/msr-safe"
    url = "https://github.com/LLNL/msr-safe/archive/refs/tags/v1.7.0.tar.gz"

    maintainers("kyotsukete", "rountree")

    license("GPL-2.0-only", checked_by="kyotsukete")

    variant(
        "test_linux699",
        default=False,
        description="This variant is for testing against Linux kernel 6.9.9",
    )

    requires("@0.0.0_linux6.9.9", when="+test_linux699")
    conflicts("@0.0.0_linux6.9.9", when="~test_linux699")

    # Version 0.0.0_linux6.9.9 is based on msr-safe@1.7.0 and solves for conflicts between 1.7.0
    # and the Linux kernel version 6.9.9.
    version(
        "0.0.0_linux6.9.9",
        sha256="2b68670eda4467eaa9ddd7340522ab2000cf9d16d083607f9c481650ea1a2fc9",
        url="https://github.com/rountree/msr-safe/archive/refs/heads/linux-6.9.9-cleanup.zip",
    )
    version("1.7.0", sha256="bdf4f96bde92a23dc3a98716611ebbe7d302005305adf6a368cb25da9c8a609a")
    version("1.6.0", sha256="defe9d12e2cdbcb1a9aa29bb09376d4156c3dbbeb7afc33315ca4b0b6859f5bb")
    version("1.5.0", sha256="e91bac281339bcb0d119a74d68a73eafb5944fd933a893e0e3209576b4c6f233")
    version("1.4.0", sha256="3e5a913e73978c9ce15ec5d2bf1a4583e9e5c30e4e75da0f76d9a7a6153398c0")
    version("1.3.0", sha256="718dcc78272b45ffddf520078e7e54b0b6ce272f1ef0376de009a133149982a0")
    version("1.2.0", sha256="d3c2e5280f94d65866f82a36fea50562dc3eaccbcaa81438562caaf35989d8e8")
    version("1.1.0", sha256="5b723e9d360e15f3ed854a84de7430b2b77be1eb1515db03c66456db43684a83")
    version("1.0.2", sha256="9511d021ab6510195e8cc3b0353a0ac414ab6965a188f47fbb8581f9156a970e")

    depends_on("linux-external-modules")

    @property
    def build_targets(self):
        return [
            "-C",
            f"{self.spec['linux-external-modules'].prefix}",
            f"M={self.build_directory}",
            "modules",
        ]

    @property
    def install_targets(self):
        return [f"DESTDIR={self.prefix}", "spack-install"]
