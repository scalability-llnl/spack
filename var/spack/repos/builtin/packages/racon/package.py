# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Racon(CMakePackage):
    """Ultrafast consensus module for raw de novo genome assembly of long
    uncorrected reads."""

    homepage = "https://github.com/lbcb-sci/racon"
    url = "https://github.com/lbcb-sci/racon/archive/refs/tags/1.5.0.tar.gz"

    license("MIT")

    def url_for_version(self, version):
        if version <= Version("1.4.3"):
            return f"https://github.com/isovic/racon/releases/download/{version}/racon-v{version}.tar.gz"

        return f"https://github.com/lbcb-sci/racon/archive/refs/tags/{version}.tar.gz"

    version("1.5.0", sha256="41e362f71cc03b934f17d6e2c0d626e1b2997258261b14551586de006666424a")
    version("1.4.21", sha256="be293cb26d167c5353cacba69f4c86cb6924e234c5e1902e8e4e68ed70217d66")
    version("1.4.20", sha256="50c22e66a1141c865b70917eecf34155b9ab3a4642765381c30f64557bdb2a9f")
    version("1.4.13", sha256="e91e6a7170554230089ebea19b2c2b5134a1677247830d8c5a3b6aa686241387")
    version("1.4.12", sha256="658e04c6f282f53bcc8ffd2c7f97a787b97447d41fef29727eddd96d576efbae")
    version("1.4.11", sha256="f1a45b5a8928ed2e133e6262a0887a99ec19dfba9143cdb8d4747d4530fa699e")
    version("1.4.10", sha256="101c1ba967eda296fea6f88c7ee7b01eb5c912b253dd0b0fdd80399b504808cb")
    version("1.4.9", sha256="ae0bef208271166dd6325440131e408386408c12a9497d8d743504908ecb45e8")
    version("1.4.7", sha256="75e39395ced636dd0f5ef1abe431d8f9f6404eb0a806c530cff8e4fa4f57fab7")
    version("1.4.6", sha256="6514e89e4e6eea1d14fc1b760c4ccd02a833443284259d52628eeea0eb5f70db")
    version(
        "1.4.3",
        sha256="dfce0bae8234c414ef72b690247701b4299e39a2593bcda548a7a864f51de7f2",
        deprecated=True,
    )
    version(
        "1.4.2",
        sha256="b36d8b767e0fc9acdd3e9d34c99a8bbc02a3aae7a953c57923d935ebdf332700",
        deprecated=True,
    )
    version(
        "1.4.0",
        sha256="3e1e97388f428326342dead3f8500e72b1986f292bdfd4d1be4a0d2a21f4cc61",
        deprecated=True,
    )
    version(
        "1.3.3",
        sha256="174afde420ed2e187e57c1a6e9fc6a414aa26723b4ae83c3904640fc84941e66",
        deprecated=True,
    )
    version(
        "1.3.2",
        sha256="7c99380a0f1091f5ee138b559e318d7e9463d3145eac026bf236751c2c4b92c7",
        deprecated=True,
    )
    version(
        "1.3.1",
        sha256="7ce3b1ce6abdb6c6a63d50755b1fc55d5a4d2ab8f86a1df81890d4a7842d9b75",
        deprecated=True,
    )
    version(
        "1.3.0",
        sha256="f2331fb88eae5c54227dc16651607af6f045ae1ccccc1d117011762927d4606a",
        deprecated=True,
    )
    version(
        "1.2.1",
        sha256="6e4b752b7cb6ab13b5e8cb9db58188cf1a3a61c4dcc565c8849bf4868b891bf8",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.2:", type="build")
    depends_on("python", type="build")
    depends_on("sse2neon", when="target=aarch64:")

    conflicts("%gcc@:4.7")
    conflicts("%clang@:3.1")

    patch("aarch64.patch", when="@:1.4 target=aarch64:")

    def cmake_args(self):
        args = ["-Dracon_build_wrapper=ON"]
        return args
