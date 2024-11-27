# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Chemfiles(CMakePackage):
    """Chemfiles is a library providing a simple and format agnostic interface for
    reading and writing computational chemistry files: trajectories, configurations,
    and topologies."""

    homepage = "https://chemfiles.org"
    url = "https://github.com/chemfiles/chemfiles/archive/refs/tags/0.10.3.tar.gz"

    maintainers("RMeli")

    license("BSD-3-Clause")

    version("0.10.4", sha256="b8232ddaae2953538274982838aa6c2df87d300f7e2f80e92c171581e06325ba")
    version("0.10.3", sha256="5f53d87a668a85bebf04e0e8ace0f1db984573de1c54891ba7d37d31cced0408")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=False, description="Build shared libraries")

    def cmake_args(self):
        args = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]
        return args
