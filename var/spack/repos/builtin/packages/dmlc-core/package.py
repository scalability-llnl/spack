# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DmlcCore(CMakePackage):
    """DMLC-Core is the backbone library to support all DMLC projects,
    offers the bricks to build efficient and scalable
    distributed machine learning libraries."""

    homepage = "https://github.com/dmlc/dmlc-core"
    git = "https://github.com/dmlc/dmlc-core.git"

    license("Apache-2.0")

    version("master")
    version("20170508", commit="a6c5701219e635fea808d264aefc5b03c3aec314")

    depends_on("cxx", type="build")  # generated

    variant("openmp", default=False, description="Enable OpenMP support")

    patch("cmake.patch")

    def patch(self):
        filter_file("export CC = gcc", "", "make/config.mk", string=True)
        filter_file("export CXX = g++", "", "make/config.mk", string=True)
        filter_file("export MPICXX = mpicxx", "", "make/config.mk", string=True)
        filter_file(
            r"^USE_OPENMP\s*=.*",
            "USE_OPENMP=%s" % ("1" if "+openmp" in self.spec else "0"),
            "make/config.mk",
        )

    def cmake_args(self):
        return [self.define_from_variant("USE_OPENMP", "openmp")]
