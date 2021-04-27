# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# adapted from official quantum espresso package


class QESirius(CMakePackage):
    """SIRIUS enabled fork of QuantumESPRESSO. """

    homepage = 'https://github.com/electronic-structure/q-e-sirius/'
    url = 'https://github.com/electronic-structure/q-e-sirius/archive/v6.5-rc4-sirius.tar.gz'
    git = 'https://github.com/electronic-structure/q-e-sirius.git'

    maintainers = ['simonpintarelli']

    version('develop-ristretto', branch='ristretto', submodules=True)
    version('6.7-rc1-sirius', tag='v6.7-rc1-sirius', submodules=True)

    variant('mpi', default=True, description='Builds with MPI support')
    variant('openmp', default=True, description='Enables OpenMP support')
    variant('scalapack', default=False, description='Enables SCALAPACK support')
    variant('elpa', default=False, description='Uses ELPA as an eigenvalue solver')
    variant('libxc', default=False, description='Support functionals through libxc')
    variant('hdf5', default=False, description='Enables HDF5 support')

    depends_on('sirius +fortran ~apps')
    depends_on('sirius +openmp', when='+openmp')
    depends_on('sirius@develop', when='@develop')

    depends_on('mpi', when='+mpi')
    depends_on('scalapack', when='+scalapack')
    depends_on('elpa', when='+elpa')
    depends_on('libxc', when='+libxc')
    depends_on('hdf5', when='+hdf5')

    depends_on('git', type='build')
    depends_on('pkgconfig', type='build')

    conflicts('~mpi', when='+scalapack', msg='SCALAPACK requires MPI support')
    conflicts('~scalapack', when='+elpa', msg='ELPA requires SCALAPACK support')

    def cmake_args(self):
        args = [
            '-DQE_ENABLE_SIRIUS=ON',
            '-DQE_ENABLE_CUDA=OFF',
            '-DQE_LAPACK_INTERNAL=OFF',
            '-DQE_ENABLE_DOC=OFF',
            self.define_from_variant('QE_ENABLE_MPI', 'mpi'),
            self.define_from_variant('QE_ENABLE_OPENMP', 'openmp'),
            self.define_from_variant('QE_ENABLE_ELPA', 'elpa'),
            self.define_from_variant('QE_ENABLE_LIBXC', 'libxc'),
            self.define_from_variant('QE_ENABLE_HDF5', 'hdf5'),
            self.define_from_variant('QE_ENABLE_SCALAPACK', 'scalapack')
        ]

        # Work around spack issue #19970 where spack sets
        # rpaths for MKL just during make, but cmake removes
        # them during make install.
        if '^mkl' in self.spec:
            args.append('-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON')

        return args
