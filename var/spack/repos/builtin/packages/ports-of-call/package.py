# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PortsOfCall(CMakePackage):
    """Ports of Call: Performance Portability Utilities"""

    homepage = "https://github.com/lanl/ports-of-call"
    url = "https://github.com/lanl/ports-of-call/archive/refs/tags/v1.1.0.tar.gz"
    git = "https://github.com/lanl/ports-of-call.git"

    maintainers("rbberger")

    license("BSD-3-Clause")

    version("main", branch="main")
    version("1.7.1", sha256="18b0b99370ef2adf3374248f653461606f826fe4076d0f19ac8c72d46035fdf5")
    version("1.7.0", sha256="99045a7c4e3fbc73f01e930ce870cdc573a39910a28d85c54d65d2135f764bfc")
    version("1.6.0", sha256="290da149d4ad79c15787956559aeeefa0a06403be2f08cd324562ef013306797")
    version("1.5.2", sha256="73d16fe9236a9475010dbb01bf751c15bef01eb2e15bf92c8d9be2c0a606329f")
    version("1.5.1", sha256="b1f0232cd6d2aac65385d77cc061ec5035283ea50d0f167e7003eae034effb78")
    version("1.4.1", sha256="82d2c75fcca8bd613273fd4126749df68ccc22fbe4134ba673b4275f9972b78d")
    version("1.4.0", sha256="e08ae556b7c30d14d77147d248d118cf5343a2e8c0847943385c602394bda0fa")
    version("1.3.0", sha256="54b4a62539c23b1a345dd87c1eac65f4f69db4e50336cd81a15a627ce80ce7d9")
    version(
        "1.2.0",
        sha256="b802ffa07c5f34ea9839f23841082133d8af191efe5a526cb7e53ec338ac146b",
        deprecated=True,
    )
    version(
        "1.1.0",
        sha256="c47f7e24c82176b69229a2bcb23a6adcf274dc90ec77a452a36ccae0b12e6e39",
        deprecated=True,
    )

    depends_on("c", type="build")  # todo: disable cmake default?
    depends_on("cxx", type="build")

    variant(
        "portability_strategy",
        description="Portability strategy backend",
        values=("Kokkos", "Cuda", "None"),
        multi=False,
        default="None",
        when="@:1.2.0",
    )
    variant("test", default=False, description="Build tests")
    variant(
        "test_portability_strategy",
        description="Portability strategy used by tests",
        values=("Kokkos", "Cuda", "None"),
        multi=False,
        default="None",
        when="@1.7.0: +test",
    )

    depends_on("cmake@3.12:", type="build")
    depends_on("catch2@3.0.1:", when="+test", type=("build", "test"))
    depends_on("kokkos", when="+test test_portability_strategy=Kokkos", type=("build", "test"))

    def cmake_args(self):
        args = [
            self.define_from_variant("PORTS_OF_CALL_BUILD_TESTING", "test"),
            self.define_from_variant(
                "PORTS_OF_CALL_TEST_PORTABILITY_STRATEGY", "test_portability_strategy"
            ),
        ]
        if self.spec.satisfies("@:1.2.0"):
            args.append(self.define_from_variant("PORTABILITY_STRATEGY", "portability_strategy"))
        if self.spec.satisfies("test_portability_strategy=Kokkos ^kokkos+rocm"):
            args.append(self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc))
            args.append(self.define("CMAKE_C_COMPILER", self.spec["hip"].hipcc))
        if self.spec.satisfies("test_portability_strategy=Kokkos ^kokkos+cuda"):
            args.append(self.define("CMAKE_CXX_COMPILER", self.spec["kokkos"].kokkos_cxx))
        return args
