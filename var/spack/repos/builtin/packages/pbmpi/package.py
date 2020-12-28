# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pbmpi(MakefilePackage):
    """A Bayesian software for phylogenetic reconstruction using mixture models
    """

    homepage = "http://megasun.bch.umontreal.ca/People/lartillot/www/index.htm"
    git      = "https://github.com/bayesiancook/pbmpi.git"

    version('partition', branch='partition')

    depends_on('mpi')
    depends_on('libfabric')

    build_directory = 'sources'

    @run_before('build')
    def make_data_dir(self):
        mkdirp(self.stage.source_path, 'data')

    def install(self, spec, prefix):
        install_tree('data', prefix.bin)
        install_tree('sources', prefix.sources)
