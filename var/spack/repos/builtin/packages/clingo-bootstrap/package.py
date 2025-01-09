# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import glob
import os

import spack.paths
import spack.user_environment
from spack.package import *
from spack.pkg.builtin.clingo import Clingo
from spack.util.environment import EnvironmentModifications


class ClingoBootstrap(Clingo):
    """Clingo with some options used for bootstrapping"""

    maintainers("alalazo")

    variant("build_type", default="Release", values=("Release",), description="CMake build type")

    variant(
        "static_libstdcpp",
        default=False,
        when="platform=linux",
        description="Require a static version of libstdc++",
    )

    variant(
        "optimized",
        default=False,
        description="Enable a series of Spack-specific optimizations (PGO, LTO, mimalloc)",
    )

    # Enable LTO
    conflicts("~ipo", when="+optimized")

    with when("+optimized platform=linux"):
        # Statically linked. Don't use ~override so we don't duplicate malloc/free, they
        # get resolved to Python's libc's malloc in our case anyway.
        depends_on("mimalloc +ipo libs=static ~override", type="build")
        conflicts("~static_libstdcpp", msg="Custom allocator requires static libstdc++")
        # Override new/delete with mimalloc.
        patch("mimalloc.patch", when="@5.5.0:")
        patch("mimalloc-pre-5.5.0.patch", when="@:5.4")
        # ensure we hide libstdc++ with custom operator new/delete symbols
        patch("version-script.patch", when="@spack,5.5:5.6")
        patch("version-script-5.4.patch", when="@5.2:5.4")

    # CMake at version 3.16.0 or higher has the possibility to force the
    # Python interpreter, which is crucial to build against external Python
    # in environment where more than one interpreter is in the same prefix
    depends_on("cmake@3.16.0:", type="build")

    # On Linux we bootstrap with GCC or clang
    requires(
        "%gcc",
        "%clang",
        when="platform=linux",
        msg="GCC or clang are required to bootstrap clingo on Linux",
    )
    conflicts("%gcc@:5", msg="C++14 support is required to bootstrap clingo")

    # On Darwin we bootstrap with Apple Clang
    requires(
        "%apple-clang",
        when="platform=darwin",
        msg="Apple-clang is required to bootstrap clingo on MacOS",
    )

    # Clingo needs the Python module to be usable by Spack
    conflicts("~python", msg="Python support is required to bootstrap Spack")

    @property
    def cmake_py_shared(self):
        return self.define("CLINGO_BUILD_PY_SHARED", "OFF")

    def cmake_args(self):
        return [*super().cmake_args(), self.define("CLINGO_BUILD_APPS", False)]

    @run_before("cmake", when="+optimized")
    def pgo_train(self):
        if self.spec.satisfies("%clang"):
            llvm_profdata = which("llvm-profdata", required=True)
        elif self.spec.satisfies("%apple-clang"):
            llvm_profdata = Executable(
                Executable("xcrun")("-find", "llvm-profdata", output=str).strip()
            )

        # First configure with PGO flags, and do build apps.
        reports = os.path.abspath("reports")
        sources = os.path.abspath(self.root_cmakelists_dir)
        cmake_options = self.std_cmake_args + self.cmake_args() + [sources]

        # Set PGO training flags.
        generate_mods = EnvironmentModifications()
        generate_mods.append_flags("CFLAGS", "-fprofile-generate={}".format(reports))
        generate_mods.append_flags("CXXFLAGS", "-fprofile-generate={}".format(reports))
        generate_mods.append_flags("LDFLAGS", "-fprofile-generate={} --verbose".format(reports))

        with working_dir(self.build_directory, create=True):
            cmake(*cmake_options, sources, extra_env=generate_mods)
            make()
            make("install")

        # Clean the reports dir.
        rmtree(reports, ignore_errors=True)

        # Run spack solve --fresh hdf5 with instrumented clingo.
        python_runtime_env = EnvironmentModifications()
        python_runtime_env.extend(
            spack.user_environment.environment_modifications_for_specs(self.spec)
        )
        python_runtime_env.unset("SPACK_ENV")
        python_runtime_env.unset("SPACK_PYTHON")
        python(spack.paths.spack_script, "solve", "--fresh", "hdf5", extra_env=python_runtime_env)

        # Clean the build dir.
        rmtree(self.build_directory, ignore_errors=True)

        if self.spec.satisfies("%clang") or self.spec.satisfies("apple-clang"):
            # merge reports
            use_report = join_path(reports, "merged.prof")
            raw_files = glob.glob(join_path(reports, "*.profraw"))
            llvm_profdata("merge", "--output={}".format(use_report), *raw_files)
            use_flag = "-fprofile-instr-use={}".format(use_report)
        else:
            use_flag = "-fprofile-use={}".format(reports)

        # Set PGO use flags for next cmake phase.
        use_mods = EnvironmentModifications()
        use_mods.append_flags("CFLAGS", use_flag)
        use_mods.append_flags("CXXFLAGS", use_flag)
        use_mods.append_flags("LDFLAGS", use_flag)
        cmake.add_default_envmod(use_mods)

    def setup_build_environment(self, env):
        if (
            self.spec.satisfies("%gcc") or self.spec.satisfies("%clang")
        ) and "+static_libstdcpp" in self.spec:
            env.append_flags("LDFLAGS", "-static-libstdc++ -static-libgcc -Wl,--exclude-libs,ALL")
