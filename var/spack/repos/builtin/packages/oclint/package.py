# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Oclint(Package):
    """OClint: a static analysis tool for C, C++, and Objective-C code

    OCLint is a static code analysis tool for improving quality and
    reducing defects by inspecting C, C++ and Objective-C code and
    looking for potential problems"""

    homepage = "https://oclint.org/"
    url = "https://github.com/oclint/oclint/archive/v0.13.tar.gz"

    version("0.13", sha256="a0fd188673863e6357d6585b9bb9c3affe737df134b9383a1a5ed021d09ed848")

    depends_on("cxx", type="build")  # generated

    depends_on("python", type=("build"))
    depends_on("git", type=("build"))
    depends_on("subversion", type=("build"))
    depends_on("cmake", type=("build"))
    depends_on("ninja", type=("build"))
    depends_on("llvm@5.0.0:")

    # Needed to fix a bug in oclint-scripts/bundle script, which
    # attempts to install c++ headers in the wrong location
    # contributed upstream as
    # https://github.com/oclint/oclint/pull/492
    patch("bundle.patch", level=0)

    def install(self, spec, prefix):
        # Build from source via directions from
        # https://docs.oclint.org/en/stable/intro/build.html,
        cd("oclint-scripts")

        # ...but instead of using oclint-scripts/make, execute the
        # commands in oclint-scripts/makeWithSystemLLVM so that
        # oclint links to spack-installed LLVM
        build_script = Executable(join_path(".", "build"))
        bundle_script = Executable(join_path(".", "bundle"))

        # Add the '-no-analytics' argument to the build script because
        # 1) it doesn't detect properly a spack install of OpenSSL,
        #    and throws an error due to missing OpenSSL headers
        # 2) the bespoke build system is a pain to patch as it is
        # 3) many sites don't allow software that communicates analytics data
        build_script(
            "-release",
            "-clean",
            "-llvm-root={0}".format(spec["llvm"].prefix),
            "-use-system-compiler",
            "-no-analytics",
            "all",
        )
        bundle_script("-release", "-llvm-root={0}".format(spec["llvm"].prefix))

        # Copy install tree into the correct locations using the
        # directory layout described in
        cd(join_path("..", "build"))
        install_tree(join_path("oclint-release", "include"), prefix.include)
        install_tree(join_path("oclint-release", "lib"), prefix.lib)
        install_tree(join_path("oclint-release", "bin"), prefix.bin)
