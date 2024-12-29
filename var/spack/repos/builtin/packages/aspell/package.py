# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


# See also: AspellDictPackage
class Aspell(AutotoolsPackage, GNUMirrorPackage):
    """GNU Aspell is a Free and Open Source spell checker designed to
    eventually replace Ispell."""

    homepage = "http://aspell.net/"
    gnu_mirror_path = "aspell/aspell-0.60.6.1.tar.gz"

    extendable = True  # support activating dictionaries

    license("LGPL-2.1-or-later")

    version("0.60.8.1", sha256="d6da12b34d42d457fa604e435ad484a74b2effcd120ff40acd6bb3fb2887d21b")
    version("0.60.8", sha256="f9b77e515334a751b2e60daab5db23499e26c9209f5e7b7443b05235ad0226f2")
    version("0.60.6.1", sha256="f52583a83a63633701c5f71db3dc40aab87b7f76b29723aeb27941eff42df6e1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    patch("fix_cpp.patch")
    patch("issue-519.patch", when="@:0.60.6.1")

    # workaround due to https://github.com/GNUAspell/aspell/issues/591
    @run_after("configure", when="@0.60.8:")
    def make_missing_files(self):
        make("gen/dirs.h")
        make("gen/static_filters.src.cpp")

    def setup_run_environment(self, env):
        env.set("ASPELL_CONF", f"prefix {self.prefix}")
