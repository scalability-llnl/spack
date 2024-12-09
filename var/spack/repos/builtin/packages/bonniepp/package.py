# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bonniepp(AutotoolsPackage):
    """Bonnie++ is a benchmark suite that is aimed at performing a number of
    simple tests of hard drive and file system performance."""

    homepage = "https://doc.coker.com.au/projects/bonnie"
    url = "https://www.coker.com.au/bonnie++/bonnie++-1.98.tgz"

    version("1.98", sha256="6e0bcbc08b78856fd998dd7bcb352d4615a99c26c2dc83d5b8345b102bad0b04")

    depends_on("cxx", type="build")  # generated

    def configure_args(self):
        configure_args = []
        configure_args.append("--enable-debug")
        return configure_args

    def setup_run_environment(self, env):
        """Prepend the sbin directory to PATH."""
        env.prepend_path("PATH", self.prefix.sbin)
