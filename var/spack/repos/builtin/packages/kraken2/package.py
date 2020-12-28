# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os

from spack.package import *


class Kraken2(Package):
    """Kraken2 is a system for assigning taxonomic labels to short DNA
       sequences, usually obtained through metagenomic studies."""

    homepage = "https://ccb.jhu.edu/software/kraken2/"
    url      = "https://github.com/DerrickWood/kraken2/archive/v2.0.8-beta.tar.gz"

    maintainers = ['rberg2']

    version('2.0.8-beta', sha256='f2a91fc57a40b3e87df8ac2ea7c0ff1060cc9295c95de417ee53249ee3f7ad8e')
    version('2.0.7-beta', sha256='baa160f5aef73327e1a79e6d1c54b64b2fcdaee0be31b456f7bc411d1897a744')
    version('2.0.6-beta', sha256='d77db6251179c4d7e16bc9b5e5e9043d25acf81f3e32ad6eadfba829a31e1d09')

    depends_on('perl', type=('build', 'run'))
    depends_on('rsync', type=('run'))
    depends_on('wget', type=('run'))

    def install(self, spec, prefix):
        installer = Executable('./install_kraken2.sh')
        installer(self.stage.source_path)
        mkdirp(prefix.bin)
        files = glob.iglob('*')
        for file in files:
            if os.path.isfile(file):
                install(file, prefix.bin)
