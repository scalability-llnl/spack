# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost
import os


class Blasr(Package):
    """The PacBio long read aligner."""

    homepage = "https://github.com/PacificBiosciences/blasr/wiki"
    url      = "https://github.com/PacificBiosciences/blasr/archive/5.3.1.tar.gz"

    version('5.3.1', sha256='ff7da5a03096294572e6c64340354da5c5ee1c86c277e7b899f2c170c1ac4049')

    depends_on('ncurses')
    depends_on('hdf5+cxx@1.8.12:1.8.99')
    depends_on('htslib')
    depends_on('zlib')

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)
    depends_on('pbbam')
    depends_on('blasr-libcpp')
    depends_on('python', type='build')

    phases = ['configure', 'build', 'install']

    def setup_build_environment(self, env):
        env.prepend_path('CPATH', self.spec['blasr-libcpp'].prefix)
        env.prepend_path('CPATH', self.spec['blasr-libcpp'].prefix.pbdata)
        env.prepend_path('CPATH', self.spec['blasr-libcpp'].prefix.alignment)
        env.prepend_path('CPATH', self.spec['blasr-libcpp'].prefix.hdf)

        # hdf has +mpi by default, so handle that possibility
        if ('+mpi' in self.spec['hdf5']):
            env.set('CC', self.spec['mpi'].mpicc)
            env.set('CXX', self.spec['mpi'].mpicxx)

    def setup_run_environment(self, env):
        env.prepend_path('PATH', self.spec.prefix.utils)

    def configure(self, spec, prefix):
        configure_args = [
            'LIBPBDATA_INC={0}'.format(
                self.spec['blasr-libcpp'].prefix),
            'LIBPBDATA_LIB={0}'.format(
                self.spec['blasr-libcpp'].prefix.pbdata),
            'LIBBLASR_LIB={0}'.format(
                self.spec['blasr-libcpp'].prefix.alignment),
            'LIBBLASR_INC={0}'.format(
                self.spec['blasr-libcpp'].prefix),
            'LIBPBIHDF_INC={0}'.format(self.spec['blasr-libcpp'].prefix),
            'LIBPBIHDF_LIB={0}'.format(self.spec['blasr-libcpp'].prefix.hdf),
            'HDF5_INC={0}'.format(self.spec['hdf5'].prefix.include),
            'HDF5_LIB={0}'.format(self.spec['hdf5'].prefix.lib),
            '--shared'
        ]
        python('configure.py', *configure_args)

    def build(self, spec, prefix):
        os.environ['CPLUS_INCLUDE_PATH'] = join_path(
            self.stage.source_path, 'include')
        make()

    def install(self, spec, prefix):
        mkdir(prefix.utils)
        mkdir(prefix.bin)
        install('blasr', prefix.bin.blasr)
        install('utils/loadPulses', prefix.utils)
        install('utils/pls2fasta', prefix.utils)
        install('utils/samFilter', prefix.utils)
        install('utils/samtoh5', prefix.utils)
        install('utils/samtom4', prefix.utils)
        install('utils/sawriter', prefix.utils)
        install('utils/sdpMatcher', prefix.utils)
        install('utils/toAfg', prefix.utils)
