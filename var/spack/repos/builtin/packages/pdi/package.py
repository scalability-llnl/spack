# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.hooks.sbang import sbang_shebang_line
from spack.package import *


class Pdi(CMakePackage):
    """PDI is a library that aims to decouple high-performance simulation codes
    from Input/Output concerns. It offers a declarative application programming
    interface that enables codes to expose the buffers in which they store data
    and to notify PDI of significant steps of the simulation. It supports a
    plugin system to make existing libraries such as HDF5, SIONlib or FTI
    available to codes, potentially mixed in a single execution."""

    homepage = "https://pdi.dev"
    git = "https://github.com/pdidev/pdi.git"

    license("BSD-3-Clause")

    maintainers("jbigot")

    version("develop", branch="main", no_cache=True)
    version("1.8.1", commit="105161d5c93431d674c73ef365dce3eb724b4fcb")
    version("1.8.0", commit="edce72fc198475bab1541cc0b77a30ad02da91c5")
    version("1.7.1", commit="7eadb5314eae65fa08010bb0d35a4dcace0ebb48")
    version("1.6.0", commit="92da1ee7fc77dce6614de49ec10d991b14e7fd02")
    version("1.5.5", commit="43bd8fdae3bd12a950ff68b09d22cd74923f4eb1")
    version("1.4.3", commit="0e92542d1df70918712cb5ee378bd6ad1199ba2d")
    version("1.3.1", commit="6a075a7af3383d1d5a6278017760b6d3dc746517")
    version("1.2.2", commit="4f7076d6e45ba3feead63a7d710695def52b8380")
    version("1.1.0", commit="5cd945d28d600d54949f610e4c152a59171b2f39")

    variant("benchs", default=False, description="Build benchmarks")
    variant("docs", default=False, description="Build documentation")
    variant("tests", default=False, description="Build tests")
    variant("fortran", default=True, description="Enable Fortran support")
    variant("python", default=True, description="Enable Python support")

    depends_on("benchmark@1.5:", type=("link"), when="@1.5:1.7 +benchs")
    depends_on("cmake@3.5:", type=("build"))
    depends_on("cmake@3.10:", type=("build"), when="+docs")
    depends_on("cmake@3.10:", type=("build"), when="+tests")
    depends_on("cmake@3.10:", type=("build"), when="@1.5:")
    depends_on("cmake@3.16.3:", type=("build"), when="@1.8:")
    depends_on("doxygen@1.8.12:", type=("build"), when="+docs")
    depends_on("doxygen@1.8.13:", type=("build"), when="@1.4.3: +docs")
    depends_on("doxygen@1.8.17:", type=("build"), when="@1.8: +docs")
    depends_on("fmt@6.1.2:", type=("link"), when="@1.5")
    depends_on("googletest@1.8: +gmock", type=("link"), when="@:1.7 +tests")
    depends_on("paraconf@1:", type=("link", "run"), when="@1.6:")
    depends_on("paraconf@0.4.16:", type=("link", "run"), when="@1.5:")
    depends_on("paraconf +fortran", type=("link", "run"), when="+fortran")
    depends_on("paraconf@0.4.14: +shared", type=("link", "run"))
    depends_on("pkgconfig", type=("build"))
    depends_on("python@3.6.5:", type=("build", "link", "run"), when="+python")
    depends_on("python@3.8.2:3.11.9", type=("build", "link", "run"), when="@1.8: +python")
    depends_on("py-pybind11@2.3:2", type=("link"), when="+python")
    depends_on("py-pybind11@:2.11", type=("link"), when="@:1.6 +python")
    depends_on("py-pybind11@2.4.3:", type=("link"), when="@1.8: +python")
    depends_on("spdlog@1.3.1:1", type=("link", "run"))
    depends_on("spdlog@1.5:", type=("link"), when="@1.5:")
    depends_on("zpp@1.0.8:", type=("build"), when="@:1.7 +fortran")
    depends_on("zpp@1.0.15:", type=("build"), when="@1.5:1.7 +fortran")

    root_cmakelists_dir = "pdi"

    def patch(self):
        # Run before build so that the standard Spack sbang install hook can fix
        # up the path to the python binary the zpp scripts requires. We dont use
        # filter_shebang("vendor/zpp-1.0.16/bin/zpp.in") because the template is
        # not yet instantiated and PYTHON_EXECUTABLE is not yet large enough to
        # trigger the replacement via filter_shebang.

        if self.spec.satisfies("@1.8"):
            filter_file(
                r"#!@PYTHON_EXECUTABLE@ -B",
                sbang_shebang_line() + "\n#!@PYTHON_EXECUTABLE@ -B",
                "vendor/zpp-1.0.16/bin/zpp.in",
            )

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_BENCHMARKING", "benchs"),
            self.define_from_variant("BUILD_DOCUMENTATION", "docs"),
            self.define_from_variant("BUILD_FORTRAN", "fortran"),
            self.define_from_variant("BUILD_PYTHON", "python"),
            self.define_from_variant("BUILD_TESTING", "tests"),
        ]
        return args
