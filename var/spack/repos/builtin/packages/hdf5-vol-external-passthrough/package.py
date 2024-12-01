# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hdf5VolExternalPassthrough(CMakePackage):
    """Package for HDF5 external pass-through VOL."""

    homepage = "https://sdm.lbl.gov/"
    url = "https://github.com/hpc-io/vol-external-passthrough/archive/refs/tags/v1.1.tar.gz"
    git = "https://github.com/hpc-io/vol-external-passthrough.git"
    maintainers("hyoklee")

    version("develop", branch="develop")
    version("1.1", sha256="9f1a7fba4958fe0f46b4451253b9b1d7a4cfb30a0ce4183f5f756ceaddbbf2c3")

    depends_on("c", type="build")  # generated
    depends_on("hdf5@1.14.0:")

    def cmake_args(self):
        args = [
            self.define("BUILD_SHARED_LIBS:BOOL", True),
            self.define("BUILD_TESTING:BOOL=ON", self.run_tests),
        ]
        return args
