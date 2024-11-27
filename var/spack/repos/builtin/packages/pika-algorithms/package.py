# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PikaAlgorithms(CMakePackage):
    """C++ parallel algorithms built on pika."""

    homepage = "https://github.com/pika-org/pika-algorithms/"
    url = "https://github.com/pika-org/pika-algorithms/archive/0.0.0.tar.gz"
    git = "https://github.com/pika-org/pika-algorithms.git"
    maintainers("msimberg", "albestro", "teonnik", "aurianer")

    license("BSL-1.0")

    version("0.1.4", sha256="67ea5e8545b234f82dcc75612a774f2e3df8425a283f2034c2d1e2e5ac74f945")
    version("0.1.3", sha256="53b79fcc0e5decc0a4d70abf0897a4f66141b85eea6d65013f51eec02ad123b7")
    version("0.1.2", sha256="286cf5c4db06717fa66c681cec8c99207154dd07e72d72f2b5b4a3cb9ff698bf")
    version("0.1.1", sha256="4aae88ac19864fd278bbdb49ae56348014c3d0d4b49a46ab3b9ba8a180f745f6")
    version("0.1.0", sha256="64da008897dfa7373155595c46d2ce6b97a8a3cb5bea33ae7f2d1ff359f0d9b6")
    version("main", branch="main")

    depends_on("cxx", type="build")

    generator("ninja")

    map_cxxstd = lambda cxxstd: "2a" if cxxstd == "20" else cxxstd
    cxxstds = ("17", "20", "23")
    variant(
        "cxxstd",
        default="17",
        values=cxxstds,
        description="Use the specified C++ standard when building",
    )

    # Build dependencies
    depends_on("git", type="build")
    depends_on("cmake@3.22:", type="build")

    conflicts("%gcc@:8")
    conflicts("%clang@:8")
    conflicts("cxxstd=23", when="^cmake@:3.20.2")

    # Other dependencies
    depends_on("boost@1.71:")
    depends_on("fmt@9:")
    depends_on("pika@0.11:0.20")
    depends_on("pika@:0.11", when="@0.1.0")
    depends_on("pika@:0.12", when="@0.1.1")
    depends_on("pika@:0.15", when="@0.1.2")
    depends_on("pika@:0.16", when="@0.1.3")

    for cxxstd in cxxstds:
        depends_on("boost cxxstd={0}".format(map_cxxstd(cxxstd)), when="cxxstd={0}".format(cxxstd))
        depends_on("fmt cxxstd={0}".format(cxxstd), when="cxxstd={0}".format(cxxstd))
        depends_on("pika cxxstd={0}".format(cxxstd), when="cxxstd={0}".format(cxxstd))

    def cmake_args(self):
        return [
            self.define("PIKA_ALGORITHMS_WITH_CXX_STANDARD", self.spec.variants["cxxstd"].value)
        ]
