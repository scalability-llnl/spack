# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dialign(MakefilePackage):
    """DIALIGN is a software program for multiple sequence alignment developed
    by Burkhard Morgenstern et al.."""

    homepage = "https://bibiserv.cebitec.uni-bielefeld.de/dialign"
    url = "https://bibiserv.cebitec.uni-bielefeld.de/applications/dialign/resources/downloads/dialign-2.2.1-src.tar.gz"

    license("LGPL-2.1-or-later")

    version("2.2.1", sha256="046361bb4ca6e4ab2ac5e634cfcd673f964a887006c09c1b8bd3310fac86f519")

    depends_on("c", type="build")  # generated

    build_directory = "src"

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(join_path("src", "dialign2-2"), prefix.bin)

        mkdirp(prefix.share)
        install_tree("dialign2_dir", prefix.share)

    def setup_run_environment(self, env):
        env.set("DIALIGN2_DIR", self.prefix.share)
