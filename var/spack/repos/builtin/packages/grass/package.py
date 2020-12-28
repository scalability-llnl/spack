# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Grass(AutotoolsPackage):
    """GRASS GIS (Geographic Resources Analysis Support System), is a free
       and open source Geographic Information System (GIS) software suite
       used for geospatial data management and analysis, image processing,
       graphics and maps production, spatial modeling, and visualization."""

    homepage = "https://grass.osgeo.org"
    url      = "https://grass.osgeo.org/grass78/source/grass-7.8.2.tar.gz"
    list_url = "https://grass.osgeo.org/download/software/sources/"
    git      = "https://github.com/OSGeo/grass.git"

    maintainers = ['adamjstewart']

    version('master', branch='master')
    version('7.8.2', sha256='33576f7078f805b39ca20c2fa416ac79c64260c0581072a6dc7d813f53aa9abb')
    version('7.8.1', sha256='6ae578fd67afcce7abec4ba4505dcc55b3d2dfe0ca46b99d966cb148c654abb3')
    version('7.8.0', sha256='4b1192294e959ffd962282344e4ff325c4472f73abe605e246a1da3beda7ccfa')
    version('7.6.1', sha256='9e25c99cafd16ed8f5e2dca75b5a10dc2af0568dbedf3fc39f1c5a0a9c840b0b')
    version('7.4.4', sha256='96a39e273103f7375a670eba94fa3e5dad2819c5c5664c9aee8f145882a94e8c')
    version('7.4.3', sha256='004e65693ee97fd4d5dc7ad244e3286a115dccd88964d04be61c07db6574b399')
    version('7.4.2', sha256='18eb19bc0aa4cd7be3f30f79ac83f9d0a29c63657f4c1b05bf4c5d5d57a8f46d')
    version('7.4.1', sha256='560b8669caaafa9e8dbd4bbf2b4b4bbab7dca1cc46ee828eaf26c744fe0635fc')
    version('7.4.0', sha256='cb6fa188e030a3a447fc5451fbe0ecbeb4069ee2fd1bf52ed8e40e9b89e293cc')

    variant('cxx',       default=True,  description='Support C++ functionality')
    variant('tiff',      default=False, description='Support TIFF functionality')
    variant('png',       default=False, description='Support PNG functionality')
    variant('postgres',  default=False, description='Support PostgreSQL functionality')
    variant('mysql',     default=False, description='Support MySQL functionality')
    variant('sqlite',    default=False, description='Support SQLite functionality')
    variant('opengl',    default=False, description='Support OpenGL functionality')
    variant('odbc',      default=False, description='Support ODBC functionality')
    variant('fftw',      default=False, description='Support FFTW functionality')
    variant('blas',      default=False, description='Support BLAS functionality')
    variant('lapack',    default=False, description='Support LAPACK functionality')
    variant('cairo',     default=False, description='Support Cairo functionality')
    variant('freetype',  default=False, description='Support FreeType functionality')
    variant('readline',  default=False, description='Support Readline functionality')
    variant('regex',     default=False, description='Support regex functionality')
    variant('pthread',   default=False, description='Support POSIX threads functionality')
    variant('openmp',    default=False, description='Support OpenMP functionality')
    variant('opencl',    default=False, description='Support OpenCL functionality')
    variant('bzlib',     default=False, description='Support BZIP2 functionality')
    variant('zstd',      default=False, description='Support Zstandard functionality')
    variant('gdal',      default=True,  description='Enable GDAL/OGR support')
    variant('liblas',    default=False, description='Enable libLAS support')
    variant('wxwidgets', default=False, description='Enable wxWidgets support')
    variant('netcdf',    default=False, description='Enable NetCDF support')
    variant('geos',      default=False, description='Enable GEOS support')
    variant('x',         default=False, description='Use the X Window System')

    # http://htmlpreview.github.io/?https://github.com/OSGeo/grass/blob/master/REQUIREMENTS.html
    # General requirements
    depends_on('gmake@3.81:', type='build')
    depends_on('iconv')
    depends_on('zlib')
    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('proj')
    depends_on('proj@:4', when='@:7.5')
    # GRASS 7.8.0 was supposed to support PROJ 6, but it still checks for
    # share/proj/epsg, which was removed in PROJ 6
    depends_on('proj@:5', when='@:7.8.0')
    # PROJ6 support released in GRASS 7.8.1
    # https://courses.neteler.org/grass-gis-7-8-1-released-with-proj-6-and-gdal-3-support/
    depends_on('proj@6:', when='@7.8.1:')
    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('python@2.7:2.8', when='@:7.6', type=('build', 'run'))
    depends_on('py-six', when='@7.8:', type=('build', 'run'))

    # Optional packages
    depends_on('libtiff', when='+tiff')
    depends_on('libpng', when='+png')
    depends_on('postgresql', when='+postgres')
    depends_on('mariadb', when='+mysql')
    depends_on('sqlite', when='+sqlite')
    depends_on('gl', when='+opengl')
    depends_on('unixodbc', when='+odbc')
    depends_on('fftw', when='+fftw')
    depends_on('blas', when='+blas')
    depends_on('lapack', when='+lapack')
    depends_on('cairo@1.5.8:', when='+cairo')
    depends_on('freetype', when='+freetype')
    depends_on('readline', when='+readline')
    depends_on('opencl', when='+opencl')
    depends_on('bzip2', when='+bzlib')
    depends_on('zstd', when='+zstd')
    depends_on('gdal', when='+gdal')  # required?
    depends_on('liblas', when='+liblas')
    depends_on('wxwidgets', when='+wxwidgets')
    depends_on('py-wxpython@2.8.10.1:', when='+wxwidgets', type=('build', 'run'))
    depends_on('netcdf-c', when='+netcdf')
    depends_on('geos', when='+geos')
    depends_on('libx11', when='+x')

    def url_for_version(self, version):
        url = "https://grass.osgeo.org/grass{0}/source/grass-{1}.tar.gz"
        return url.format(version.up_to(2).joined, version)

    # https://grasswiki.osgeo.org/wiki/Compile_and_Install
    def configure_args(self):
        spec = self.spec

        args = [
            '--without-nls',
            # TODO: add packages for these optional dependencies
            '--without-opendwg',
            '--without-pdal',
            '--with-proj-share={0}'.format(spec['proj'].prefix.share.proj),
        ]

        if '+cxx' in spec:
            args.append('--with-cxx')
        else:
            args.append('--without-cxx')

        if '+tiff' in spec:
            args.append('--with-tiff')
        else:
            args.append('--without-tiff')

        if '+png' in spec:
            args.append('--with-png')
        else:
            args.append('--without-png')

        if '+postgres' in spec:
            args.append('--with-postgres')
        else:
            args.append('--without-postgres')

        if '+mysql' in spec:
            args.append('--with-mysql')
        else:
            args.append('--without-mysql')

        if '+sqlite' in spec:
            args.append('--with-sqlite')
        else:
            args.append('--without-sqlite')

        if '+opengl' in spec:
            args.append('--with-opengl')
        else:
            args.append('--without-opengl')

        if '+odbc' in spec:
            args.append('--with-odbc')
        else:
            args.append('--without-odbc')

        if '+fftw' in spec:
            args.append('--with-fftw')
        else:
            args.append('--without-fftw')

        if '+blas' in spec:
            args.append('--with-blas')
        else:
            args.append('--without-blas')

        if '+lapack' in spec:
            args.append('--with-lapack')
        else:
            args.append('--without-lapack')

        if '+cairo' in spec:
            args.append('--with-cairo')
        else:
            args.append('--without-cairo')

        if '+freetype' in spec:
            args.append('--with-freetype')
        else:
            args.append('--without-freetype')

        if '+readline' in spec:
            args.append('--with-readline')
        else:
            args.append('--without-readline')

        if '+regex' in spec:
            args.append('--with-regex')
        else:
            args.append('--without-regex')

        if '+pthread' in spec:
            args.append('--with-pthread')
        else:
            args.append('--without-pthread')

        if '+openmp' in spec:
            args.append('--with-openmp')
        else:
            args.append('--without-openmp')

        if '+opencl' in spec:
            args.append('--with-opencl')
        else:
            args.append('--without-opencl')

        if '+bzlib' in spec:
            args.append('--with-bzlib')
        else:
            args.append('--without-bzlib')

        if '+zstd' in spec:
            args.append('--with-zstd')
        else:
            args.append('--without-zstd')

        if '+gdal' in spec:
            args.append('--with-gdal={0}/gdal-config'.format(
                spec['gdal'].prefix.bin))
        else:
            args.append('--without-gdal')

        if '+liblas' in spec:
            args.append('--with-liblas={0}/liblas-config'.format(
                spec['liblas'].prefix.bin))
        else:
            args.append('--without-liblas')

        if '+wxwidgets' in spec:
            args.append('--with-wxwidgets={0}/wx-config'.format(
                spec['wxwidgets'].prefix.bin))
        else:
            args.append('--without-wxwidgets')

        if '+netcdf' in spec:
            args.append('--with-netcdf={0}/bin/nc-config'.format(
                spec['netcdf-c'].prefix))
        else:
            args.append('--without-netcdf')

        if '+geos' in spec:
            args.append('--with-geos={0}/bin/geos-config'.format(
                spec['geos'].prefix))
        else:
            args.append('--without-geos')

        if '+x' in spec:
            args.append('--with-x')
        else:
            args.append('--without-x')

        return args

    # see issue: https://github.com/spack/spack/issues/11325
    # 'Platform.make' is created after configure step
    # hence invoke the following function afterwards
    @run_after('configure')
    def fix_iconv_linking(self):
        if self.spec['iconv'].name != 'libiconv':
            return

        makefile = FileFilter('include/Make/Platform.make')
        makefile.filter(r'^ICONVLIB\s*=.*', 'ICONVLIB = -liconv')
