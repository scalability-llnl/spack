# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Alps(CMakePackage):
    """Algorithms for Physics Simulations

    Tags: Condensed Matter Physics, Computational Physics
    """

    homepage = "https://alps.comp-phys.org"
    url      = "http://alps.comp-phys.org/static/software/releases/alps-2.3.0-src.tar.gz"

    version('2.3.0', sha256='e64208d1e5acdd6f569277413c4867e1fa366cf4a224570eacbf1e9939fca2d2')

    # Refs for building from source and recipes
    # http://alps.comp-phys.org/mediawiki/index.php/Building_ALPS_from_source
    # https://github.com/easybuilders/easybuild-easyconfigs/tree/master/easybuild/easyconfigs/a/ALPS
    # https://github.com/conda-forge/alps-feedstock/tree/master/recipe

    # Package failed to build with boost version >= 1.64
    depends_on('boost@:1.63.0 +chrono +date_time +filesystem +iostreams +mpi +numpy +program_options +python +regex +serialization +system +test +thread +timer')
    depends_on('fftw')
    depends_on('hdf5 ~mpi+hl')
    depends_on('lapack')
    # build fails for latest python@3.7
    depends_on('python@:3.6.99', type=('build', 'link', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))

    # use depends_on to help with dependency resolution
    depends_on('py-numpy@:1.19', when='^python@:3.6.99')
    depends_on('py-scipy@:1.5', when='^python@:3.6.99')

    # fix for gcc@7:
    patch('alps_newgcc.patch', when='%gcc@7:')

    # remove a problematic build variable
    patch('mpi.patch')

    # include climits to use INT_MAX
    patch('alps_climit.patch')

    # ctest tries to test '/usr/bin/time'
    patch('alps_cmake_time.patch')

    extends('python')

    root_cmakelists_dir = 'alps'

    def cmake_args(self):
        args = []
        args.append('Boost_ROOT_DIR=' + self.spec['boost'].prefix)
        args.append("-DCMAKE_CXX_FLAGS={0}".format(self.compiler.cxx98_flag))
        return args

    def _single_test(self, target, exename, dataname, opts=[]):
        troot = self.prefix.tutorials
        copy_tree(join_path(troot, target), target)

        if target == 'dmrg-01-dmrg':
            test_dir = self.test_suite.current_test_data_dir
            copy(join_path(test_dir, dataname), target)

        self.run_test('parameter2xml',
                      options=[dataname, 'SEED=123456'],
                      work_dir=target
                      )
        options = []
        options.extend(opts)
        options.extend(['--write-xml', '{0}.in.xml'.format(dataname)])
        self.run_test(exename,
                      options=options,
                      expected=['Finished with everything.'],
                      work_dir=target
                      )

    def test(self):
        self._single_test('mc-02-susceptibilities', 'spinmc', 'parm2a',
                          ['--Tmin', '10'])
        self._single_test('ed-01-sparsediag', 'sparsediag', 'parm1a')
        self._single_test('dmrg-01-dmrg', 'dmrg', 'spin_one_half')
