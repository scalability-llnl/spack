# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class MpasModel(MakefilePackage):
    """The Model for Prediction Across Scales (MPAS) is a collaborative
    project for developing atmosphere, ocean and other earth-system
    simulation components for use in climate, regional climate and weather
    studies."""

    homepage = "https://mpas-dev.github.io/"
    url = "https://github.com/MPAS-Dev/MPAS-Model/archive/v7.0.tar.gz"

    version('7.0', sha256='f898ce257e66cff9e29320458870570e55721d16cb000de7f2cc27de7fdef14f')
    version('6.3', sha256='e7f1d9ebfeb6ada37d42a286aaedb2e69335cbc857049dc5c5544bb51e7a8db8')
    version('6.2', sha256='2a81825a62a468bf5c56ef9d9677aa2eb88acf78d4f996cb49a7db98b94a6b16')

    depends_on('mpi')
    depends_on('parallelio')

    patch('makefile.patch', when='@7.0')

    parallel = False

    resource(when='@6.2:6.3',
             name='MPAS-Data',
             git='https://github.com/MPAS-Dev/MPAS-Data.git',
             commit='33561790de8b43087ab850be833f51a4e605f1bb')
    resource(when='@7.0',
             name='MPAS-Data',
             git='https://github.com/MPAS-Dev/MPAS-Data.git',
             tag='v7.0')

    def target(self, model, action):
        spec = self.spec
        satisfies = spec.satisfies
        fflags = [self.compiler.openmp_flag]
        cppflags = ['-D_MPI']
        if satisfies('%gcc'):
            fflags.extend([
                '-ffree-line-length-none',
                '-fconvert=big-endian',
                '-ffree-form',
                '-fdefault-real-8',
                '-fdefault-double-8',
            ])
            cppflags.append('-DUNDERSCORE')
        elif satisfies('%fj'):
            fflags.extend([
                '-Free',
                '-Fwide',
                '-CcdRR8',
            ])
            cppflags.append('-DUNDERSCORE')
        targets = [
            'FC_PARALLEL={0}'.format(spec['mpi'].mpifc),
            'CC_PARALLEL={0}'.format(spec['mpi'].mpicc),
            'CXX_PARALLEL={0}'.format(spec['mpi'].mpicxx),
            'FC_SERIAL={0}'.format(spack_fc),
            'CC_SERIAL={0}'.format(spack_cc),
            'CXX_SERIAL={0}'.format(spack_cxx),
            'CFLAGS_OMP={0}'.format(self.compiler.openmp_flag),
            'FFLAGS_OMP={0}'.format(' '.join(fflags)),
            'CPPFLAGS={0}'.format(' '.join(cppflags)),
            'PIO={0}'.format(spec['parallelio'].prefix),
            'NETCDF={0}'.format(spec['netcdf-c'].prefix),
            'NETCDFF={0}'.format(spec['netcdf-fortran'].prefix)
        ]
        if satisfies('^parallelio+pnetcdf'):
            targets.append(
                'PNETCDF={0}'.format(spec['parallel-netcdf'].prefix)
            )
        targets.extend([
            'USE_PIO2=true', 'CPP_FLAGS=-D_MPI', 'OPENMP=true',
            'CORE={0}'.format(model), action
        ])
        return targets

    def build(self, spec, prefix):
        copy_tree(join_path('MPAS-Data', 'atmosphere'),
                  join_path('src', 'core_atmosphere', 'physics'))
        make(*self.target('init_atmosphere', 'all'))
        mkdir('bin')
        copy('init_atmosphere_model', 'bin')
        make(*self.target('init_atmosphere', 'clean'))
        make(*self.target('atmosphere', 'all'))
        copy('atmosphere_model', 'bin')

    def install(self, spec, prefix):
        install_tree('bin', prefix.bin)
