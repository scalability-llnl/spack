# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ModeltestNg(CMakePackage):
    """Best-fit model selection"""

    homepage = "https://github.com/ddarriba/modeltest"
    url = "https://github.com/ddarriba/modeltest/archive/refs/tags/v0.1.7.tar.gz"
    git = "https://github.com/ddarriba/modeltest.git"

    maintainers("snehring")

    license("GPL-3.0-only")

    version("20220721", commit="1066356b984100897b8bd38ac771c5c950984c01", submodules=True)
    version("0.1.7", commit="cc028888f1d4222aaa53b99c6b02cd934a279001", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("mpi", default=False, description="Enable MPI")

    depends_on("glib")
    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("openmpi", when="+mpi")

    # 40217: ICE by gcc-toolset-12-gcc-12.2.1-7.4.el8.aarch64 of Rocky Linux 8.8:
    conflicts("%gcc@12.2.0:12.2", when="target=aarch64:", msg="ICE with gcc@12.2 on aarch64")

    requires(
        "@20220721:", when="target=aarch64:", msg="Support for aarch64 was added after 20220721."
    )

    def cmake_args(self):
        return [self.define_from_variant("ENABLE_MPI", "mpi")]
