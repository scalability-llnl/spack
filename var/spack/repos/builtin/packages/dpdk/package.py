# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.makefile import MakefileBuilder
from spack.build_systems.meson import MesonBuilder
from spack.package import *


class Dpdk(MakefilePackage, MesonPackage):
    """DPDK is a set of libraries and drivers for fast packet processing.
    It supports many processor architectures and both FreeBSD and Linux."""

    homepage = "https://github.com/DPDK/dpdk"
    url = "https://github.com/DPDK/dpdk/archive/v23.03.tar.gz"
    git = "https://github.com/DPDK/dpdk"

    maintainers("hyoklee")

    license("BSD-3-Clause AND GPL-2.0-only")

    version("main", branch="main")
    version("23.03", sha256="8a8fa67941b1e0d428937f9068f401457e4e4fd576031479450da065385b332c")
    version("22.11", sha256="ed8b2a2b153f0311ffa065d35af29a098367af44a22b3c33e191e1a74211f2e3")
    version("20.02", sha256="29e56ea8e47e30110ecb881fa5a37125a865dd2d45b61f68e93e334caaab16b7")
    version("19.11", sha256="ce1befb20a5e5c5399b326a39cfa23314a5229c0ced2553f53b09b1ae630706b")
    version("19.08", sha256="1ceff1a6f4f8d5f6f62c1682097249227ac5225ccd9638e0af09f5411c681038")
    version("19.05", sha256="5fea95cb726e6adaa506dab330e79563ccd4dacf03f126c826aabdced605d32b")
    version("19.02", sha256="04885d32c86fff5aefcfffdb8257fed405233602dbcd22f8298be13c2e285a50")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    conflicts("target=aarch64:", msg="DPDK is not supported on aarch64.")

    # Build system
    build_system(
        conditional("meson", when="@22.11:"),
        conditional("makefile", when="@:20.02"),
        default="meson",
    )

    with when("build_system=meson"):
        depends_on("cmake@3.9:", type="build")
        depends_on("ninja", type="build")
        depends_on("py-pyelftools", when="@22.11:")
    depends_on("numactl")


class MesonBuilder(MesonBuilder):
    def meson_args(self):
        return ["--warnlevel=3"]


class MakefileBuilder(MakefileBuilder):
    def build(self, pkg, spec, prefix):
        make("defconfig")
        make()

    def install(self, pkg, spec, prefix):
        install_tree(".", prefix)
