# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class VbzCompression(CMakePackage):
    """
    VBZ Compression uses variable byte integer encoding to compress nanopore signal data and is built using the following libraries:

    https://github.com/lemire/streamvbyte
    https://github.com/facebook/zstd

    The performance of VBZ is achieved by taking advantage of the properties of the raw signal and therefore is most effective when applied to the signal dataset.
    Other datasets you may have in your Fast5 files will not be able to take advantage of the default VBZ settings for compression.
    VBZ will be used as the default compression scheme in a future release of MinKNOW.
    """

    homepage = "https://nanoporetech.com"
    git = "https://github.com/nanoporetech/vbz_compression.git"

    license("MPL-2.0")

    version("1.0.3", commit="02fb8f50b93921ffa3c040106e809aaf8adbe5c5", submodules=True)
    version("1.0.2", commit="3f77a01c6a0a41707b7a5bcea959e734178b6ce2", submodules=True)
    version("1.0.1", commit="975cbcf33640d131b5cf2d2a124eed1a702b54f7", submodules=True)
    version("1.0.0", commit="2db0e3f62fa7a612dc42dc802401c26781eed068", submodules=True)
    version("0.9.3", commit="9a748efcdd0754be835e1080cf7086f3451e17d1", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.11:", type="build")
    depends_on("zstd@1.3.1:")
    depends_on("hdf5@1.8.16:")

    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Release", "Default"),
    )

    def cmake_args(self):
        args = [
            self.define("ENABLE_CONAN", False),
            self.define("ENABLE_PERF_TESTING", False),
            self.define("ENABLE_PYTHON", False),
        ]
        return args
