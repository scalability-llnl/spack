# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bats(Package):
    """Bats is a TAP-compliant testing framework for Bash."""

    homepage = "https://github.com/bats-core/bats-core"
    url = "https://github.com/bats-core/bats-core/archive/refs/tags/v1.10.0.tar.gz"

    license("MIT")

    version("1.10.0", sha256="a1a9f7875aa4b6a9480ca384d5865f1ccf1b0b1faead6b47aa47d79709a5c5fd")
    version(
        "0.4.0",
        sha256="480d8d64f1681eee78d1002527f3f06e1ac01e173b761bc73d0cf33f4dc1d8d7",
        url="https://github.com/sstephenson/bats/archive/v0.4.0.tar.gz",
    )

    def install(self, spec, prefix):
        bash = which("bash")
        bash("./install.sh", prefix)
