# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Diamond(CMakePackage):
    """DIAMOND is a sequence aligner for protein and translated DNA searches,
    designed for high performance analysis of big sequence data."""

    homepage = "https://ab.inf.uni-tuebingen.de/software/diamond"
    url = "https://github.com/bbuchfink/diamond/archive/v2.0.9.tar.gz"
    maintainers("snehring")

    license("GPL-3.0-only")

    version("2.1.9", sha256="4cde9df78c63e8aef9df1e3265cd06a93ce1b047d6dba513a1437719b70e9d88")
    version("2.1.8", sha256="b6088259f2bc92d1f9dc4add44590cff68321bcbf91eefbc295a3525118b9415")
    version("2.1.7", sha256="2dcaba0e79ecb02c3d2a6816d317e714767118a9a056721643abff4c586ca95b")
    version("2.1.6", sha256="852d27c7535d53f1ce59db0625ff23ac3bf17e57f7a3b1c46c08718f77e19c54")
    version("2.0.15", sha256="cc8e1f3fd357d286cf6585b21321bd25af69aae16ae1a8f605ea603c1886ffa4")
    version("2.0.14", sha256="3eaef2b957e4ba845eac27a2ca3249aae4259ff1fe0ff5a21b094481328fdc53")
    version("2.0.11", sha256="41f3197aaafff9c42763fb7658b67f730ebc6dd3c0533c9c3d54bd3166e93f24")
    version("2.0.9", sha256="3019f1adb6411c6669a3a17351d0338ae02f6b3cab3c8a3bac91cf334dcda620")
    version("2.0.8", sha256="04eed7c83828f50c7d9a1d48fe7c50a4c753e008501dc639c6521cf8a756c43b")
    version("2.0.4", sha256="94e8fe72bdc28b83fd0f2d90c439b58b63b38263aa1a3905582ef68f614ae95d")
    version("0.9.25", sha256="65298f60cf9421dcc7669ce61642611cd9eeffc32f66fd39ebfa25dd64416808")
    version("0.9.23", sha256="0da5cdd5e5b77550ec0eaba2c6c431801cdd10d31606ca12f952b57d3d31db92")
    version("0.9.22", sha256="35e518cfa0ac2fbc57e422d380bdb5123c6335742dd7965b76c34c95f241b729")
    version("0.9.21", sha256="3f10e089c24d24f3066f3a58fa01bf356c4044e0a0bcab081b9bf1a8d946c9b1")
    version("0.9.20", sha256="5cf629baf135f54dc93728e3618ae08c64c1ecb81b3f2d2d48fcfd1c010ed8f0")
    version("0.9.19", sha256="fab783f51af9010666f2b569f438fb38843d0201fe0c0e167db5b70d12459e30")
    version("0.9.14", sha256="de870a7806ac0aa47b97c9b784dd7201e2c8e11a122003bde440d926211b911e")
    version("0.8.38", sha256="582a7932f3aa73b0eac2275dd773818665f0b067b32a79ff5a13b0e3ca375f60")
    version("0.8.26", sha256="00d2be32dad76511a767ab8e917962c0ecc572bc808080be60dec028df45439f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("blas", when="+eigen")
    depends_on("blast-plus", when="+blast")
    depends_on("eigen", when="+eigen")
    depends_on("lapack", when="+eigen")
    depends_on("zlib-api")
    depends_on("zstd", when="+zstd")

    variant("zstd", default=False, description="Bulid with zstd support", when="@2.1.0:")
    variant("blast", default=True, description="Build with blast db support", when="@2.1.0:")
    variant("eigen", default=False, description="Build with Eigen support", when="@2.1.0:")

    requires("+zstd", when="+blast", msg="blast support requires zstd")

    conflicts("target=aarch64:", when="@:0.9.25")

    # fix error [-Wc++11-narrowing]
    # Ref: https://github.com/bbuchfink/diamond/commit/155e076d662b0e9268e2b00bef6d33d90aede7ff
    patch("fix_narrowing_error.patch", when="@:0.9.25")

    def cmake_args(self):
        args = [
            self.define_from_variant("WITH_ZSTD", "zstd"),
            self.define_from_variant("EIGEN_BLAS", "eigen"),
        ]
        if self.spec.satisfies("+blast"):
            args.extend(
                [
                    self.define(
                        "BLAST_INCLUDE_DIR",
                        join_path(self.spec["blast-plus"].prefix.include, "ncbi-tools++"),
                    ),
                    self.define("BLAST_LIBRARY_DIR", self.spec["blast-plus"].prefix.lib),
                ]
            )
        return args
