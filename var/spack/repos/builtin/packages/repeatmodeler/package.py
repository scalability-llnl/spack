# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Repeatmodeler(Package):
    """RepeatModeler is a de-novo repeat family identification and modeling
       package."""

    homepage = "http://www.repeatmasker.org/RepeatModeler/"
    url      = "http://www.repeatmasker.org/RepeatModeler/RepeatModeler-open-1.0.11.tar.gz"

    version('1.0.11', sha256='7ff0d588b40f9ad5ce78876f3ab8d2332a20f5128f6357413f741bb7fa172193')

    depends_on('perl', type=('build', 'run'))
    depends_on('perl-json', type=('build', 'run'))
    depends_on('perl-uri', type=('build', 'run'))
    depends_on('perl-libwww-perl', type=('build', 'run'))

    depends_on('repeatmasker', type='run')
    depends_on('recon+repeatmasker', type='run')
    depends_on('repeatscout', type='run')
    depends_on('trf', type='run')
    depends_on('nseg', type='run')
    depends_on('ncbi-rmblastn', type='run')

    def install(self, spec, prefix):
        # like repeatmasker, another interactive installer
        # questions:
        #   1. <enter to continue>
        #   2. <perl path, default is OK>
        #   3. <source path, default is OK>
        #   4. RepeatMasker bin path
        #   5. RECON bin path
        #   6. RepeatScout bin path
        #   7. Nseg bin path
        #   8. trf bin path
        #   9. Add a search engine:
        #        1. RMBlast -> Path, Default? (Y/N)
        #        2. WUBlast/ABBlast -> Path, Default? (Y/N)
        #        3. Done

        config_answers = [
            '', '', '',
            spec['repeatmasker'].prefix.bin,
            spec['recon'].prefix.bin,
            spec['repeatscout'].prefix.bin,
            spec['nseg'].prefix.bin,
            spec['trf'].prefix.bin,
            '1', spec['ncbi-rmblastn'].prefix.bin, 'Y',
            '3',
        ]

        config_filename = 'spack-config.in'

        with open(config_filename, 'w') as f:
            f.write('\n'.join(config_answers))

        with open(config_filename, 'r') as f:
            perl = which('perl')
            perl('configure', input=f)

        install_tree('.', prefix.bin)
