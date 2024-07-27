# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty
from llnl.util.tty.color import colorize

import spack
import spack.cmd
from spack.cmd.common import arguments
from spack.error import SpackError
from spack.util.environment import EnvironmentModifications

description = "configure CMake project in current working directory using a Spack spec"
section = "developer"
level = "long"

# first assumption, we're in the source directory
source_dir = os.getcwd()
binary_dir = "build"

while source_dir != "/" and not os.path.exists(os.path.join(source_dir, "CMakeLists.txt")):
    # now assume we're in a build folder, try to find source_dir as parent
    binary_dir = "."
    source_dir = os.path.dirname(source_dir)


def setup_parser(subparser):
    subparser.usage = """spack cmake [-h] [-B BINARY_DIR] [-S SOURCE_DIR]
                   [-c|--compiler-only] [-i|--inherit] [-t|--test] [-d|--dry-run]
                   spec [-- CMAKE_OPTIONS]"""
    subparser.add_argument("-B", "--binary_dir", default=binary_dir)
    subparser.add_argument("-S", "--source_dir", default=source_dir)
    subparser.add_argument("-t", "--test", action="store_true", help="Enable testing")
    subparser.add_argument(
        "-d", "--dry-run", action="store_true", help="Only generate command line"
    )
    subparser.add_argument(
        "-c", "--compiler-only", action="store_true", help="Only generate CMake compiler options"
    )
    subparser.add_argument(
        "-i", "--inherit", action="store_true", help="Inherit variants from Spack environment"
    )
    arguments.add_common_arguments(subparser, ["spec"])


def cmake(parser, args, unparsed_args):
    source_dir = os.path.abspath(args.source_dir)
    binary_dir = os.path.abspath(args.binary_dir)

    # check final source_dir location
    if not os.path.exists(os.path.join(source_dir, "CMakeLists.txt")):
        raise SpackError("Couldn't find source directory. Please specify with -S <path>!")

    active_env = spack.environment.active_environment()

    if args.inherit and not active_env:
        raise SpackError("No active environment found to inherit from!")

    specs = spack.cmd.parse_specs(args.spec)

    if len(specs) > 1:
        raise SpackError("spack cmake requires at most one named spec")

    app_spec = specs[0]

    print("Input spec")
    print("--------------------------------")
    print(app_spec.tree())

    if active_env:

        def unwrap(x, zero_msg, ambiguous_msg, zero=tty.die, ambiguous=tty.die):
            if not x:
                zero(zero_msg)
            if len(x) > 1:
                ambiguous(ambiguous_msg)
            return next(iter(x))

        if args.inherit:
            app_spec = unwrap(
                {r for _, r in active_env.concretized_specs() if r.satisfies(app_spec)},
                "No compatible spec in environment",
                "Choice of compatible spec is ambiguous",
            )
            tty.info(f"Reusing environment spec for {app_spec.name}\n")
            print("Concretized")
            print("--------------------------------")
            print(app_spec.tree())
        else:
            roots = {r for _, r in active_env.concretized_specs() if r.satisfies(app_spec.name)}
            compilers = {r.compiler for r in roots}

            if app_spec.compiler:
                if not any(c.satisfies(app_spec.compiler) for c in compilers):
                    tty.warn(
                        "Compilers used in environment not compatible with spec!",
                        f"environment: {' '.join([str(c) for c in compilers])}",
                        f"spec:        {app_spec.compiler}\n",
                    )
            else:
                app_spec.compiler = unwrap(
                    compilers,
                    "No compatible environment compiler available",
                    "Choice of environment compiler is ambiguous",
                )

            app_spec.concretize()
            print("Concretized")
            print("--------------------------------")
            print(app_spec.tree())

            for dep in app_spec.dependencies():
                if not any(dep.name in r for r in roots):
                    tty.warn(
                        f"Missing dependency {dep.name} in environment!\n  {dep.short_spec}\n"
                    )
                else:
                    selected = unwrap(
                        {r[dep.name] for r in roots if dep.name in r},
                        f"Missing dependency {dep.name} in environment!\n  {dep.short_spec}\n",
                        f"Dependency {dep.name} is ambiguous in environment!\n",
                        zero=tty.warn,
                        ambiguous=tty.warn,
                    )
                    if not selected.satisfies(dep):
                        tty.warn(
                            f"{dep.name} in environment not compatible with provided spec!",
                            f"environment: {selected.cshort_spec}",
                            f"spec:        {dep.cshort_spec}\n",
                        )
    else:
        app_spec.concretize()
        print("Concretized")
        print("--------------------------------")
        print(app_spec.tree())

    app = app_spec.package
    app.run_tests = args.test

    if app_spec.satisfies("^hip"):
        # Needed, so hipcc is set
        app_spec["hip"].package.setup_dependent_package(None, None)

    # TODO add Fortran, CUDA, HIP compilers
    compiler = spack.compilers.compiler_for_spec(app_spec.compiler, app_spec.architecture)
    compiler_args = [f"-DCMAKE_CXX_COMPILER={compiler.cxx}", f"-DCMAKE_C_COMPILER={compiler.cc}"]

    if app_spec.satisfies("^kokkos"):
        # Needed so kokkos_cxx is set (e.g. to nvcc_wrapper) and can be used in cmake_args()
        app_spec["kokkos"].package.module.spack_cxx = compiler.cxx
        if app_spec.satisfies("^kokkos-nvcc-wrapper"):
            env = EnvironmentModifications()
            app_spec["kokkos-nvcc-wrapper"].package.setup_dependent_build_environment(
                env, app_spec
            )
            app_spec["kokkos-nvcc-wrapper"].package.setup_dependent_package(None, None)
            env.apply_modifications()
        app_spec["kokkos"].package.setup_dependent_package(None, None)

    dir_args = ["-B", binary_dir, "-S", source_dir]

    accepted_std_args = (
        "-G",
        "Unix Makefiles",
        "Ninja",
        "CMAKE_BUILD_TYPE",
        "CMAKE_INTERPROCEDURAL_OPTIMIZATION",
    )
    std_args = (
        []
        if args.compiler_only
        else [x for x in app.builder.std_cmake_args if any(n in x for n in accepted_std_args)]
    )

    app_args = app.cmake_args()
    if args.compiler_only:
        app_args = [
            x for x in app_args if any(n in x for n in ("CMAKE_CXX_COMPILER", "CMAKE_C_COMPILER"))
        ]

    cmake_args = std_args + compiler_args + app_args + unparsed_args + dir_args

    cmake = os.path.join(app_spec["cmake"].prefix, "bin", "cmake")
    cmd = " ".join([cmake] + cmake_args)
    tty.msg(f"CMake Command: {colorize(f'@c{{{cmd}}}')}")
    if not args.dry_run:
        os.execl(cmake, cmake, *cmake_args)
