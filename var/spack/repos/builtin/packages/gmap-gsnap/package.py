# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GmapGsnap(AutotoolsPackage):
    """GMAP: A Genomic Mapping and Alignment Program for
       mRNA and EST Sequences, and GSNAP: Genomic Short-read
       Nucleotide Alignment Program"""

    homepage = "http://research-pub.gene.com/gmap/"
    url      = "http://research-pub.gene.com/gmap/src/gmap-gsnap-2017-06-16.tar.gz"

    version('2021-03-08', sha256='00de0e945b86bcbda50df94c68a61957f3783e232cce466fcd5f8d3a55398aa2')
    version('2020-06-01', sha256='7917f9f78570943f419445e371f2cc948c6741e73c3cbb063391756f4479d365')
    version('2019-05-12', sha256='3dc1b6ee4f6c049c07bcf4a5aba30eb2d732997241cdcad818dab571719f8008')
    version('2019-02-15', sha256='7e82b9867a1e561b4816fb2f2fb916294077c384c6a88bb94cce39bfe71ab3ac')
    version('2018-07-04', sha256='a9f8c1f0810df65b2a089dc10be79611026f4c95e4681dba98fea3d55d598d24')
    version('2018-03-25', sha256='a65bae6115fc50916ad7425d0b5873b611c002690bf35026bfcfc41ee0c0265a')
    version('2018-02-12', sha256='5dedddab7f08f9924a995332ebc7bdbe2621fcd67021690707c876d865091fcc')
    version('2017-06-16', sha256='2a277a6d45cade849be3bfb7b0f69f61ab79744af821a88eb1d599b32f358f8d')
    version('2014-12-28', sha256='108433f3e3ea89b8117c8bb36d396913225caf1261d46ce6d89709ff1b44025d')

    depends_on('zlib')
    depends_on('bzip2')

    variant(
        'simd',
        description='CPU support.',
        values=('avx2', 'sse42', 'avx512', 'sse2'),
        multi=True,
        default='sse2'
    )

    def configure(self, spec, prefix):
        configure = Executable('../configure')

        for simd in spec.variants['simd'].value:
            with working_dir(simd, create=True):
                configure('--with-simd-level={0}'.format(simd),
                          '--prefix={0}'.format(prefix))

    def build(self, spec, prefix):
        for simd in spec.variants['simd'].value:
            with working_dir(simd):
                make()

    def check(self):
        for simd in self.spec.variants['simd'].value:
            with working_dir(simd):
                make('check')

    def install(self, spec, prefix):
        for simd in spec.variants['simd'].value:
            with working_dir(simd):
                make('install')
