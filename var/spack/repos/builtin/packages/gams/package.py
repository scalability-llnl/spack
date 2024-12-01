# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Gams(Package):
    """The General Algebraic Modeling System is a high-level modeling system
    for mathematical optimization. GAMS is designed for modeling and solving
    linear, nonlinear, and mixed-integer optimization problems."""

    homepage = "https://www.gams.com/"
    manual_download = True

    version("27.2", md5="4f3f3484a4389661e0522a4cfe0289fd", expand=False)

    def url_for_version(self, version):
        return "file://{0}/linux_x64_64_sfx.exe".format(os.getcwd())

    def setup_run_environment(self, env):
        env.prepend_path(
            "PATH", join_path(self.prefix, "gams{0}_linux_x64_64_sfx".format(self.version))
        )

    def install(self, spec, prefix):
        os.chmod(join_path(self.stage.source_path, "linux_x64_64_sfx.exe"), 0o755)
        os.system("./linux_x64_64_sfx.exe")
        install_tree(
            join_path(self.stage.source_path, "gams{0}_linux_x64_64_sfx".format(self.version)),
            join_path(self.prefix, "gams{0}_linux_x64_64_sfx".format(self.version)),
        )
        install(
            "{0}/gamslice.txt".format(os.getcwd()),
            join_path(
                self.prefix, "gams{0}_linux_x64_64_sfx".format(self.version), "gamslice.txt"
            ),
        )
