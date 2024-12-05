# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CbtfLanl(CMakePackage):
    """CBTF LANL project contains a memory tool and data center type system
    command monitoring tool."""

    homepage = "https://sourceforge.net/p/cbtf/wiki/Home/"
    git = "https://github.com/OpenSpeedShop/cbtf-lanl.git"

    maintainers("jgalarowicz")

    version("develop", branch="master")
    version("1.9.4.1", branch="1.9.4.1")
    version("1.9.4", branch="1.9.4")
    version("1.9.3", branch="1.9.3")

    depends_on("cxx", type="build")  # generated

    variant(
        "build_type",
        default="RelWithDebInfo",
        description="The build type to build",
        values=("Debug", "Release", "RelWithDebInfo"),
    )

    variant(
        "runtime", default=False, description="build only the runtime libraries and collectors."
    )

    depends_on("cmake@3.0.2:", type="build")

    # For MRNet
    depends_on("mrnet@5.0.1-3:+lwthreads", when="@develop")
    depends_on("mrnet@5.0.1-3+lwthreads", when="@1.9.3:9999")

    # For Xerces-C
    depends_on("xerces-c")

    # For CBTF
    depends_on("cbtf@develop", when="@develop")
    depends_on("cbtf@1.9.3:9999", when="@1.9.3:9999")

    # For CBTF with runtime
    depends_on("cbtf@develop+runtime", when="@develop+runtime")
    depends_on("cbtf@1.9.3:9999+runtime", when="@1.9.3:9999+runtime")

    # For CBTF-KRELL
    depends_on("cbtf-krell@develop", when="@develop")
    depends_on("cbtf-krell@1.9.3:9999", when="@1.9.3:9999")

    depends_on("cbtf-krell@develop+runtime", when="@develop+runtime")
    depends_on("cbtf-krell@1.9.3:9999+runtime", when="@1.9.3:9999+runtime")

    parallel = False

    build_directory = "build_cbtf_lanl"

    def cmake_args(self):
        spec = self.spec
        compile_flags = "-O2 -g -Wall"

        cmake_args = [
            "-DCMAKE_CXX_FLAGS=%s" % compile_flags,
            "-DCMAKE_C_FLAGS=%s" % compile_flags,
            "-DCBTF_DIR=%s" % spec["cbtf"].prefix,
            "-DCBTF_KRELL_DIR=%s" % spec["cbtf-krell"].prefix,
            "-DMRNET_DIR=%s" % spec["mrnet"].prefix,
            "-DXERCESC_DIR=%s" % spec["xerces-c"].prefix,
            "-DCMAKE_MODULE_PATH=%s" % join_path(prefix.share, "KrellInstitute", "cmake"),
        ]

        return cmake_args
