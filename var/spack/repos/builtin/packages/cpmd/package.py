# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Cpmd(MakefilePackage):
    """The CPMD code is a parallelized plane wave / pseudopotential
    implementation of Density Functional Theory, particularly
    designed for ab-initio molecular dynamics.
    Move to new directory, download CPMD main archive and patch.to.XXXXs
    manually, and run Spack"""

    homepage = "https://www.cpmd.org/wordpress/"
    basedir = os.getcwd()
    url = "file://{0}/cpmd-v4.3.tar.gz".format(basedir)
    manual_download = True

    version('4.3', sha256='4f31ddf045f1ae5d6f25559d85ddbdab4d7a6200362849df833632976d095df4')

    variant('omp', description='Enables the use of OMP instructions',
            default=False)
    variant('mpi', description='Build with MPI support', default=False)

    depends_on('lapack')
    depends_on('mpi', when='+mpi')

    conflicts('^openblas threads=none', when='+omp')
    conflicts('^openblas threads=pthreads', when='+omp')

    patch('file://{0}/patch.to.4612'.format(basedir), sha256='3b7d91e04c40418ad958069234ec7253fbf6c4be361a1d5cfd804774eeb44915', level=0, when='@4.3')
    patch('file://{0}/patch.to.4615'.format(basedir), sha256='5ec5790fb6ca64632bcc1b0f5b8f3423c54455766a0979ff4136624bbe8d49eb', level=0, when='@4.3')
    patch('file://{0}/patch.to.4616'.format(basedir), sha256='ac0bc215c4259f55da4dc59803fe636f797e241f8a01974e05730c9778ad44c4', level=0, when='@4.3')
    patch('file://{0}/patch.to.4621'.format(basedir), sha256='2d2bc7e37246032fc354f51da7dbdb5a219dd228867399931b0e94da1265d5ca', level=0, when='@4.3')
    patch('file://{0}/patch.to.4624'.format(basedir), sha256='0a19687528264bf91c9f50ffdc0b920a8511eecf5259b667c8c29350f9dabc53', level=0, when='@4.3')

    def edit(self, spec, prefix):
        # patch configure file
        cbase = 'LINUX-GFORTRAN'
        cp = FileFilter(join_path('configure', cbase))
        # Compilers
        if spec.satisfies('+mpi'):
            fc = spec["mpi"].mpifc
            cc = spec["mpi"].mpicc
        else:
            fc = spack_fc
            cc = spack_cc

        cp.filter('FC=.+', "FC='{0}'".format(fc))
        cp.filter('CC=.+', "CC='{0}'".format(cc))
        cp.filter('LD=.+', "LD='{0}'".format(fc))

        # MPI flag
        if spec.satisfies('+mpi'):
            cp.filter('-D__Linux', '-D__Linux -D__PARALLEL')

        # OMP flag
        if spec.satisfies('+omp'):
            cp.filter('-fopenmp', self.compiler.openmp_flag)

        # lapack
        cp.filter(
            'LIBS=.+',
            "LIBS='{0}'".format(spec['lapack'].libs.ld_flags)
        )

        # LFLAGS
        cp.filter("'-static '", '')

        # Compiler specific
        if spec.satisfies('%fj'):
            cp.filter('-ffixed-form', '-Fixed')
            cp.filter('-ffree-line-length-none', '')
            cp.filter('-falign-commons', '-Kalign_commons')

        # create Makefile
        bash = which('bash')
        if spec.satisfies('+omp'):
            bash('./configure.sh', '-omp', cbase)
        else:
            bash('./configure.sh', cbase)

    def install(self, spec, prefix):
        install_tree('.', prefix)

    def test(self):
        test_dir = self.test_suite.current_test_data_dir
        test_file = join_path(test_dir, '1-h2o-pbc-geoopt.inp')
        opts = []
        if self.spec.satisfies('+mpi'):
            exe_name = self.spec['mpi'].prefix.bin.mpirun
            opts.extend(['-n', '2'])
            opts.append(join_path(self.prefix.bin, 'cpmd.x'))
        else:
            exe_name = 'cpmd.x'
        opts.append(test_file)
        opts.append(test_dir)
        expected = ['2       1        H        O              1.84444     0.97604',
                    '3       1        H        O              1.84444     0.97604',
                    '2   1   3         H     O     H              103.8663'
                    ]
        self.run_test(exe_name, options=opts, expected=expected)
