# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libatasmart(AutotoolsPackage):
    """A small and lightweight parser library for ATA S.M.A.R.T. hard disk
    health monitoring."""

    homepage = "https://github.com/ebe-forks/libatasmart"
    url = "https://github.com/ebe-forks/libatasmart/archive/v0.19.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.19", sha256="10bb5321a254e28bd60fd297f284bfc81cce4fde92e150187640e62ec667e5fb")
    version("0.18", sha256="4a6e93fbaec2d4caffb06ddd47c2c35ea4ad2d3d22e805bf284adba949f64ddf")
    version("0.17", sha256="353b2ec097814254989a809fd495f95a315e608fdf320c2b96dc52d70392e955")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
