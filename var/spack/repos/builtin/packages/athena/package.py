# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Athena(AutotoolsPackage):
    """Athena is a grid-based code for astrophysical magnetohydrodynamics
    (MHD). It was developed primarily for studies of the interstellar medium,
    star formation, and accretion flows."""

    homepage = "https://princetonuniversity.github.io/Athena-Cversion/"
    url      = "https://github.com/PrincetonUniversity/Athena-Cversion/archive/version-4.2.tar.gz"
    git      = "https://github.com/PrincetonUniversity/Athena-Cversion.git"

    version('master', branch='master')
    version('4.2', sha256='6334848d7f1325aa44859418feac8ce223b56793ae8907103000af5b27f50e7e')

    # PHYSICS "packages":
    variant('problem', default='linear_wave', description='Problem generator',
            values=[
                'blast',
                'carbuncle',
                'collapse3d',
                'cpaw',
                'cshock1d',
                'current_sheet',
                'cyladvect',
                'cylblast',
                'cylbphi',
                'cylbr',
                'cylcvmri',
                'cyldiff',
                'cylfieldloop',
                'cylnewtmri',
                'cylrayleigh',
                'cylspiral',
                'cylwind',
                'cylwindrot',
                'cylwindrotb',
                'dmr',
                'fft_test',
                'field_loop',
                'firehose',
                'hall_drift',
                'hb3',
                'hgb',
                'hkdisk',
                'jeans',
                'jet',
                'kh',
                'linear_wave',
                'lw_implode',
                'msa',
                'noh',
                'orszag-tang',
                'par_collision',
                'par_epicycle',
                'par_strat2d',
                'par_strat3d',
                'pgflow',
                'rotor',
                'rt',
                'shk_cloud',
                'shkset1d',
                'shkset2d',
                'shkset3d',
                'shu-osher',
                'strat',
                'streaming2d_multi',
                'streaming2d_single',
                'streaming3d_multi',
                'streaming3d_single',
                'twoibw'
            ])
    variant('gas', default='mhd', description='Gas properties',
            values=['mhd', 'hydro'])
    variant('eos', default='adiabatic', description='Equation of state',
            values=['adiabatic', 'isothermal'])
    variant('nscalars', default=0, description='Number of advected scalars')
    variant('gravity', default='none', description='Algorithm for self gravity',
            values=['fft', 'fft_disk', 'fft_obc', 'multigrid', 'none'])
    variant('particles', default='none',
            description='Dust particle integration algorithm',
            values=['feedback', 'passive', 'none'])
    variant('coord', default='cartesian', description='Coordinate System',
            values=['cartesian', 'cylindrical'])

    # PHYSICS "features":
    variant('conduction', default=False, description='Enable thermal conduction')
    variant('resistivity', default=False, description='Enable resistivity')
    variant('special_relativity', default=False, description='Enable special relativistic hydro or MHD')
    variant('viscosity', default=False, description='Enable viscosity')

    # ALGORITHM "packages":
    variant('order', default='2',
            description='Order and type of spatial reconstruction',
            values=['1', '2', '3', '2p', '3p'])
    variant('flux', default='roe', description='Flux function', values=[
        'roe', 'hllc', 'hlld', 'hlle', 'force', 'exact', 'two-shock'
    ])
    variant('integrator', default='ctu',
            description='Unsplit integration algorithm',
            values=['ctu', 'vl'])
    variant('cflags', default='opt', description='Compiler flags',
            values=['opt', 'debug', 'profile'])

    # ALGORITHM "features":
    variant('fargo', default=False, description='Enable FARGO algorithm')
    variant('fft', default=False, description='Use FFTW block decomposition')
    variant('fofc', default=False, description='Enable first-order flux correction')
    variant('ghost', default=False, description='Write ghost zones')
    variant('h_correction', default=False, description='Turn on H-correction')
    variant('mpi', default=True, description='Enable MPI parallelization')
    variant('shearing_box', default=False, description='Turn on shearing-box')
    variant('single', default=False, description='Use single-precision instead of double-precision')
    variant('sts', default=False, description='Turn on super timestepping')
    variant('smr', default=False, description='Use static mesh refinement')
    variant('rotating_frame', default=False, description='Turn on rotating_frame')
    variant('l1_inflow', default=False, description='Enable inflow from L1 point')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('mpi', when='+mpi')
    depends_on('fftw', when='+fft')

    conflicts('flux=hllc', when='gas=mhd')
    conflicts('flux=exact', when='gas=mhd')
    conflicts('flux=two-shock', when='gas=mhd')
    conflicts('+h_correction', when='flux=hllc')
    conflicts('+h_correction', when='flux=hlld')
    conflicts('+h_correction', when='flux=hlle')
    conflicts('+h_correction', when='flux=force')
    conflicts('+h_correction', when='flux=exact')
    conflicts('+h_correction', when='flux=two-shock')
    conflicts('coord=cylindrical', when='gravity=none')
    conflicts('coord=cylindrical', when='particles=none')
    conflicts('integrator=vl', when='order=3')
    conflicts('integrator=vl', when='order=2')

    build_targets = ['all']

    patch('missing-separator.patch')

    def setup_build_environment(self, env):
        spec = self.spec

        env.set('OPT', '-O3')

        if '+mpi' in spec:
            env.set('CC', spec['mpi'].mpicc)
            env.set('LDR', spec['mpi'].mpicc)
            env.set('MPILIB', spec['mpi'].libs.ld_flags)
            env.set('MPIINC', spec['mpi'].headers.include_flags)
        else:
            env.set('CC', spack_cc)
            env.set('LDR', spack_cc)

        if '+fft' in spec:
            env.set('FFTWLIB', spec['fftw'].libs.ld_flags)
            env.set('FFTWINC', spec['fftw'].headers.include_flags)

    def configure_args(self):
        spec = self.spec
        args = []

        if '+conduction' in spec:
            args.append('--enable-conduction')
        else:
            args.append('--disable-conduction')

        if '+resistivity' in spec:
            args.append('--enable-resistivity')
        else:
            args.append('--disable-resistivity')

        if '+special_relativity' in spec:
            args.append('--enable-special-relativity')
        else:
            args.append('--disable-special-relativity')

        if '+viscosity' in spec:
            args.append('--enable-viscosity')
        else:
            args.append('--disable-viscosity')

        if '+single' in spec:
            args.append('--enable-single')
        else:
            args.append('--disable-single')

        if '+ghost' in spec:
            args.append('--enable-ghost')
        else:
            args.append('--disable-ghost')

        if '+mpi' in spec:
            args.append('--enable-mpi')
        else:
            args.append('--disable-mpi')

        if '+h_correction' in spec:
            args.append('--enable-h-correction')
        else:
            args.append('--disable-h-correction')

        if '+fft' in spec:
            args.append('--enable-fft')
        else:
            args.append('--disable-fft')

        if '+shearing_box' in spec:
            args.append('--enable-shearing-box')
        else:
            args.append('--disable-shearing-box')

        if '+fargo' in spec:
            args.append('--enable-fargo')
        else:
            args.append('--disable-fargo')

        if '+sts' in spec:
            args.append('--enable-sts')
        else:
            args.append('--disable-sts')

        if '+smr' in spec:
            args.append('--enable-smr')
        else:
            args.append('--disable-smr')

        if '+fofc' in spec:
            args.append('--enable-fofc')
        else:
            args.append('--disable-fofc')

        if '+rotating_frame' in spec:
            args.append('--enable-rotating_frame')
        else:
            args.append('--disable-rotating_frame')

        if '+l1_inflow' in spec:
            args.append('--enable-l1_inflow')
        else:
            args.append('--disable-l1_inflow')

        args.extend([
            '--with-problem=' + spec.variants['problem'].value,
            '--with-gas=' + spec.variants['gas'].value,
            '--with-eos=' + spec.variants['eos'].value,
            '--with-nscalars=' + spec.variants['nscalars'].value,
            '--with-gravity=' + spec.variants['gravity'].value,
            '--with-particles=' + spec.variants['particles'].value,
            '--with-coord=' + spec.variants['coord'].value,
            '--with-order=' + spec.variants['order'].value,
            '--with-flux=' + spec.variants['flux'].value,
            '--with-integrator=' + spec.variants['integrator'].value,
            '--with-cflags=' + spec.variants['cflags'].value,
        ])

        return args

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('bin/athena', prefix.bin)
