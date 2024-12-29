# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lmbench(MakefilePackage):
    """lmbench is a suite of simple, portable, ANSI/C microbenchmarks for
    UNIX/POSIX. In general, it measures two key features: latency and
    bandwidth. lmbench is intended to give system developers insight into
    basic costs of key operations."""

    homepage = "https://lmbench.sourceforge.net/"
    git = "https://github.com/intel/lmbench.git"

    license("GPL-2.0-only")

    version("master", branch="master")

    depends_on("c", type="build")  # generated

    depends_on("libtirpc")

    patch(
        "fix_results_path_for_aarch64.patch",
        sha256="2af57abc9058c56b6dd0697bb01a98902230bef92b117017e318faba148eef60",
        when="target=aarch64:",
    )

    def setup_build_environment(self, env):
        env.prepend_path("CPATH", self.spec["libtirpc"].prefix.include.tirpc)
        env.append_flags("LDFLAGS", "-ltirpc")

    def build(self, spec, prefix):
        make("build")

    def install(self, spec, prefix):
        install_tree(".", prefix)
