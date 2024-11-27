# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MiniappAscent(Package):
    """Pantheon/E4S/Ascent in-situ miniapp example workflow"""

    homepage = "https://github.com/cinemascienceworkflows/2021-04_Miniapp-Ascent"
    git = "https://github.com/cinemascienceworkflows/2021-04_Miniapp-Ascent.git"
    url = "https://github.com/cinemascienceworkflows/2021-04_Miniapp-Ascent/archive/refs/heads/master.zip"

    license("BSD-3-Clause")

    version("master", branch="master")

    depends_on("ascent", type=("run"))

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)
