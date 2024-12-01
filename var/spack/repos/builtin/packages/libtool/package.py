# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Libtool(AutotoolsPackage, GNUMirrorPackage):
    """libtool -- library building part of autotools."""

    homepage = "https://www.gnu.org/software/libtool/"
    gnu_mirror_path = "libtool/libtool-2.4.6.tar.gz"

    license("LGPL-2.0-or-later AND GPL-2.0-or-later")

    version(
        "develop",
        git="https://git.savannah.gnu.org/git/libtool.git",
        branch="master",
        submodules=True,
    )

    version("2.4.7", sha256="04e96c2404ea70c590c546eba4202a4e12722c640016c12b9b2f1ce3d481e9a8")
    version("2.4.6", sha256="e3bd4d5d3d025a36c21dd6af7ea818a2afcd4dfc1ea5a17b39d7854bcd0c06e3")
    # Version released in 2011
    version(
        "2.4.2",
        sha256="b38de44862a987293cd3d8dfae1c409d514b6c4e794ebc93648febf9afc38918",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("m4@1.4.6:", type="build")

    # the following are places in which libtool depends on findutils
    # https://github.com/autotools-mirror/libtool/blob/v2.4.7/build-aux/ltmain.in#L3296
    # https://github.com/autotools-mirror/libtool/blob/v2.4.6/build-aux/ltmain.in#L3278
    # https://github.com/autotools-mirror/libtool/blob/v2.4.2/libltdl/config/ltmain.m4sh#L3028
    depends_on("findutils", type="run")

    with when("@2.4.2"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("help2man", type="build")

    with when("@2.4.6"):
        depends_on("autoconf@2.62:", type="test")
        depends_on("automake", type="test")

    with when("@develop"):
        depends_on("autoconf", type="build")
        depends_on("automake", type="build")
        depends_on("help2man", type="build")
        depends_on("xz", type="build")
        depends_on("texinfo", type="build")
        # Fix parsing of compiler output when collecting predeps and postdeps
        # https://lists.gnu.org/archive/html/bug-libtool/2016-03/msg00003.html
        patch("flag_space.patch")

    build_directory = "spack-build"

    tags = ["build-tools"]

    executables = ["^g?libtool(ize)?$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"\(GNU libtool\)\s+(\S+)", output)
        return match.group(1) if match else None

    @when("@2.4.2,develop")
    def autoreconf(self, spec, prefix):
        Executable("./bootstrap")()

    @property
    def libs(self):
        return find_libraries(["libltdl"], root=self.prefix, recursive=True, shared=True)

    def _make_executable(self, name):
        return Executable(join_path(self.prefix.bin, name))

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies("%nvhpc@:20.11"):
            filter_file("-fno-builtin", "-Mnobuiltin", "configure")
            filter_file("-fno-builtin", "-Mnobuiltin", "libltdl/configure")

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.append_path("ACLOCAL_PATH", self.prefix.share.aclocal)

    def setup_dependent_package(self, module, dependent_spec):
        # Automake is very likely to be a build dependency, so we add
        # the tools it provides to the dependent module. Some build
        # systems differentiate between BSD libtool (e.g., Darwin) and
        # GNU libtool, so also add 'glibtool' and 'glibtoolize' to the
        # list of executables. See Homebrew:
        # https://github.com/Homebrew/homebrew-core/blob/master/Formula/libtool.rb
        executables = ["libtoolize", "libtool", "glibtoolize", "glibtool"]
        for name in executables:
            setattr(module, name, self._make_executable(name))

    @run_after("install")
    def post_install(self):
        # Some platforms name GNU libtool and GNU libtoolize
        # 'glibtool' and 'glibtoolize', respectively, to differentiate
        # them from BSD libtool and BSD libtoolize. On these BSD
        # platforms, build systems sometimes expect to use the assumed
        # GNU commands glibtool and glibtoolize instead of the BSD
        # variant; this happens frequently, for instance, on Darwin
        symlink(join_path(self.prefix.bin, "libtool"), join_path(self.prefix.bin, "glibtool"))
        symlink(
            join_path(self.prefix.bin, "libtoolize"), join_path(self.prefix.bin, "glibtoolize")
        )

    def setup_build_environment(self, env):
        """Wrapper until spack has a real implementation of setup_test_environment()"""
        if self.run_tests:
            self.setup_test_environment(env)

    def setup_test_environment(self, env):
        """When Fortran is not provided, a few tests need to be skipped"""
        if self.compiler.f77 is None:
            env.set("F77", "no")
        if self.compiler.fc is None:
            env.set("FC", "no")

    @when("@2.4.6")
    def check(self):
        """installcheck of libtool-2.4.6 runs the full testsuite, skip 'make check'"""
        pass
