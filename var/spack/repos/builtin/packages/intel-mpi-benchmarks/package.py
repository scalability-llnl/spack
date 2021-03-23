# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class IntelMpiBenchmarks(MakefilePackage):
    """Intel(R) MPI Benchmarks provides a set of elementary benchmarks
       that conform to MPI-1, MPI-2, and MPI-3 standard.
       You can run all of the supported benchmarks, or a subset specified
       in the command line using one executable file.
       Use command-line parameters to specify various settings, such as
       time measurement, message lengths, and selection of communicators. """

    homepage = "https://software.intel.com/en-us/articles/intel-mpi-benchmarks"
    url      = "https://github.com/intel/mpi-benchmarks/archive/IMB-v2019.5.tar.gz"

    maintainers = ['carsonwoods']

    version('2019.6', sha256='1cd0bab9e947228fced4666d907f77c51336291533919896a923cff5fcad62e9')
    version('2019.5', sha256='61f8e872a3c3076af53007a68e4da3a8d66be2ba7a051dc21e626a4e2d26e651')
    version('2019.4', sha256='aeb336be10275c1a2f579b491b6631122876b461ac7148b1d0764f13b7552690')
    version('2019.3', sha256='4f256d11bfed9ca6166548486d61a062e67be61f13dd9f30690232720e185f31')
    version('2019.2', sha256='0bc2224a913073aaa5958f6ae08341e5fcd39cedc6722a09bfd4a3d7591a340b')

    depends_on('mpi')

    # https://github.com/intel/mpi-benchmarks/pull/19
    patch('add_const.patch', when='@:2019.6')
    # https://github.com/intel/mpi-benchmarks/pull/20
    patch('reorder_benchmark_macros.patch', when='@:2019.6')

    variant(
        'benchmark', default='all',
        values=('mpi1', 'ext', 'io', 'nbc',
                'p2p', 'rma', 'mt', 'all'),
        multi=False,
        description='Specify which benchmark to build')

    def build(self, spec, prefix):
        env['CC'] = spec['mpi'].mpicc
        env['CXX'] = spec['mpi'].mpicxx

        if 'benchmark=mpi1' in spec:
            make('IMB-MPI1')
        elif 'benchmark=ext' in spec:
            make('IMB-EXT')
        elif 'benchmark=io' in spec:
            make('IMB-IO')
        elif 'benchmark=nbc' in spec:
            make('IMB-NBC')
        elif 'benchmark=p2p' in spec:
            make('IMB-P2P')
        elif 'benchmark=rma' in spec:
            make('IMB-RMA')
        elif 'benchmark=mt' in spec:
            make('IMB-MT')
        else:
            make("all")

    def install(self, spec, prefix):
        mkdir(prefix.bin)

        if 'benchmark=mpi1' in spec:
            install('IMB-MPI1', prefix.bin)
        elif 'benchmark=ext' in spec:
            install('IMB-EXT', prefix.bin)
        elif 'benchmark=io' in spec:
            install('IMB-IO', prefix.bin)
        elif 'benchmark=nbc' in spec:
            install('IMB-NBC', prefix.bin)
        elif 'benchmark=p2p' in spec:
            install('IMB-P2P', prefix.bin)
        elif 'benchmark=rma' in spec:
            install('IMB-RMA', prefix.bin)
        elif 'benchmark=mt' in spec:
            install('IMB-MT', prefix.bin)
        else:
            install('IMB-EXT',  prefix.bin)
            install('IMB-IO',   prefix.bin)
            install('IMB-MPI1', prefix.bin)
            install('IMB-MT',   prefix.bin)
            install('IMB-NBC',  prefix.bin)
            install('IMB-P2P',  prefix.bin)
            install('IMB-RMA',  prefix.bin)
