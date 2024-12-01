# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Libcudf(CMakePackage):
    """Built based on the Apache Arrow columnar memory format,
    cuDF is a GPU DataFrame library for loading, joining,
    aggregating, filtering, and otherwise manipulating data."""

    homepage = "https://rapids.ai"
    url = "https://github.com/rapidsai/cudf/archive/v0.15.0.tar.gz"

    license("Apache-2.0")

    version("0.15.0", sha256="2570636b72cce4c52f71e36307f51f630e2f9ea94a1abc018d40ce919ba990e4")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.14:", type="build")
    depends_on("cuda@10.0:")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on("arrow+cuda+orc+parquet")
    depends_on("librmm")
    depends_on("dlpack")

    root_cmakelists_dir = "cpp"

    def cmake_args(self):
        args = []

        # args.append('-DGPU_ARCHES')
        args.append("-DUSE_NVTX=ON")
        args.append("-DBUILD_BENCHMARKS=OFF")
        args.append("-DDISABLE_DEPRICATION_WARNING=ON")
        args.append("-DPER_THREAD_DEFAULT_STREAM=OFF")
        return args
