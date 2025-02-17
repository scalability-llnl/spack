# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


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
    depends_on("boost")
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
