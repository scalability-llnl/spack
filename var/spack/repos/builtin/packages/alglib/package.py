# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class Alglib(MakefilePackage):
    """ALGLIB is a cross-platform numerical analysis and data processing
    library."""

    homepage = "https://www.alglib.net/"
    url = "https://www.alglib.net/translator/re/alglib-3.11.0.cpp.gpl.tgz"

    version("4.01.0", sha256="95e8ea41b32c92346f49a694759e786c5f3a1087b401a9259ef592c0eea4befb")
    version("4.00.0", sha256="827b5f559713a3e8c7c1452ed1ffd5227adb9622d1a165ceb70c117c8ed3ccb4")
    version("3.20.0", sha256="e7357f0f894313ff1b640ec9cb5e8b63f06d2d3411c2143a374aa0e9740da8a9")
    version("3.11.0", sha256="34e391594aac89fb354bdaf58c42849489cd1199197398ba98bb69961f42bdb0")

    depends_on("cxx", type="build")  # generated

    build_directory = "src"

    def edit(self, spec, prefix):
        # this package has no build system!
        make_file_src = join_path(os.path.dirname(self.module.__file__), "Makefile")
        make_file = join_path(self.stage.source_path, "src", "Makefile")
        copy(make_file_src, make_file)
        filter_file(r"so", dso_suffix, make_file)

    def install(self, spec, prefix):
        name = f"libalglib.{dso_suffix}"
        with working_dir("src"):
            mkdirp(prefix.lib)
            install(name, prefix.lib)
            mkdirp(prefix.include)
            install("*.h", prefix.include)

    @run_after("install")
    def fix_darwin_install(self):
        # The shared libraries are not installed correctly on Darwin:
        if sys.platform == "darwin":
            fix_darwin_install_name(self.spec.prefix.lib)
