# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from collections import defaultdict

from spack import *
from spack.util.environment import is_system_path


class Cdo(AutotoolsPackage):
    """CDO is a collection of command line Operators to manipulate and analyse
       Climate and NWP model Data.
    """

    homepage = 'https://code.mpimet.mpg.de/projects/cdo'
    url = 'https://code.mpimet.mpg.de/attachments/download/12760/cdo-1.7.2.tar.gz'
    list_url = 'https://code.mpimet.mpg.de/projects/cdo/files'

    maintainers = ['skosukhin', 'Try2Code']

    version('1.9.10', sha256='cc39c89bbb481d7b3945a06c56a8492047235f46ac363c4f0d980fccdde6677e', url='https://code.mpimet.mpg.de/attachments/download/24638/cdo-1.9.10.tar.gz')
    version('1.9.9', sha256='959b5b58f495d521a7fd1daa84644888ec87d6a0df43f22ad950d17aee5ba98d', url='https://code.mpimet.mpg.de/attachments/download/23323/cdo-1.9.9.tar.gz')
    version('1.9.8', sha256='f2660ac6f8bf3fa071cf2a3a196b3ec75ad007deb3a782455e80f28680c5252a', url='https://code.mpimet.mpg.de/attachments/download/20826/cdo-1.9.8.tar.gz')
    version('1.9.7.1', sha256='3771952e065bcf935d43e492707370ed2a0ecb59a06bea24f9ab69d77943962c', url='https://code.mpimet.mpg.de/attachments/download/20124/cdo-1.9.7.1.tar.gz')
    version('1.9.6', sha256='b31474c94548d21393758caa33f35cf7f423d5dfc84562ad80a2bdcb725b5585', url='https://code.mpimet.mpg.de/attachments/download/19299/cdo-1.9.6.tar.gz')
    version('1.9.5', sha256='48ed65cc5b436753c8e7f9eadd8aa97376698ce230ceafed2a4350a5b1a27148', url='https://code.mpimet.mpg.de/attachments/download/18264/cdo-1.9.5.tar.gz')
    version('1.9.4', sha256='3d1c0fd3f7d38c5d3d88139ca1546c9d24e1b1ff752a794a4194dfe624695def', url='https://code.mpimet.mpg.de/attachments/download/17374/cdo-1.9.4.tar.gz')
    version('1.9.3', sha256='e83a3de7b402600c0d9a5df18073d36d133ff9719d3c561a0efa90f9c1599f3f', url='https://code.mpimet.mpg.de/attachments/download/16435/cdo-1.9.3.tar.gz')
    version('1.9.2', sha256='d1c5092167034a48e4b8ada24cf78a1d4b84e364ffbb08b9ca70d13f428f300c', url='https://code.mpimet.mpg.de/attachments/download/16035/cdo-1.9.2.tar.gz')
    version('1.9.1', sha256='33cba3cfcc27e5896769143c5f8e2f300ca14c7a40d1f19ffd1ed24b49ea3d55', url='https://code.mpimet.mpg.de/attachments/download/15653/cdo-1.9.1.tar.gz')
    version('1.9.0', sha256='df367f8c3abf4ab085bcfc61e0205b28a5ecc69b7b83ba398b4d3c874dd69008', url='https://code.mpimet.mpg.de/attachments/download/15187/cdo-1.9.0.tar.gz')
    version('1.8.2', sha256='6ca6c1263af2237737728ac937a275f8aa27680507636a6b6320f347c69a369a', url='https://code.mpimet.mpg.de/attachments/download/14686/cdo-1.8.2.tar.gz')
    version('1.7.2', sha256='4c43eba7a95f77457bfe0d30fb82382b3b5f2b0cf90aca6f0f0a008f6cc7e697', url='https://code.mpimet.mpg.de/attachments/download/12760/cdo-1.7.2.tar.gz')

    variant('netcdf', default=True, description='Enable NetCDF support')
    variant('grib2', default='eccodes', values=('eccodes', 'grib-api', 'none'),
            description='Specify GRIB2 backend')
    variant('external-grib1', default=False,
            description='Ignore the built-in support and use the external '
                        'GRIB2 backend for GRIB1 files')
    variant('szip', default=True,
            description='Enable szip compression for GRIB1')
    variant('hdf5', default=True, description='Enable HDF5 support')

    variant('udunits2', default=True, description='Enable UDUNITS2 support')
    variant('libxml2', default=True, description='Enable libxml2 support')
    variant('proj', default=True,
            description='Enable PROJ library for cartographic projections')
    variant('curl', default=False, description='Enable curl support')
    variant('fftw3', default=True, description='Enable support for fftw3')
    variant('magics', default=False,
            description='Enable Magics library support')
    variant('openmp', default=True, description='Enable OpenMP support')

    depends_on('pkgconfig', type='build')

    depends_on('netcdf-c', when='+netcdf')
    # The internal library of CDO implicitly links to hdf5.
    # We also need the backend of netcdf to be thread safe.
    depends_on('hdf5+threadsafe', when='+netcdf')

    depends_on('grib-api', when='grib2=grib-api')
    depends_on('eccodes', when='grib2=eccodes')

    depends_on('szip', when='+szip')

    depends_on('hdf5+threadsafe', when='+hdf5')

    depends_on('udunits', when='+udunits2')
    depends_on('libxml2', when='+libxml2')
    depends_on('proj@:5', when='@:1.9.6+proj')
    depends_on('proj@:7', when='@1.9.7+proj')
    depends_on('proj@5:', when='@1.9.8:+proj')
    depends_on('curl', when='+curl')
    depends_on('fftw-api@3:', when='+fftw3')
    depends_on('magics', when='+magics')
    depends_on('uuid')

    conflicts('+szip', when='+external-grib1 grib2=none',
              msg='The configuration does not support GRIB1')
    conflicts('%gcc@9:', when='@:1.9.6',
              msg='GCC 9 changed OpenMP data sharing behavior')

    def configure_args(self):
        config_args = []

        flags = defaultdict(list)

        def yes_or_prefix(spec_name):
            prefix = self.spec[spec_name].prefix
            return 'yes' if is_system_path(prefix) else prefix

        if '+netcdf' in self.spec:
            config_args.append('--with-netcdf=' + yes_or_prefix('netcdf-c'))
            # We need to make sure that the libtool script of libcdi - the
            # internal library of CDO - finds the correct version of hdf5.
            # Note that the argument of --with-hdf5 is not passed to the
            # configure script of libcdi, therefore we have to provide
            # additional flags regardless of whether hdf5 support is enabled.
            hdf5_spec = self.spec['hdf5']
            if not is_system_path(hdf5_spec.prefix):
                flags['LDFLAGS'].append(self.spec['hdf5'].libs.search_flags)
        else:
            config_args.append('--without-netcdf')

        if self.spec.variants['grib2'].value == 'eccodes':
            if self.spec.satisfies('@1.9:'):
                config_args.append('--with-eccodes=' + yes_or_prefix('eccodes'))
                config_args.append('--without-grib_api')
            else:
                config_args.append('--with-grib_api=yes')
                eccodes_spec = self.spec['eccodes']
                eccodes_libs = eccodes_spec.libs
                flags['LIBS'].append(eccodes_libs.link_flags)
                if not is_system_path(eccodes_spec.prefix):
                    flags['LDFLAGS'].append(eccodes_libs.search_flags)
        elif self.spec.variants['grib2'].value == 'grib-api':
            config_args.append('--with-grib_api=' + yes_or_prefix('grib-api'))
            if self.spec.satisfies('@1.9:'):
                config_args.append('--without-eccodes')
        else:
            config_args.append('--without-grib_api')
            if self.spec.satisfies('@1.9:'):
                config_args.append('--without-eccodes')

        if '+external-grib1' in self.spec:
            config_args.append('--disable-cgribex')
        else:
            config_args.append('--enable-cgribex')

        if '+szip' in self.spec:
            config_args.append('--with-szlib=' + yes_or_prefix('szip'))
        else:
            config_args.append('--without-szlib')

        config_args += self.with_or_without('hdf5',
                                            activation_value=yes_or_prefix)

        config_args += self.with_or_without(
            'udunits2',
            activation_value=lambda x: yes_or_prefix('udunits'))

        if '+libxml2' in self.spec:
            libxml2_spec = self.spec['libxml2']
            if is_system_path(libxml2_spec.prefix):
                config_args.append('--with-libxml2=yes')
                # Spack does not inject the header search flag in this case,
                # which is still required, unless libxml2 is installed to '/usr'
                # (handled by the configure script of CDO).
                if libxml2_spec.prefix != '/usr':
                    flags['CPPFLAGS'].append(libxml2_spec.headers.include_flags)
            else:
                config_args.append('--with-libxml2=' + libxml2_spec.prefix)
        else:
            config_args.append('--without-libxml2')

        config_args += self.with_or_without('proj',
                                            activation_value=yes_or_prefix)

        config_args += self.with_or_without('curl',
                                            activation_value=yes_or_prefix)

        config_args += self.with_or_without('magics',
                                            activation_value=yes_or_prefix)

        config_args += self.with_or_without('fftw3')

        config_args += self.enable_or_disable('openmp')

        # Starting version 1.9.0 CDO is a C++ program but it uses the C
        # interface of HDF5 without the parallel features. To avoid
        # unnecessary dependencies on mpi's cxx library, we need to set the
        # following flags. This works for OpenMPI, MPICH, MVAPICH, Intel MPI,
        # IBM Spectrum MPI, bullx MPI, and Cray MPI.
        if self.spec.satisfies('@1.9:+hdf5^hdf5+mpi'):
            flags['CPPFLAGS'].append('-DOMPI_SKIP_MPICXX -DMPICH_SKIP_MPICXX')

        config_args.extend(['{0}={1}'.format(var, ' '.join(val))
                            for var, val in flags.items()])

        return config_args
