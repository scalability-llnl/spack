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

    variant("benchs", default=False, description="Build benchmarks")
    variant("docs", default=False, description="Build documentation")
    variant("tests", default=False, description="Build tests")
    variant("fortran", default=True, description="Enable Fortran support")
    variant("python", default=True, description="Enable Python support")

    depends_on("cmake@3.16.3:", type=("build"), when="@1.8:")
    depends_on("doxygen@1.8.17:", type=("build"), when="@1.8: +docs")
    depends_on("paraconf@1:", type=("link", "run"), when="@1.6:")
    depends_on("paraconf +fortran", type=("link", "run"), when="+fortran")
    depends_on("paraconf@0.4.14: +shared", type=("link", "run"))
    depends_on("pkgconfig", type=("build"))
    depends_on("python@3.8.2:3.11.9", type=("build", "link", "run"), when="@1.8: +python")
    depends_on("py-pybind11@2.3:2", type=("link"), when="+python")
    depends_on("py-pybind11@2.4.3:", type=("link"), when="@1.8: +python")
    depends_on("spdlog@1.5:", type=("link"), when="@1.5:")

    root_cmakelists_dir = "pdi"

    def patch(self):
        # Run before build so that the standard Spack sbang install hook can fix
        # up the path to the python binary the zpp scripts requires. We dont use
        # filter_shebang("vendor/zpp-1.0.16/bin/zpp.in") because the template is
        # not yet instantiated and PYTHON_EXECUTABLE is not yet large enough to
        # trigger the replacement via filter_shebang.

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
