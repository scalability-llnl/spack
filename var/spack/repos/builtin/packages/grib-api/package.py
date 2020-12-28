# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GribApi(CMakePackage):
    """The ECMWF GRIB API is an application program interface accessible from
       C, FORTRAN and Python programs developed for encoding and decoding WMO
       FM-92 GRIB edition 1 and edition 2 messages."""

    homepage = 'https://software.ecmwf.int/wiki/display/GRIB/Home'
    url = 'https://software.ecmwf.int/wiki/download/attachments/3473437/grib_api-1.17.0-Source.tar.gz?api=v2'
    list_url = 'https://software.ecmwf.int/wiki/display/GRIB/Releases'

    maintainers = ['skosukhin']

    version('1.24.0', sha256='6b0d443cb0802c5de652e5816c5b88734cb3ead454eb932c5ec12ef8d4f77bcd')
    version('1.21.0', sha256='50c2b58303ab578c55735e6c21c72ffc24f82a5bf52565550f54d49cb60e8a90')
    version('1.17.0', sha256='55cbb4fdcb4ee1be6a27cece9ae7e26070beb8ab6cb7e77773db3fb0d4272462')
    version('1.16.0', sha256='0068ca4149a9f991d4c86a813ac73b4e2299c6a3fd53aba9e6ab276ef6f0ff9a')

    variant('netcdf', default=False,
            description='Enable netcdf encoding/decoding using netcdf library')
    variant('jp2k', default='openjpeg', values=('openjpeg', 'jasper', 'none'),
            description='Specify JPEG2000 decoding/encoding backend')
    variant('png', default=False,
            description='Enable png for decoding/encoding')
    variant('aec', default=False,
            description='Enable Adaptive Entropy Coding for decoding/encoding')
    variant('pthreads', default=False,
            description='Enable POSIX threads')
    variant('openmp', default=False,
            description='Enable OpenMP threads')
    variant('python', default=False,
            description='Enable the Python interface')
    variant('numpy', default=False,
            description='Enable numpy support in the Python interface')
    variant('fortran', default=False, description='Enable the Fortran support')
    variant('examples', default=True,
            description='Build the examples (part of the full test suite)')
    variant('test', default=True, description='Enable the tests')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo', 'Production'))

    # The building script tries to find an optional package valgrind when
    # tests are enabled but the testing scripts don't use it.
    # depends_on('valgrind', type='test', when='+test')

    depends_on('netcdf-c', when='+netcdf')
    depends_on('openjpeg@1.5.0:1.5.999', when='jp2k=openjpeg')
    depends_on('jasper', when='jp2k=jasper')
    depends_on('libpng', when='+png')
    depends_on('libaec', when='+aec')
    depends_on('python@2.5:2.999', when='+python',
               type=('build', 'link', 'run'))
    depends_on('py-numpy', when='+python+numpy', type=('build', 'run'))
    extends('python', when='+python')

    conflicts('+openmp', when='+pthreads',
              msg='Cannot enable both POSIX threads and OMP')
    conflicts('+numpy', when='~python',
              msg='Numpy variant is valid only when the Python interface is '
                  'enabled')

    # The following enforces linking against the specified JPEG2000 backend.
    patch('enable_only_openjpeg.patch', when='jp2k=openjpeg')
    patch('enable_only_jasper.patch', when='jp2k=jasper')

    # Disable NumPy even if it's available.
    patch('disable_numpy.patch', when='+python~numpy')

    # CMAKE_INSTALL_RPATH must be a semicolon-separated list.
    patch('cmake_install_rpath.patch')

    @run_before('cmake')
    def check_fortran(self):
        if '+fortran' in self.spec and self.compiler.fc is None:
            raise InstallError(
                'Fortran interface requires a Fortran compiler!')

    def cmake_args(self):
        var_opt_list = [('+pthreads', 'GRIB_THREADS'),
                        ('+openmp', 'GRIB_OMP_THREADS'),
                        ('+python', 'PYTHON'),
                        ('+fortran', 'FORTRAN'),
                        ('+examples', 'EXAMPLES'),
                        ('+test', 'TESTS')]

        args = ['-DENABLE_%s=%s' % (opt, 'ON' if var in self.spec else 'OFF')
                for var, opt in var_opt_list]

        if '+netcdf' in self.spec:
            args.extend(['-DENABLE_NETCDF=ON',
                         # Prevent overriding by environment variable
                         # HDF5_ROOT.
                         '-DHDF5_ROOT=' + self.spec['hdf5'].prefix,
                         # Prevent possible overriding by environment variables
                         # NETCDF_ROOT, NETCDF_DIR, and NETCDF_PATH.
                         '-DNETCDF_PATH=' + self.spec['netcdf-c'].prefix])
        else:
            args.append('-DENABLE_NETCDF=OFF')

        if self.spec.variants['jp2k'].value == 'none':
            args.append('-DENABLE_JPG=OFF')
        else:
            args.append('-DENABLE_JPG=ON')

        if self.spec.variants['jp2k'].value == 'openjpeg':
            args.append('-DOPENJPEG_PATH=' + self.spec['openjpeg'].prefix)

        if '+png' in self.spec:
            args.extend(['-DENABLE_PNG=ON',
                         '-DZLIB_ROOT=' + self.spec['zlib'].prefix])
        else:
            args.append('-DENABLE_PNG=OFF')

        if '+aec' in self.spec:
            args.extend(['-DENABLE_AEC=ON',
                         # Prevent overriding by environment variables
                         # AEC_DIR and AEC_PATH.
                         '-DAEC_DIR=' + self.spec['libaec'].prefix])
        else:
            args.append('-DENABLE_AEC=OFF')

        if '^python' in self.spec:
            args.append('-DPYTHON_EXECUTABLE:FILEPATH=' + python.path)

        return args
