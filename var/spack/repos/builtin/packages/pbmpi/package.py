# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pbmpi(MakefilePackage):
    """A Bayesian software for phylogenetic reconstruction using mixture models"""

    homepage = "https://github.com/bayesiancook/pbmpi"
    url = "https://github.com/bayesiancook/pbmpi/archive/refs/tags/v1.8c.tar.gz"
    git = "https://github.com/bayesiancook/pbmpi.git"

    maintainers("snehring")

    license("GPL-2.0-only")

    version("1.9", sha256="567d8db995f23b2b0109c1e6088a7e5621e38fec91d6b2f27abd886b90ea31ce")
    version("1.8c", sha256="2a80ec4a98d92ace61c67ff9ba78249d45d03094b364959d490b1ad05797a279")
    version("partition", branch="partition")

    depends_on("cxx", type="build")  # generated

    depends_on("mpi")
    depends_on("libfabric")

    build_directory = "sources"

    @run_before("build")
    def make_data_dir(self):
        mkdirp(self.stage.source_path, "data")

    def install(self, spec, prefix):
        install_tree("data", prefix.bin)
        install_tree("sources", prefix.sources)
