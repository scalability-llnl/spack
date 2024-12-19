# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pathlib
import shutil
from typing import List

import archspec.cpu

from llnl.util import lang

import spack.compilers.libraries
import spack.config
import spack.package_base
from spack.package import *


class CompilerWrapper(Package):
    """Spack compiler wrapper script.

    Compiler commands go through this compiler wrapper in Spack builds.
    The compiler wrapper is a thin layer around the standard compilers.
    It enables several key pieces of functionality:

    1. It allows Spack to swap compilers into and out of builds easily.
    2. It adds several options to the compile line so that spack
       packages can find their dependencies at build time and run time:
       -I and/or -isystem arguments for dependency /include directories.
       -L                 arguments for dependency /lib directories.
       -Wl,-rpath         arguments for dependency /lib directories.
    """

    homepage = "https://github.com/spack/spack"
    url = f"file:///{pathlib.PurePath(__file__).parent}/cc.sh"

    # FIXME (compiler as nodes): use a different tag, since this is only to exclude
    # this node from auto-generated rules
    tags = ["runtime"]

    license("Apache-2.0 OR MIT")

    version(
        "1.0",
        sha256="92924570efbc0f388bbbeb87188e05537008bc25069529f7b519b4e48d7ddfb6",
        expand=False,
    )

    conflicts("platform=windows")

    def bin_dir(self) -> pathlib.Path:
        # This adds an extra "spack" subdir, so that the script and symlinks don't get
        # their way to the default view /bin directory in environment
        return pathlib.Path(str(self.prefix)) / "spack" / "bin"

    def install(self, spec, prefix):
        cc_script = pathlib.Path(self.stage.source_path) / "cc.sh"
        bin_dir = self.bin_dir()

        # Copy the script
        bin_dir.mkdir(parents=True)
        installed_script = bin_dir / "cc"
        shutil.copy(cc_script, str(installed_script))
        set_executable(installed_script)

        # Create links to use the script under different names
        for name in (
            "ld.lld",
            "ld.gold",
            "ld",
            "ftn",
            "fc",
            "f95",
            "f90",
            "f77",
            "cpp",
            "c99",
            "c89",
            "c++",
        ):
            (bin_dir / name).symlink_to(installed_script)

        for subdir, name in (
            ("aocc", "clang"),
            ("aocc", "clang++"),
            ("aocc", "flang"),
            ("arm", "armclang"),
            ("arm", "armclang++"),
            ("arm", "armflang"),
            ("case-insensitive", "CC"),
            ("cce", "cc"),
            ("cce", "craycc"),
            ("cce", "crayftn"),
            ("cce", "ftn"),
            ("clang", "clang"),
            ("clang", "clang++"),
            ("clang", "flang"),
            ("fj", "fcc"),
            ("fj", "frt"),
            ("gcc", "gcc"),
            ("gcc", "g++"),
            ("gcc", "gfortran"),
            ("intel", "icc"),
            ("intel", "icpc"),
            ("intel", "ifort"),
            ("nag", "nagfor"),
            ("nvhpc", "nvc"),
            ("nvhpc", "nvc++"),
            ("nvhpc", "nvfortran"),
            ("oneapi", "icx"),
            ("oneapi", "icpx"),
            ("oneapi", "ifx"),
            ("rocmcc", "amdclang"),
            ("rocmcc", "amdclang++"),
            ("rocmcc", "amdflang"),
            ("xl", "xlc"),
            ("xl", "xlc++"),
            ("xl", "xlf"),
            ("xl", "xlf90"),
            ("xl_r", "xlc_r"),
            ("xl_r", "xlc++_r"),
            ("xl_r", "xlf_r"),
            ("xl_r", "xlf90_r"),
        ):
            (bin_dir / subdir).mkdir(exist_ok=True)
            (bin_dir / subdir / name).symlink_to(installed_script)

    def setup_dependent_build_environment(self, env, dependent_spec):
        _var_list = []
        if dependent_spec.dependencies(virtuals=("c",)):
            _var_list.append(("c", "cc", "CC", "SPACK_CC"))

        if dependent_spec.dependencies(virtuals=("cxx",)):
            _var_list.append(("cxx", "cxx", "CXX", "SPACK_CXX"))

        if dependent_spec.dependencies(virtuals=("fortran",)):
            _var_list.append(("fortran", "fortran", "F77", "SPACK_F77"))
            _var_list.append(("fortran", "fortran", "FC", "SPACK_FC"))

        # The package is not used as a compiler, so skip this setup
        if not _var_list:
            return

        bin_dir = self.bin_dir()
        implicit_rpaths, env_paths = [], []
        for language, attr_name, wrapper_var_name, spack_var_name in _var_list:
            compiler_pkg = dependent_spec[language].package
            if not hasattr(compiler_pkg, attr_name):
                continue

            compiler = getattr(compiler_pkg, attr_name)
            env.set(spack_var_name, compiler)

            if language not in compiler_pkg.link_paths:
                continue

            wrapper_path = bin_dir / compiler_pkg.link_paths.get(language)

            env.set(wrapper_var_name, str(wrapper_path))
            env.set(f"SPACK_{wrapper_var_name}_RPATH_ARG", compiler_pkg.rpath_arg)

            uarch = dependent_spec.architecture.target
            version_number, _ = archspec.cpu.version_components(
                compiler_pkg.spec.version.dotted_numeric_string
            )
            try:
                isa_arg = uarch.optimization_flags(compiler_pkg.archspec_name(), version_number)
            except (ValueError, archspec.cpu.UnsupportedMicroarchitecture):
                isa_arg = ""

            if isa_arg:
                env.set(f"SPACK_TARGET_ARGS_{attr_name.upper()}", isa_arg)

            # Add spack build environment path with compiler wrappers first in
            # the path. We add the compiler wrapper path, which includes default
            # wrappers (cc, c++, f77, f90), AND a subdirectory containing
            # compiler-specific symlinks.  The latter ensures that builds that
            # are sensitive to the *name* of the compiler see the right name when
            # we're building with the wrappers.
            #
            # Conflicts on case-insensitive systems (like "CC" and "cc") are
            # handled by putting one in the <bin_dir>/case-insensitive
            # directory.  Add that to the path too.
            compiler_specific_dir = (bin_dir / compiler_pkg.link_paths[language]).parent

            for item in [bin_dir, compiler_specific_dir]:
                env_paths.append(item)
                ci = item / "case-insensitive"
                if ci.is_dir():
                    env_paths.append(ci)

            env.set(f"SPACK_{wrapper_var_name}_LINKER_ARG", compiler_pkg.linker_arg)

            # Check if this compiler has implicit rpaths
            implicit_rpaths.extend(_implicit_rpaths(pkg=compiler_pkg))

        if implicit_rpaths:
            # Implicit rpaths are accumulated across all compilers so, whenever they are mixed,
            # the compiler used in ccld mode will account for rpaths from other compilers too.
            implicit_rpaths = lang.dedupe(implicit_rpaths)
            env.set("SPACK_COMPILER_IMPLICIT_RPATHS", ":".join(implicit_rpaths))

        # Check whether we want to force RPATH or RUNPATH
        if spack.config.CONFIG.get("config:shared_linking:type") == "rpath":
            env.set("SPACK_DTAGS_TO_STRIP", self.enable_new_dtags)
            env.set("SPACK_DTAGS_TO_ADD", self.disable_new_dtags)
        else:
            env.set("SPACK_DTAGS_TO_STRIP", self.disable_new_dtags)
            env.set("SPACK_DTAGS_TO_ADD", self.enable_new_dtags)

        for item in env_paths:
            env.prepend_path("SPACK_ENV_PATH", item)

    def setup_dependent_package(self, module, dependent_spec):
        bin_dir = self.bin_dir()

        if dependent_spec.dependencies(virtuals=("c",)):
            compiler_pkg = dependent_spec["c"].package
            setattr(module, "spack_cc", str(bin_dir / compiler_pkg.link_paths["c"]))

        if dependent_spec.dependencies(virtuals=("cxx",)):
            compiler_pkg = dependent_spec["cxx"].package
            setattr(module, "spack_cxx", str(bin_dir / compiler_pkg.link_paths["cxx"]))

        if dependent_spec.dependencies(virtuals=("fortran",)):
            compiler_pkg = dependent_spec["fortran"].package
            setattr(module, "spack_fc", str(bin_dir / compiler_pkg.link_paths["fortran"]))
            setattr(module, "spack_f77", str(bin_dir / compiler_pkg.link_paths["fortran"]))

    @property
    def disable_new_dtags(self) -> str:
        if self.spec.satisfies("platform=darwin"):
            return ""
        return "--disable-new-dtags"

    @property
    def enable_new_dtags(self) -> str:
        if self.spec.satisfies("platform=darwin"):
            return ""
        return "--enable-new-dtags"


def _implicit_rpaths(pkg: spack.package_base.PackageBase) -> List[str]:
    detector = spack.compilers.libraries.CompilerPropertyDetector(pkg.spec)
    paths = detector.implicit_rpaths()
    return paths
