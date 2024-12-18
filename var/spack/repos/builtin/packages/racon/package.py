# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Racon(CMakePackage):
    """Ultrafast consensus module for raw de novo genome assembly of long
    uncorrected reads."""

    homepage = "https://github.com/isovic/racon"
    url = "https://github.com/isovic/racon/releases/download/1.2.1/racon-v1.2.1.tar.gz"

    license("MIT")

    version("1.4.3", sha256="dfce0bae8234c414ef72b690247701b4299e39a2593bcda548a7a864f51de7f2")
    version("1.4.2", sha256="b36d8b767e0fc9acdd3e9d34c99a8bbc02a3aae7a953c57923d935ebdf332700")
    version("1.4.0", sha256="3e1e97388f428326342dead3f8500e72b1986f292bdfd4d1be4a0d2a21f4cc61")
    version("1.3.3", sha256="174afde420ed2e187e57c1a6e9fc6a414aa26723b4ae83c3904640fc84941e66")
    version("1.3.2", sha256="7c99380a0f1091f5ee138b559e318d7e9463d3145eac026bf236751c2c4b92c7")
    version("1.3.1", sha256="7ce3b1ce6abdb6c6a63d50755b1fc55d5a4d2ab8f86a1df81890d4a7842d9b75")
    version("1.3.0", sha256="f2331fb88eae5c54227dc16651607af6f045ae1ccccc1d117011762927d4606a")
    version("1.2.1", sha256="6e4b752b7cb6ab13b5e8cb9db58188cf1a3a61c4dcc565c8849bf4868b891bf8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.2:", type="build")
    depends_on("python", type="build")
    depends_on("sse2neon", when="target=aarch64:")

    conflicts("%gcc@:4.7,10.1.0:")
    conflicts("%clang@:3.1")

    patch("aarch64.patch", when="target=aarch64:")

    def cmake_args(self):
        args = ["-Dracon_build_wrapper=ON"]
        return args
