# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CandleBenchmarks(Package):
    """ECP-CANDLE Benchmarks"""

    homepage = "https://github.com/ECP-CANDLE/Benchmarks"
    url      = "https://github.com/ECP-CANDLE/Benchmarks/archive/v0.1.tar.gz"

    tags = ['proxy-app', 'ecp-proxy-app']

    version('0.1', sha256='767f74f43ee3a5d4e0f26750f2a96b8433e25a9cd4f2d29938ac8acf263ab58d')

    variant('mpi', default=True, description='Build with MPI support')

    extends('python')
    depends_on('python@2.7:')
    depends_on('py-theano +gpu', type=('build', 'run'))
    depends_on('py-keras', type=('build', 'run'))
    depends_on('py-matplotlib +image@:2.2.3', type=('build', 'run'))
    depends_on('py-tqdm', type=('build', 'run'))
    depends_on('py-scikit-learn', type=('build', 'run'))
    depends_on('opencv@3.2.0: +core +highgui +imgproc +jpeg +png +tiff +zlib +python -dnn ~eigen ~gtk')
    depends_on('py-mdanalysis', type=('build', 'run'))
    depends_on('py-mpi4py', when='+mpi', type=('build', 'run'))
    depends_on('py-h5py~mpi', when='~mpi', type=('build', 'run'))
    depends_on('py-h5py+mpi', when='+mpi', type=('build', 'run'))
    depends_on('py-requests', type=('build', 'run'))

    # see #3244, but use external for now
    # depends_on('tensorflow')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix.bin)
