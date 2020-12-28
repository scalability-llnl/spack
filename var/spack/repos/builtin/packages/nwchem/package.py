# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


class Nwchem(Package):
    """High-performance computational chemistry software"""

    homepage = "https://nwchemgit.github.io"
    url      = "https://github.com/nwchemgit/nwchem/releases/download/v7.0.2-release/nwchem-7.0.2-release.revision-b9985dfa-srconly.2020-10-12.tar.bz2"

    tags = ['ecp', 'ecp-apps']

    version('7.0.2', sha256='9bf913b811b97c8ed51bc5a02bf1c8e18456d0719c0a82b2e71223a596d945a7',
            url='https://github.com/nwchemgit/nwchem/releases/download/v7.0.2-release/nwchem-7.0.2-release.revision-b9985dfa-srconly.2020-10-12.tar.bz2')
    version('7.0.0', sha256='e3c6510627345be596f4079047e5e7b59e6c20599798ecfe122e3527f8ad6eb0',
            url='https://github.com/nwchemgit/nwchem/releases/download/v7.0.0-release/nwchem-7.0.0-release.revision-2c9a1c7c-srconly.2020-02-26.tar.bz2')
    version('6.8.1', sha256='fd20f9ca1b410270a815e77e052ec23552f828526cd252709f798f589b2a6431',
            url='https://github.com/nwchemgit/nwchem/releases/download/6.8.1-release/nwchem-6.8.1-release.revision-v6.8-133-ge032219-srconly.2018-06-14.tar.bz2')

    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi')
    depends_on('scalapack')
    depends_on('python@3:', when='@7:', type=('build', 'link', 'run'))
    depends_on('python@2.7:2.8', when='@:6', type=('build', 'link', 'run'))
    conflicts('%gcc@10:', when='@:6', msg='NWChem versions prior to 7.0.0 do not build with GCC 10')

    def install(self, spec, prefix):
        scalapack = spec['scalapack'].libs
        lapack = spec['lapack'].libs
        blas = spec['blas'].libs
        # see https://nwchemgit.github.io/Compiling-NWChem.html
        args = []
        args.extend([
            'NWCHEM_TOP=%s' % self.stage.source_path,
            # NWCHEM is picky about FC and CC. They should NOT be full path.
            # see https://nwchemgit.github.io/Special_AWCforum/sp/id7524
            'CC=%s' % os.path.basename(spack_cc),
            'FC=%s' % os.path.basename(spack_fc),
            'USE_MPI=y',
            'PYTHONVERSION=%s' % spec['python'].version.up_to(2),
            'BLASOPT=%s' % ((lapack + blas).ld_flags),
            'BLAS_LIB=%s' % blas.ld_flags,
            'LAPACK_LIB=%s' % lapack.ld_flags,
            'SCALAPACK_LIB=%s' % scalapack.ld_flags,
            'NWCHEM_MODULES=all python',
            'NWCHEM_LONG_PATHS=Y',  # by default NWCHEM_TOP is 64 char max
            'USE_NOIO=Y'  # skip I/O algorithms
        ])
        if spec.version < Version('7.0.0'):
            args.extend([
                'PYTHONVERSION=%s' % spec['python'].version.up_to(2),
                'PYTHONHOME=%s' % spec['python'].home,
                'USE_PYTHONCONFIG=Y',
            ])

        # TODO: query if blas/lapack/scalapack uses 64bit Ints
        # A flag to distinguish between 32bit and 64bit integers in linear
        # algebra (Blas, Lapack, Scalapack)
        use_32_bit_lin_alg = True

        if use_32_bit_lin_alg:
            args.extend([
                'USE_64TO32=y',
                'BLAS_SIZE=4',
                'LAPACK_SIZE=4',
                'SCALAPACK_SIZE=4'
            ])
        else:
            args.extend([
                'BLAS_SIZE=8',
                'LAPACK_SIZE=8'
                'SCALAPACK_SIZE=8'
            ])

        if sys.platform == 'darwin':
            target = 'MACX64'
            args.extend([
                'CFLAGS_FORGA=-DMPICH_NO_ATTR_TYPE_TAGS'
            ])
        else:
            target = 'LINUX64'

        args.extend(['NWCHEM_TARGET=%s' % target])

        with working_dir('src'):
            make('nwchem_config', *args)
            if use_32_bit_lin_alg:
                make('64_to_32', *args)
            make(*args)

            #  need to install by hand. Follow Ubuntu:
            #  http://packages.ubuntu.com/trusty/all/nwchem-data/filelist
            #  http://packages.ubuntu.com/trusty/amd64/nwchem/filelist
            share_path = join_path(prefix, 'share', 'nwchem')
            mkdirp(prefix.bin)

            install_tree('data', share_path)
            install_tree(join_path('basis', 'libraries'),
                         join_path(share_path, 'libraries'))
            install_tree(join_path('nwpw', 'libraryps'),
                         join_path(share_path, 'libraryps'))

            b_path = join_path(self.stage.source_path, 'bin',
                               target, 'nwchem')
            chmod = which('chmod')
            chmod('+x', b_path)
            install(b_path, prefix.bin)

            # Finally, make user's life easier by creating a .nwchemrc file
            # to point to the required data files.
            nwchemrc = """\
   nwchem_basis_library {data}/libraries/
   nwchem_nwpw_library {data}/libraryps/
   ffield amber
   amber_1 {data}/amber_s/
   amber_2 {data}/amber_q/
   amber_3 {data}/amber_x/
   amber_4 {data}/amber_u/
   spce    {data}/solvents/spce.rst
   charmm_s {data}/charmm_s/
   charmm_x {data}/charmm_x/
""".format(data=share_path)
            with open(".nwchemrc", 'w') as f:
                f.write(nwchemrc)
            install(".nwchemrc", share_path)

    def setup_run_environment(self, env):
        env.set('NWCHEM_BASIS_LIBRARY', join_path(
            self.prefix,
            'share/nwchem/libraries/'))
        env.set('NWCHEM_NWPW_LIBRARY', join_path(
            self.prefix,
            'share/nwchem/libraryps/'))
