# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Thrust(Package, CMakePackage):
    """Thrust is a parallel algorithms library
    which resembles the C++ Standard Template Library (STL)."""

    homepage = "https://thrust.github.io"
    url = "https://github.com/NVIDIA/thrust/archive/1.12.0.tar.gz"
    git = "https://github.com/NVIDIA/thrust.git"

    license("BSL-1.0")

    # to support CMake build system package installation, Thrust
    # submodules must be downloaded, which aren't included in tarballs
    version("1.17.2", commit="1ac51f2b6219ff17d15d93f2e0be85038556f346", submodules=True)
    version("1.17.1", commit="4dd337f41622f5624359d6a958e3cb6ac7c6f57e", submodules=True)
    version("1.17.0", commit="6a3078c64cab0e2f276340fa5dcafa0d758ed890", submodules=True)
    # versions prior to 1.17 install from tarballs
    version("1.16.0", sha256="93b9553e3ee544e05395022bea67e6d600f8f3eb680950ec7cf73c0f55162487")
    version("1.15.0", sha256="0eeaf5a77cd7cb143f3443bd96b215ae1c4eacf18a712762e6a5c85213f80cc2")
    version("1.14.0", sha256="ddba9f3ed47b1a33562a4aea2d000a2ca2abcd45ff760af12aa81b8b7e492962")
    version("1.13.1", sha256="964fbd84eb146a53ff9d5a4422a2b256c5bce27579d9afe1a4be5fa5ebcb67d6")
    version("1.13.0", sha256="f43306ae4230efdd78a8ce82fb10685676b27ce692777ee5c5a3361ced305d63")
    version("1.12.1", sha256="0a7f8a57e5ffb3ba25aaf528d5a5c9d090973afba1c395da856c5353f9bd1690")
    version("1.12.0", sha256="d68f89937ed1a0dadafd4f77d3e65ab9a5baa48dd5fa5698f8d3f7e3d6749da2")
    version(
        "1.12.0-rc0", sha256="458c5ccc8572af00b3176af0f45f5f7eeb5af737bcc0a853982b55afcbe4cef6"
    )
    version("1.11.0", sha256="c65211a66fe0dce9f5470cc8fcb80ae6b04da12fd94707ed63ddddbd82fa9444")
    version("1.10.0", sha256="8149b30eabbc9a2af5f038fb2b7f91070d4e01266377e0cd12e3af3feda93f8f")
    version("1.9.10-1", sha256="9aed4adf97e3fcb2627a5f62bf4b0669af074475fe717952c29254eee413d98a")
    version("1.9.10", sha256="5071c995a03e97e2bcfe0c5cc265330160316733336bb87dfcea3fc381065316")
    version("1.9.9", sha256="74740b94e0c62e1e54f9880cf1eeb2d0bfb2203ae35fd72ece608f9b8e073ef7")
    version("1.9.8-1", sha256="7d8d927e610272ff59a2afc5d90d69cf6ad886dbf9eb7d7ab25bc86f15f8ed52")
    version("1.9.8", sha256="d014396a2128417bd1421ba80d2601422577094c0ff727c60bd3c6eb4856af9b")
    version("1.9.7-1", sha256="c3c433c04a420afd351de44c0e40711d5813092b76f0cfa901a3119b75ab8118")
    version("1.9.7", sha256="72519f7f6b5d28953e5086253bbcf5b10decde913ddeb93872dc51522bdfad2b")
    version("1.9.6-1", sha256="66261f0272082f1752fe66b0ed5907cf292946b7276fc777d21bc86bd16460fe")
    version("1.9.6", sha256="67e937c31d279cec9ad2c54a4f66e479dfbe506ceb0253f611a54323fb4c1cfb")
    version("1.9.5", sha256="d155dc2a260fe0c75c63c185fa4c4b4c6c5b7c444fcdac7109bb71941c9603f1")
    version("1.9.4", sha256="41931a7d73331fc39c6bea56d1eb8d4d8bbf7c73688979bbdab0e55772f538d1")
    version("1.9.3", sha256="92482ad0219cd2d727766f42a4fc952d7c5fd0183c5e201d9a117568387b4fd1")
    version("1.9.2", sha256="1fb1272be9e8c28973f5c39eb230d1914375ef38bcaacf09a3fa51c6b710b756")
    version("1.9.1", sha256="7cf59bf42a7b05bc6799c88269bf41eb637ca2897726a5ade334a1b8b4579ef1")
    version("1.9.0", sha256="a98cf59fc145dd161471291d4816f399b809eb0db2f7085acc7e3ebc06558b37")
    version("1.8.3", sha256="2254200512fde7f4fd0fc74306286e192ea6ac9037576dbd31309c0579229dbb")
    version("1.8.2", sha256="83bc9e7b769daa04324c986eeaf48fcb53c2dda26bcc77cb3c07f4b1c359feb8")

    depends_on("cxx", type="build")  # generated

    # leave the build system of pre-1.17 as originally implemented,
    # but use CMake for newer versions
    build_system(
        conditional("cmake", when="@1.17:"), conditional("generic", when="@:1.16"), default="cmake"
    )

    # minimum CMake version is 3.15 for plain package installation (no
    # examples, tests, etc)
    depends_on("cmake@3.15:", when="@1.17:", type="build")


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        return [
            self.define("THRUST_ENABLE_HEADER_TESTING", "OFF"),
            self.define("THRUST_ENABLE_TESTING", "OFF"),
            self.define("THRUST_ENABLE_EXAMPLES", "OFF"),
            self.define("THRUST_ENABLE_BENCHMARKS", "OFF"),
            self.define("THRUST_INCLUDE_CUB_CMAKE", "OFF"),
        ]


class GenericBuilder(spack.build_systems.generic.GenericBuilder):
    def install(self, pkg, spec, prefix):
        install_tree("doc", join_path(prefix, "doc"))
        install_tree("examples", join_path(prefix, "examples"))
        install_tree("thrust", join_path(prefix, "include", "thrust"))
