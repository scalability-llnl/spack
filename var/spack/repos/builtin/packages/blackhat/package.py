# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Blackhat(AutotoolsPackage):
    """Blackhat MC generator"""

    homepage = "https://blackhat.hepforge.org"
    git = "https://github.com/cms-externals/blackhat.git"

    version("0.9.9", branch="cms/v0.9.9")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("qd")
    depends_on("python")
    extends("python")

    def patch(self):
        filter_file(
            "else return Cached_OLHA_user_normal",
            "else return new Cached_OLHA_user_normal",
            "src/cached_OLHA.cpp",
        )

    def configure_args(self):
        return ["--with-QDpath=" + self.spec["qd"].prefix, "--enable-pythoninterface=no"]

    def setup_build_environment(self, env):
        env.append_flags("CXXFLAGS", "-Wno-deprecated")
