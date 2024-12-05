# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ThePlatinumSearcher(Package):
    """Fast parallel recursive grep alternative"""

    homepage = "https://github.com/monochromegane/the_platinum_searcher"
    go = "github.com/monochromegane/the_platinum_searcher/..."

    version("head")

    extends("go", type="build")

    def install(self, spec, prefix):
        env["GOPATH"] = self.stage.source_path + ":" + env["GOPATH"]
        go("install", self.package, env=env)
        install_tree("bin", prefix.bin)
