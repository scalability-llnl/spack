# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mimalloc(CMakePackage):
    """mimalloc is a compact general purpose allocator with excellent performance."""

    homepage = "https://microsoft.github.io/mimalloc"
    url = "https://github.com/microsoft/mimalloc/archive/v0.0.0.tar.gz"
    git = "https://github.com/microsoft/mimalloc.git"
    maintainers("msimberg")

    license("MIT")

    version("dev-slice", branch="dev-slice")
    version("dev", branch="dev")
    version("master", branch="master")
    version("2.1.7", sha256="0eed39319f139afde8515010ff59baf24de9e47ea316a315398e8027d198202d")
    version("2.1.2", sha256="2b1bff6f717f9725c70bf8d79e4786da13de8a270059e4ba0bdd262ae7be46eb")
    version("2.1.1", sha256="38b9660d0d1b8a732160191609b64057d8ccc3811ab18b7607bc93ca63a6010f")
    version("2.1.0", sha256="86e5e53e38bace59a9eb20d27e7bd7c5f448cb246a887d4f99478fa4809731fc")
    version("2.0.9", sha256="4a29edae32a914a706715e2ac8e7e4109e25353212edeed0888f4e3e15db5850")
    version("2.0.7", sha256="f23aac6c73594e417af50cb38f1efed88ef1dc14a490f0eff07c7f7b079810a4")
    version("2.0.6", sha256="9f05c94cc2b017ed13698834ac2a3567b6339a8bde27640df5a1581d49d05ce5")
    version("1.8.2", sha256="4058d53d6ceb75862f32c30a6ee686c3cbb5e965b2c324b828ca454f7fe064f9")
    version("1.8.1", sha256="7aaa54c3ed1feac90b6187eb93108e808660c6e103b0fa6a7e2fabb58c3147d5")
    version("1.8.0", sha256="4bb69b49821499256e7d9b2a47427c4661f5ad3f1547a21f7bdea7e3bcbc60f8")
    version("1.7.9", sha256="45e05be518363d32b2cdcce1a1fac3580895ea2e4524e1a3c7e71145cb58659f")
    version("1.7.7", sha256="0f6663be1e1764851bf9563fcf7a6b3330e23b933eb4737dd07e3289b87895fe")
    version("1.7.6", sha256="d74f86ada2329016068bc5a243268f1f555edd620b6a7d6ce89295e7d6cf18da")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("cmake@3.0:", type="build")
    conflicts("^cmake@:3.17", when="@2.1.7:")

    libs_values = ("shared", "static", "object")
    variant(
        "libs",
        default=",".join(libs_values),
        values=libs_values,
        multi=True,
        description="Build shared, static, or object libraries",
    )

    mimalloc_options = {
        "secure": (
            False,
            "Use full security mitigations (like guard pages, allocation "
            "randomization, double-free mitigation, and free-list corruption "
            "detection)",
            None,
        ),
        "debug_full": (
            False,
            "Use full internal heap invariant checking in DEBUG mode (expensive)",
            None,
        ),
        "padding": (
            True,
            "Enable padding to detect heap block overflow (used only in DEBUG mode)",
            None,
        ),
        "override": (
            True,
            "Override the standard malloc interface (e.g. define entry points "
            "for malloc() etc)",
            None,
        ),
        "xmalloc": (False, "Enable abort() call on memory allocation failure by default", None),
        "show_errors": (
            False,
            "Show error and warning messages by default (only enabled by default "
            "in DEBUG mode)",
            None,
        ),
        "use_cxx": (
            False,
            "Use the C++ compiler to compile the library (instead of the C compiler)",
            None,
        ),
        "see_asm": (False, "Generate assembly files", None),
        "osx_interpose": (
            True,
            "Use interpose to override standard malloc on macOS",
            "platform=darwin",
        ),
        "osx_zone": (
            True,
            "Use malloc zone to override standard malloc on macOS",
            "platform=darwin",
        ),
        "local_dynamic_tls": (
            False,
            "Use slightly slower, dlopen-compatible TLS mechanism (Unix)",
            None,
        ),
        "build_tests": (False, "Build test executables", None),
        "debug_tsan": (False, "Build with thread sanitizer (needs clang)", "%clang"),
        "debug_ubsan": (
            False,
            "Build with undefined-behavior sanitizer (needs clang++)",
            "%clang build_type=Debug +use_cxx",
        ),
        "skip_collect_on_exit": (False, "Skip collecting memory on program exit", None),
    }

    for k, v in mimalloc_options.items():
        if v[2]:
            variant(k, default=v[0], description=v[1], when=v[2])
        else:
            variant(k, default=v[0], description=v[1])

    def cmake_args(self):
        args = [
            self.define("MI_BUILD_%s" % lib.upper(), lib in self.spec.variants["libs"].value)
            for lib in self.libs_values
        ]
        args += [self.define_from_variant("MI_%s" % k.upper(), k) for k in self.mimalloc_options]

        # Use LTO also for non-Intel compilers please. This can be removed when they
        # bump cmake_minimum_required to VERSION 3.9.
        if "+ipo" in self.spec:
            args.append("-DCMAKE_POLICY_DEFAULT_CMP0069=NEW")
        return args
