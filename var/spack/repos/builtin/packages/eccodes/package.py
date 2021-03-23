# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
from spack import *


class Eccodes(CMakePackage):
    """ecCodes is a package developed by ECMWF for processing meteorological
    data in GRIB (1/2), BUFR (3/4) and GTS header formats."""

    homepage = 'https://software.ecmwf.int/wiki/display/ECC/ecCodes+Home'
    url = 'https://software.ecmwf.int/wiki/download/attachments/45757960/eccodes-2.2.0-Source.tar.gz?api=v2'
    list_url = 'https://software.ecmwf.int/wiki/display/ECC/Releases'

    maintainers = ['skosukhin']

    version('2.20.0', sha256='207a3d7966e75d85920569b55a19824673e8cd0b50db4c4dac2d3d52eacd7985')
    version('2.19.1', sha256='9964bed5058e873d514bd4920951122a95963128b12f55aa199d9afbafdd5d4b')
    version('2.18.0', sha256='d88943df0f246843a1a062796edbf709ef911de7269648eef864be259e9704e3')
    version('2.13.0', sha256='c5ce1183b5257929fc1f1c8496239e52650707cfab24f4e0e1f1a471135b8272')
    version('2.5.0', sha256='18ab44bc444168fd324d07f7dea94f89e056f5c5cd973e818c8783f952702e4e')
    version('2.2.0', sha256='1a4112196497b8421480e2a0a1164071221e467853486577c4f07627a702f4c3')

    variant('netcdf', default=False,
            description='Enable GRIB to NetCDF conversion tool')
    variant('jp2k', default='openjpeg', values=('openjpeg', 'jasper', 'none'),
            description='Specify JPEG2000 decoding/encoding backend')
    variant('png', default=False,
            description='Enable PNG support for decoding/encoding')
    variant('aec', default=False,
            description='Enable Adaptive Entropy Coding for decoding/encoding')
    variant('pthreads', default=False,
            description='Enable POSIX threads')
    variant('openmp', default=False,
            description='Enable OpenMP threads')
    variant('memfs', default=False,
            description='Enable memory based access to definitions/samples')
    variant('python', default=False,
            description='Enable the Python 2 interface')
    variant('fortran', default=False, description='Enable the Fortran support')

    depends_on('netcdf-c', when='+netcdf')
    # Cannot be built with openjpeg@2.0.x.
    depends_on('openjpeg@1.5.0:1.5.999,2.1.0:2.3.999', when='jp2k=openjpeg')
    # Additional constraint for older versions.
    depends_on('openjpeg@:2.1.999', when='@:2.16 jp2k=openjpeg')
    depends_on('jasper', when='jp2k=jasper')
    depends_on('libpng', when='+png')
    depends_on('libaec', when='+aec')
    # Can be built with Python 2 or Python 3.
    depends_on('python', when='+memfs', type='build')
    # The interface is available only for Python 2.
    # Python 3 interface is available as a separate packages:
    # https://confluence.ecmwf.int/display/ECC/Python+3+interface+for+ecCodes
    depends_on('python@2.6:2.999', when='+python',
               type=('build', 'link', 'run'))
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    extends('python', when='+python')

    depends_on('cmake@3.6:', type='build')
    depends_on('cmake@3.12:', when='@2.19:', type='build')
    conflicts('+openmp', when='+pthreads',
              msg='Cannot enable both POSIX threads and OMP')

    # Enforce linking against the specified JPEG2000 backend, see also
    # https://github.com/ecmwf/eccodes/commit/2c10828495900ff3d80d1e570fe96c1df16d97fb
    patch('openjpeg_jasper.patch', when='@:2.16')

    # CMAKE_INSTALL_RPATH must be a semicolon-separated list.
    patch('cmake_install_rpath.patch', when='@:2.10')

    @run_before('cmake')
    def check_fortran(self):
        if '+fortran' in self.spec and self.compiler.fc is None:
            raise InstallError(
                'Fortran interface requires a Fortran compiler!')

    def cmake_args(self):
        var_opt_list = [('+pthreads', 'ECCODES_THREADS'),
                        ('+openmp', 'ECCODES_OMP_THREADS'),
                        ('+memfs', 'MEMFS'),
                        ('+python', 'PYTHON'),
                        ('+fortran', 'FORTRAN')]

        args = ['-DENABLE_%s=%s' % (opt, 'ON' if var in self.spec else 'OFF')
                for var, opt in var_opt_list]

        args.extend(
            ['-DENABLE_%s=%s' % (opt, 'ON' if self.run_tests else 'OFF')
             for opt in ['TESTS',
                         # Examples are not installed and are
                         # just part of the test suite.
                         'EXAMPLES']])

        # Unconditionally disable the extended regression testing,
        # which requires data downloads.
        args.append('-DENABLE_EXTRA_TESTS=OFF')

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

        jp2k = self.spec.variants['jp2k'].value
        args.append('-DENABLE_JPG=' +
                    ('OFF' if jp2k == 'none' else 'ON'))
        args.append('-DENABLE_JPG_LIBJASPER=' +
                    ('ON' if jp2k == 'jasper' else 'OFF'))
        args.append('-DENABLE_JPG_LIBOPENJPEG=' +
                    ('ON' if jp2k == 'openjpeg' else 'OFF'))

        if jp2k == 'openjpeg':
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

    def check(self):
        # https://confluence.ecmwf.int/display/ECC/ecCodes+installation
        with working_dir(self.build_directory):
            ctest()
