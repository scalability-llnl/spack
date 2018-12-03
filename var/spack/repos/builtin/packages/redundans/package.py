# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Redundans(Package):
    """Redundans pipeline assists an assembly of heterozygous genomes."""

    homepage = "https://github.com/Gabaldonlab/redundans"
    url      = "https://github.com/Gabaldonlab/redundans/archive/v0.13c.tar.gz"
    git      = "https://github.com/Gabaldonlab/redundans.git"

    version('0.14a', commit='a20215a862aed161cbfc79df9133206156a1e9f0')
    version('0.13c', '2003fb7c70521f5e430553686fd1a594',
            preferred=True)

    depends_on('python', type=('build', 'run'))
    depends_on('py-pyscaf', type=('build', 'run'))
    depends_on('py-fastaindex', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('perl', type=('build', 'run'))
    depends_on('sspace-standard')
    depends_on('bwa')
    depends_on('last')
    depends_on('gapcloser')
    depends_on('parallel')
    depends_on('snap-berkeley@1.0beta.18:', type=('build', 'run'))

    def install(self, spec, prefix):
        sspace_location = join_path(spec['sspace-standard'].prefix,
                                    'SSPACE_Standard_v3.0.pl')
        mkdirp(prefix.bin)
        filter_file(r'sspacebin = os.path.join(.*)$',
                    'sspacebin = \'' + sspace_location + '\'',
                    'redundans.py')

        binfiles = ['fasta2homozygous.py', 'fasta2split.py',
                    'fastq2insert_size.py', 'fastq2mates.py',
                    'fastq2shuffled.py', 'fastq2sspace.py',
                    'filterReads.py', 'redundans.py']

        # new internal dep with 0.14a
        if spec.satisfies('@0.14a:'):
            binfiles.extend(['denovo.py'])

        with working_dir('bin'):
            for f in binfiles:
                install(f, prefix.bin)
