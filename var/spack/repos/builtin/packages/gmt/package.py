# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gmt(Package):
    """GMT (Generic Mapping Tools) is an open source collection of about 80
    command-line tools for manipulating geographic and Cartesian data sets
    (including filtering, trend fitting, gridding, projecting, etc.) and
    producing PostScript illustrations ranging from simple x-y plots via
    contour maps to artificially illuminated surfaces and 3D perspective views.
    """

    homepage = "https://www.generic-mapping-tools.org/"
    url      = "https://github.com/GenericMappingTools/gmt/archive/6.1.0.tar.gz"
    git      = "https://github.com/GenericMappingTools/gmt.git"

    maintainers = ['adamjstewart']

    version('master', branch='master')
    version('6.1.0', sha256='f76ad7f444d407dfd7e5762644eec3a719c6aeb06d877bf746fe51abd79b1a9e')
    version('6.0.0', sha256='7a733e670f01d99f8fc0da51a4337320d764c06a68746621f83ccf2e3453bcb7')
    version('5.4.4', sha256='b593dfb101e6507c467619f3d2190a9f78b09d49fe2c27799750b8c4c0cd2da0')
    version('4.5.9', sha256='9b13be96ccf4bbd38c14359c05dfa7eeeb4b5f06d6f4be9c33d6c3ea276afc86',
            url='ftp://ftp.soest.hawaii.edu/gmt/legacy/gmt-4.5.9.tar.bz2')

    variant('ghostscript', default=False, description='Ability to convert PostScript plots to PDF and rasters')
    variant('gdal', default=False, description='Ability to read and write numerous grid and image formats')
    variant('pcre', default=False, description='Regular expression support')
    variant('fftw', default=False, description='Fast FFTs')
    variant('glib', default=False, description='GTHREAD support')
    variant('lapack', default=False, description='Fast matrix inversion')
    variant('blas', default=False, description='Fast matrix multiplications')
    variant('graphicsmagick', default=False, description='Convert images to animated GIFs')
    variant('ffmpeg', default=False, description='Convert images to videos')
    variant('docs', default=False, description='Build manpage and HTML documentation')

    # https://github.com/GenericMappingTools/gmt/blob/master/BUILDING.md
    # https://github.com/GenericMappingTools/gmt/blob/master/MAINTENANCE.md

    # Required dependencies
    depends_on('cmake@2.8.12:', type='build', when='@5:')
    depends_on('netcdf-c@4:')
    depends_on('curl', when='@5.4:')

    # Optional dependencies
    depends_on('ghostscript', when='+ghostscript')
    depends_on('gdal', when='+gdal')
    depends_on('pcre', when='+pcre')
    depends_on('fftw', when='+fftw')
    depends_on('glib', when='+glib')
    depends_on('lapack', when='+lapack')
    depends_on('blas', when='+blas')
    depends_on('graphicsmagick', when='+graphicsmagick')
    depends_on('ffmpeg', when='+ffmpeg')
    depends_on('py-sphinx@1.4:', when='+docs', type='build')

    depends_on('graphicsmagick', type='test')

    # https://github.com/GenericMappingTools/gmt/pull/3603
    patch('regexp.patch', when='@6.1.0')
    patch('type.patch', when='@4.5.9')

    executables = ['^gmt-config$']

    @classmethod
    def determine_version(cls, exe):
        return Executable(exe)('--version', output=str, error=str).rstrip()

    @when('@5:')
    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            args = std_cmake_args

            args.extend([
                '-DNETCDF_CONFIG={0}'.format(
                    spec['netcdf-c'].prefix.bin.join('nc-config')),
                '-DNETCDF_INCLUDE_DIR={0}'.format(
                    spec['netcdf-c'].headers.directories[0]),
                '-DNETCDF_LIBRARY={0}'.format(
                    spec['netcdf-c'].libs[0])
            ])

            # If these options aren't explicitly disabled,
            # CMake will search OS for dependencies
            if '+ghostscript' in spec:
                args.append('-DGS={0}'.format(
                    spec['ghostscript'].prefix.bin.gs))
            else:
                args.append('-DGS=')

            if '+gdal' in spec:
                args.extend([
                    '-DGDAL_TRANSLATE={0}'.format(
                        spec['gdal'].prefix.bin.gdal_translate),
                    '-DOGR2OGR={0}'.format(
                        spec['gdal'].prefix.bin.ogr2ogr),
                ])
            else:
                args.extend(['-DGDAL_TRANSLATE=', '-DOGR2OGR='])

            if 'graphicsmagick' in spec:
                args.extend([
                    '-DGM={0}'.format(
                        spec['graphicsmagick'].prefix.bin.gm),
                    '-DGRAPHICSMAGICK={0}'.format(
                        spec['graphicsmagick'].prefix.bin.gm),
                ])
            else:
                args.extend(['-DGM=', '-DGRAPHICSMAGICK='])

            if '+ffmpeg' in spec:
                args.append('-DFFMPEG={0}'.format(
                    spec['ffmpeg'].prefix.bin.ffmpeg))
            else:
                args.append('-DFFMPEG=')

            cmake('..', *args)

            make()
            if self.run_tests:
                make('check')
            make('install')

    @when('@:4')
    def install(self, spec, prefix):
        args = [
            '--prefix={0}'.format(prefix),
            '--enable-netcdf={0}'.format(spec['netcdf-c'].prefix),
            '--enable-shared',
            '--without-x'
        ]

        if '+gdal' in spec:
            args.append('--enable-gdal')
        else:
            args.append('--disable-gdal')

        configure(*args)

        # Building in parallel results in dozens of errors like:
        # *** No rule to make target `../libgmtps.so', needed by `pssegyz'.
        make(parallel=False)

        # Installing in parallel results in dozens of errors like:
        # /usr/bin/install: cannot create directory '...': File exists
        make('install', parallel=False)
