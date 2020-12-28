# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Moab(AutotoolsPackage):
    """MOAB is a component for representing and evaluating mesh
    data. MOAB can store structured and unstructured mesh, consisting
    of elements in the finite element 'zoo.' The functional interface
    to MOAB is simple yet powerful, allowing the representation of
    many types of metadata commonly found on the mesh. MOAB is
    optimized for efficiency in space and time, based on access to
    mesh in chunks rather than through individual entities, while also
    versatile enough to support individual entity access."""

    homepage = "https://bitbucket.org/fathomteam/moab"
    git = "https://bitbucket.org/fathomteam/moab.git"
    url = "http://ftp.mcs.anl.gov/pub/fathom/moab-5.0.0.tar.gz"

    maintainers = ['vijaysm', 'iulian787']

    version('develop', branch='develop')
    version('master', branch='master')
    version('5.2.1', sha256='60d31762be3f0e5c89416c764e844ec88dac294169b59a5ead3c316b50f85c29')
    version('5.2.0', sha256='805ed3546deff39e076be4d1f68aba1cf0dda8c34ce43e1fc179d1aff57c5d5d')
    version('5.1.0', sha256='0371fc25d2594589e95700739f01614f097b6157fb6023ed8995e582726ca658')
    version('5.0.2', commit='01d05b1805236ef44da36f67eb2701095f2e33c7')
    version('5.0.1', commit='6cc12bd4ae3fa7c9ad81c595e4d38fa84f0884be')
    version('5.0.0', sha256='df5d5eb8c0d0dbb046de2e60aa611f276cbf007c9226c44a24ed19c570244e64')
    version('4.9.2', sha256='26611b8cc24f6b7df52eb4ecbd31523d61523da0524b5a2d066a7656e2e82ac5')
    version('4.9.1', sha256='b26cee46c096157323cafe047ad58616e16ebdb1e06caf6878673817cb4410cf')
    version('4.9.0', sha256='267a7c05da847e4ea856db2c649a5484fb7bdc132ab56721ca50ee69a7389f4d')
    version('4.8.2', sha256='b105cff42930058dc14eabb9a25e979df7289b175732fe319d2494e83e09e968')

    variant('mpi', default=True, description='enable mpi support')
    variant('hdf5', default=True,
            description='Required to enable the hdf5 (default I/O) format')
    variant('netcdf', default=False,
            description='Required to enable the ExodusII reader/writer.')
    variant('pnetcdf', default=False,
            description='Enable pnetcdf (AKA parallel-netcdf) support')
    variant('zoltan', default=False, description='Enable zoltan support')
    variant('cgm', default=False, description='Enable common geometric module')
    variant('metis', default=True, description='Enable metis link')
    variant('parmetis', default=True, description='Enable parmetis link')
    variant('irel', default=False, description='Enable irel interface')
    variant('fbigeom', default=False, description='Enable fbigeom interface')
    variant('coupler', default=True, description='Enable mbcoupler tool')
    variant('dagmc', default=False, description='Enable dagmc tool')

    variant("debug", default=False, description='enable debug symbols')
    variant('shared', default=False,
            description='Enables the build of shared libraries')
    variant('fortran', default=True, description='Enable Fortran support')

    conflicts('+irel', when='~cgm')
    conflicts('+pnetcdf', when='~mpi')
    conflicts('+parmetis', when='~mpi')
    conflicts('+coupler', when='~mpi')

    # There are many possible variants for MOAB. Here are examples for
    # two of them:
    #
    # variant('vtk', default=False, description='Enable VTK support')
    # variant('cgns', default=False, description='Enable CGNS support')
    # depends_on('cgns', when='+cgns')
    # depends_on('vtk', when='+vtk')

    depends_on('autoconf', type='build', when='@master,5.0.1:')
    depends_on('automake', type='build', when='@master,5.0.1:')
    depends_on('libtool', type='build', when='@master,5.0.1:')
    depends_on('m4', type='build', when='@master,5.0.1:')
    depends_on('blas')
    depends_on('lapack')
    depends_on('mpi', when='+mpi')
    depends_on('hdf5', when='+hdf5')
    depends_on('hdf5+mpi', when='+hdf5+mpi')
    depends_on('netcdf-c', when='+netcdf')
    depends_on('parallel-netcdf', when='+pnetcdf')
    depends_on('cgm', when='+cgm')
    depends_on('metis', when='+metis')
    depends_on('parmetis', when='+parmetis')
    # FIXME it seems that zoltan needs to be built without fortran
    depends_on('zoltan~fortran', when='+zoltan')

    patch('tools-492.patch', when='@4.9.2')

    @run_before('configure')
    def remove_march_native(self):
        filter_file('-march=native', '', 'configure', string=True)

    def configure_args(self):
        spec = self.spec

        options = [
            '--enable-optimize',
            '--disable-vtkMOABReader',
            '--disable-mbtagprop',
            '--disable-mbmem',
            '--disable-spheredecomp',
            '--disable-mbsurfplot',
            '--disable-gsets',
            '--disable-mcnpmit',
            '--disable-refiner',
            '--disable-h5mtools',
            '--disable-mbcslam',
            '--with-pic',
            '--without-vtk'
        ]
        if '+mpi' in spec:
            options.extend([
                '--with-mpi=%s' % spec['mpi'].prefix,
                'CXX=%s' % spec['mpi'].mpicxx,
                'CC=%s' % spec['mpi'].mpicc,
                'FC=%s' % spec['mpi'].mpifc
            ])
            if '+parmetis' in spec:
                options.append('--with-parmetis=%s' % spec['parmetis'].prefix)
            else:
                options.append('--without-parmetis')
