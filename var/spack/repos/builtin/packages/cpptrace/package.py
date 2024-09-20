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

    version("0.7.1", sha256="63df54339feb0c68542232229777df057e1848fc8294528613971bbf42889e83")
    version("0.7.0", sha256="b5c1fbd162f32b8995d9b1fefb1b57fac8b1a0e790f897b81cdafe3625d12001")
    version("0.6.3", sha256="665bf76645ec7b9e6d785a934616f0138862c36cdb58b0d1c9dd18dd4c57395a")

    variant("shared", default=True, description="Build shared libs")
    variant("pic", default=True, description="Build with position independent code")

    patch(
        "https://github.com/jeremy-rifkin/cpptrace/commit/f671819510fffa3f953c2437fb7114068c8765d0.patch?full_index=1",
        sha256="7610b1e52c422023fa84899d7568958e509f5c14ddedced148f495502c6828b7",
        when="@:0.7.0",
    )

    with when("platform=linux"):
        variant(
            "unwinding-backend",
            multi=False,
            default="unwind",
            values=("unwind", "execinfo", "libunwind", "nothing"),
            description="Library backend for unwinding",
        )
        variant(
            "symbols-backend",
            multi=False,
            default="libdwarf",
            values=("libdwarf", "libbacktrace", "addr2line", "libdl", "nothing"),
            description="Library backend for symbols",
        )
        variant(
            "demangling-backend",
            multi=False,
            default="cxxabi",
            values=("cxxabi", "nothing"),
            description="Library backend for demangling",
        )

    with when("platform=darwin"):
        variant(
            "unwinding-backend",
            multi=False,
            default="execinfo",
            values=("unwind", "execinfo", "libunwind", "nothing"),
            description="Library backend for unwinding",
        )

        variant(
            "symbols-backend",
            multi=False,
            default="libdwarf",
            values=("libdwarf", "libbacktrace", "addr2line", "libdl", "nothing"),
            description="Library backend for symbols",
        )
        variant(
            "demangling-backend",
            multi=False,
            default="cxxabi",
            values=("cxxabi", "nothing"),
            description="Library backend for demangling",
        )

    with when("platform=windows"):
        variant(
            "unwinding-backend",
            multi=False,
            default="dbghelp",
            values=("winapi", "dbghelp", "libunwind", "nothing"),
            description="Library backend for unwinding",
        )
        variant(
            "symbols-backend",
            multi=False,
            default="dbghelp",
            values=("dbghelp", "nothing"),
            description="Library backend for symbols",
        )
        variant(
            "demangling-backend",
            multi=False,
            default="winapi",
            values=("winapi", "nothing"),
            description="Library backend for demangling",
        )

    conflicts("+shared ~pic")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.14:", type="build")

    depends_on("unwind", when="unwinding-backend=libunwind")
    depends_on("libdwarf", when="symbols-backend=libdwarf")

    depends_on("googletest", type="test")

    def cmake_args(self):
        spec = self.spec
        define = self.define
        from_variant = self.define_from_variant

        args = [
            from_variant("BUILD_SHARED_LIBS", "shared"),
            from_variant("CPPTRACE_POSITION_INDEPENDENT_CODE", "pic"),
            define("CPPTRACE_BUILD_TESTING", self.run_tests),
            define("CPPTRACE_USE_EXTERNAL_GTEST", self.run_tests),
            define("CPPTRACE_USE_EXTERNAL_LIBDWARF", True),
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
