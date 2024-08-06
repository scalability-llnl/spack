# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cpptrace(CMakePackage):
    """Simple, portable, and self-contained stacktrace library for C++11 and newer"""

    homepage = "https://github.com/jeremy-rifkin/cpptrace"
    url = "https://github.com/jeremy-rifkin/cpptrace/archive/refs/tags/v0.6.3.tar.gz"

    maintainers("pranav-sivaraman")

    license("MIT", checked_by="pranav-sivaraman")

    version("0.6.3", sha256="665bf76645ec7b9e6d785a934616f0138862c36cdb58b0d1c9dd18dd4c57395a")

    variant("shared", default=True, description="Build shared libs")
    variant("pic", default=True, description="Build with position independent code")

    with when("platform=linux"):
        variant(
            "unwinding-backend",
            multi=False,
            default="unwind",
            values=("unwind", "execinfo", "libunwind", "nothing"),
        )
        variant(
            "symbols-backend",
            multi=False,
            default="libdwarf",
            values=("libdwarf", "libbacktrace", "addr2line", "libdl", "nothing"),
        )
        variant("demangling-backend", multi=False, default="cxxabi", values=("cxxabi", "nothing"))

    with when("platform=darwin"):
        variant(
            "unwinding-backend",
            multi=False,
            default="unwind",
            values=("unwind", "execinfo", "libunwind", "nothing"),
        )
        variant(
            "symbols-backend",
            multi=False,
            default="libdwarf",
            values=("libdwarf", "libbacktrace", "addr2line", "libdl", "nothing"),
        )
        variant("demangling-backend", multi=False, default="cxxabi", values=("cxxabi", "nothing"))

    with when("platform=windows"):
        variant(
            "unwinding-backend",
            multi=False,
            default="dbghelp",
            values=("winapi", "dbghelp", "libunwind", "nothing"),
        )
        variant("symbols-backend", multi=False, default="dbghelp", values=("dbghelp", "nothing"))
        variant("demangling-backend", multi=False, default="winapi", values=("winapi", "nothing"))

    depends_on("libunwind", when="unwinding-backend=libunwind")
    depends_on("libdwarf", when="symbols-backend=libdwarf")

    depends_on("googletest", type="test")

    conflicts("+shared ~pic")

    def cmake_args(self):
        spec = self.spec
        define = self.define
        from_variant = self.from_variant

        args = [
            from_variant("BUILD_SHARED_LIBS", "shared"),
            from_variant("CPPTRACE_POSITION_INDEPENDENT_CODE", "pic"),
            define("CPPTRACE_BUILD_TESTING", self.run_tests),
            define("CPPTRACE_USE_EXTERNAL_LIBDWARF", True),
            define("CPPTRACE_USE_EXTERNAL_GTEST", True),
            define(
                f"CPPTRACE_UNWIND_WITH_{spec.variants['unwinding-backend'].value.upper()}", True
            ),
            define(
                f"CPPTRACE_GET_SYMBOLS_WITH_{spec.variants['symbols-backend'].value.upper()}", True
            ),
            define(
                f"CPPTRACE_DEMANGLE_WITH_{spec.variants['demangling-backend'].value.upper()}", True
            ),
        ]

        return args
