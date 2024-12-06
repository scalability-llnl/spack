# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cinch(Package):
    """
    Cinch is a set of utilities and configuration options designed to make
    cmake builds easy to use and manage.
    """

    homepage = "https://github.com/laristra/cinch"
    url = "https://github.com/laristra/cinch/archive/1.0.zip"
    git = "https://github.com/laristra/cinch.git"

    license("Unlicense")

    version("master", branch="master", submodules=False)
    version("1.0", sha256="98b73473829b478191481621d84c3d63c662da6e951321f858a032eae3ca07b7")

    def install(self, spec, prefix):
        # (CMake) Header Only library so just copy
        install_tree(self.stage.source_path, prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path("CMAKE_PREFIX_PATH", self.prefix)
        env.set("CINCH_SOURCE_DIR", self.prefix)
