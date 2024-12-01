# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Hyperqueue(Package):
    """Scheduler for sub-node tasks for HPC systems with batch scheduling"""

    homepage = "https://it4innovations.github.io/hyperqueue"
    url = "https://github.com/It4innovations/hyperqueue/archive/refs/tags/v0.11.0.tar.gz"
    git = "https://github.com/It4innovations/hyperqueue"

    maintainers("Nortamo", "Kobzol")

    license("MIT")

    version("main", branch="main")
    version(
        "0.12.0-rc1", sha256="0c7b5d567bb6cb8dd4e7bafdf784b0379cef74b3aecb958c7f20248f8fedfbc1"
    )
    version(
        "0.11.0",
        preferred=True,
        sha256="07fa7eda3a8a5278e058a526fee92e1e524370813b362aaa1a5dfc49d1f3fc28",
    )
    version("0.10.0", sha256="dc022170bf45479cb03edfe55a2fde066e7bf69542f644a8e78db604e8c6d67f")
    version("0.9.0", sha256="49be05b3a042382ee31dddea9a5de64d3e3ff747cb2c47fa170b407fa8fdd2e1")

    depends_on("rust@1.59:")

    def install(self, spec, prefix):
        cargo = which("cargo")
        cargo("install", "--root", prefix, "--path", "crates/hyperqueue")
