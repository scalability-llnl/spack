# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libibumad(CMakePackage):
    """This package installs the user-space libraries and headers for libibumad.
    This is a subset of the linux-rdma distribution."""

    homepage = "https://github.com/linux-rdma/"
    url = "https://github.com/linux-rdma/rdma-core/archive/v25.0.tar.gz"

    license("GPL-2.0-only OR BSD-2-Clause")

    version("46.0", sha256="23fd2a5a656f7d147796660c3d3728b31287bc70a3e913e28ea5da7f39269229")
    version("44.1", sha256="1dec7e25dd248f1ff4d262e5674297205ad9113a4ff25ab7ecbb75a824adac27")
    version("25.0", sha256="d735bd091d13e8a68ce650e432b5bdc934fc7f1d5fb42a6045278a5b3f7fe48b")

    depends_on("c", type="build")  # generated

    depends_on("libnl")

    def build(self, spec, prefix):
        with working_dir(join_path(self.build_directory, "libibumad")):
            make()

    def install(self, spec, prefix):
        with working_dir(join_path(self.build_directory, "libibumad")):
            make("install")
