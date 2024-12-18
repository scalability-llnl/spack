# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AbseilCpp(CMakePackage):
    """Abseil Common Libraries (C++)"""

    homepage = "https://abseil.io/"
    url = "https://github.com/abseil/abseil-cpp/archive/refs/tags/20211102.0.tar.gz"

    maintainers("jcftang")
    tags = ["windows"]

    license("Apache-2.0", checked_by="wdconinc")

    version(
        "20240722.0", sha256="f50e5ac311a81382da7fa75b97310e4b9006474f9560ac46f54a9967f07d4ae3"
    )
    version(
        "20240116.2", sha256="733726b8c3a6d39a4120d7e45ea8b41a434cdacde401cba500f14236c49b39dc"
    )
    version(
        "20240116.1", sha256="3c743204df78366ad2eaf236d6631d83f6bc928d1705dd0000b872e53b73dc6a"
    )
    version(
        "20230802.1", sha256="987ce98f02eefbaf930d6e38ab16aa05737234d7afbab2d5c4ea7adbe50c28ed"
    )
    version(
        "20230125.3", sha256="5366d7e7fa7ba0d915014d387b66d0d002c03236448e1ba9ef98122c13b35c36"
    )
    version(
        "20230125.2", sha256="9a2b5752d7bfade0bdeee2701de17c9480620f8b237e1964c1b9967c75374906"
    )
    version(
        "20220623.0", sha256="4208129b49006089ba1d6710845a45e31c59b0ab6bff9e5788a87f55c5abd602"
    )
    version(
        "20211102.0", sha256="dcf71b9cba8dc0ca9940c4b316a0c796be8fab42b070bb6b7cab62b48f0e66c4"
    )
    version(
        "20210324.2", sha256="59b862f50e710277f8ede96f083a5bb8d7c9595376146838b9580be90374ee1f"
    )
    version(
        "20210324.1", sha256="441db7c09a0565376ecacf0085b2d4c2bbedde6115d7773551bc116212c2a8d6"
    )
    version(
        "20210324.0", sha256="dd7db6815204c2a62a2160e32c55e97113b0a0178b2f090d6bab5ce36111db4b"
    )
    version(
        "20200923.3", sha256="ebe2ad1480d27383e4bf4211e2ca2ef312d5e6a09eba869fd2e8a5c5d553ded2"
    )
    version(
        "20200923.2", sha256="bf3f13b13a0095d926b25640e060f7e13881bd8a792705dd9e161f3c2b9aa976"
    )
    version(
        "20200923.1", sha256="808350c4d7238315717749bab0067a1acd208023d41eaf0c7360f29cc8bc8f21"
    )
    version(
        "20200225.2", sha256="f41868f7a938605c92936230081175d1eae87f6ea2c248f41077c8f88316f111"
    )
    version(
        "20200225.1", sha256="0db0d26f43ba6806a8a3338da3e646bb581f0ca5359b3a201d8fb8e4752fd5f8"
    )
    version("20190808", sha256="8100085dada279bf3ee00cd064d43b5f55e5d913be0dfe2906f06f8f28d5b37e")
    version("20181200", sha256="e2b53bfb685f5d4130b84c4f3050c81bf48c497614dc85d91dbd3ed9129bce6d")
    version("20180600", sha256="794d483dd9a19c43dc1fbbe284ce8956eb7f2600ef350dac4c602f9b4eb26e90")

    depends_on("cxx", type="build")  # generated

    # Avoid export of testonly target absl::test_allocator in CMake builds
    patch(
        "https://github.com/abseil/abseil-cpp/commit/779a3565ac6c5b69dd1ab9183e500a27633117d5.patch?full_index=1",
        sha256="14ad7abbc20b10d57e00d0940e8338f69fd69f58d8285214848998e8687688cc",
        when="@20240116",
    )

    variant("shared", default=True, description="Build shared instead of static libraries")

    conflicts("+shared", when="@:20190808")

    variant(
        "cxxstd",
        values=(conditional("11", when="@:2022"), "14", "17", "20"),
        default="14",
        description="C++ standard used during compilation",
    )

    depends_on("cmake@3.16:", when="@20240722:", type="build")
    depends_on("cmake@3.10:", when="@20220907:", type="build")
    depends_on("cmake@3.5:", when="@20190312:", type="build")
    depends_on("cmake@3.1:", type="build")

    depends_on("googletest", type="build", when="@20220623:")

    def cmake_args(self):
        run_tests = self.run_tests and self.spec.satisfies("@20220623:")
        return [
            self.define("BUILD_TESTING", run_tests),
            self.define("ABSL_BUILD_TESTING", run_tests),
            self.define("ABSL_USE_EXTERNAL_GOOGLETEST", run_tests),
            self.define("ABSL_FIND_GOOGLETEST", run_tests),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
        ]