#          FIXME: --without-mpi does not configure right
#       else:
#           options.append('--without-mpi')

        options.append('--with-blas=%s' % spec['blas'].libs.ld_flags)
        options.append('--with-lapack=%s' % spec['lapack'].libs.ld_flags)

        if '+hdf5' in spec:
            options.append('--with-hdf5=%s' % spec['hdf5'].prefix)
        else:
            options.append('--without-hdf5')

        if '+netcdf' in spec:
            options.append('--with-netcdf=%s' % spec['netcdf-c'].prefix)
        else:
            options.append('--without-netcdf')

        if '+pnetcdf' in spec:
            options.append('--with-pnetcdf=%s'
                           % spec['parallel-netcdf'].prefix)
        else:
            options.append('--without-pnetcdf')

        if '+cgm' in spec:
            options.append('--with-cgm=%s' % spec['cgm'].prefix)
            if '+irel' in spec:
                options.append('--enable-irel')
            else:
                options.append('--disable-irel')
        else:
            options.append('--without-cgm')
        if '+fbigeom' in spec:
            options.append('--enable-fbigeom')
        else:
            options.append('--disable-fbigeom')

        if '+coupler' in spec:
            options.append('--enable-mbcoupler')
        else:
            options.append('--disable-mbcoupler')

        if '+dagmc' in spec:
            options.append('--enable-dagmc')
        else:
            options.append('--disable-dagmc')

        if '+metis' in spec:
            options.append('--with-metis=%s' % spec['metis'].prefix)
        else:
            options.append('--without-metis')

        if '+parmetis' in spec:
            options.append('--with-parmetis=%s' % spec['parmetis'].prefix)
        else:
            options.append('--without-parmetis')

        if '+zoltan' in spec:
            options.append('--with-zoltan=%s' % spec['zoltan'].prefix)
        else:
            options.append('--without-zoltan')

        if '+debug' in spec:
            options.append('--enable-debug')
        else:
            options.append('--disable-debug')

        # FIXME it seems that with cgm and shared, we have a link
        #   issue  in tools/geometry
        if '+shared' in spec:
            options.append('--enable-shared')
        else:
            options.append('--disable-shared')

        if '~fortran' in spec:
            options.append('--disable-fortran')
        else:
            options.append('--enable-fortran')

        return options

    # FIXME Run the install phase with -j 1.  There seems to be a problem with
    # parallel installations of examples
    def install(self, spec, prefix):
        make('install', parallel=False)
