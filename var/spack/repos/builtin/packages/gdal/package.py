# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class Gdal(AutotoolsPackage):
    """GDAL (Geospatial Data Abstraction Library) is a translator library for
    raster and vector geospatial data formats that is released under an X/MIT
    style Open Source license by the Open Source Geospatial Foundation. As a
    library, it presents a single raster abstract data model and vector
    abstract data model to the calling application for all supported formats.
    It also comes with a variety of useful command line utilities for data
    translation and processing.
    """

    homepage   = "https://www.gdal.org/"
    url        = "https://download.osgeo.org/gdal/3.1.4/gdal-3.1.4.tar.xz"
    list_url   = "https://download.osgeo.org/gdal/"
    list_depth = 1

    maintainers = ['adamjstewart']

    import_modules = [
        'osgeo', 'osgeo.gdal', 'osgeo.ogr', 'osgeo.osr',
        'osgeo.gdal_array', 'osgeo.gdalconst'
    ]

    version('3.1.4',  sha256='7b82486f71c71cec61f9b237116212ce18ef6b90f068cbbf9f7de4fc50b576a8')
    version('3.1.3',  sha256='161cf55371a143826f1d76ce566db1f0a666496eeb4371aed78b1642f219d51d')
    version('3.1.2',  sha256='767c8d0dfa20ba3283de05d23a1d1c03a7e805d0ce2936beaff0bb7d11450641')
    version('3.1.1',  sha256='97154a606339a6c1d87c80fb354d7456fe49828b2ef9a3bc9ed91771a03d2a04')
    version('3.1.0',  sha256='e754a22242ccbec731aacdb2333b567d4c95b9b02d3ba1ea12f70508d244fcda')
    version('3.0.4',  sha256='5569a4daa1abcbba47a9d535172fc335194d9214fdb96cd0f139bb57329ae277')
    version('3.0.3',  sha256='e20add5802265159366f197a8bb354899e1693eab8dbba2208de14a457566109')
    version('3.0.2',  sha256='c3765371ce391715c8f28bd6defbc70b57aa43341f6e94605f04fe3c92468983')
    version('3.0.1',  sha256='45b4ae25dbd87282d589eca76481c426f72132d7a599556470d5c38263b09266')
    version('3.0.0',  sha256='ad316fa052d94d9606e90b20a514b92b2dd64e3142dfdbd8f10981a5fcd5c43e')
    version('2.4.4',  sha256='a383bd3cf555d6e1169666b01b5b3025b2722ed39e834f1b65090f604405dcd8')
    version('2.4.3',  sha256='d52dc3e0cff3af3e898d887c4151442989f416e839948e73f0994f0224bbff60')
    version('2.4.2',  sha256='dcc132e469c5eb76fa4aaff238d32e45a5d947dc5b6c801a123b70045b618e0c')
    version('2.4.1',  sha256='fd51b4900b2fc49b98d8714f55fc8a78ebfd07218357f93fb796791115a5a1ad')
    version('2.4.0',  sha256='c3791dcc6d37e59f6efa86e2df2a55a4485237b0a48e330ae08949f0cdf00f27')
    version('2.3.3',  sha256='c3635e41766a648f945d235b922e3c5306e26a2ee5bbd730d2181e242f5f46fe')
    version('2.3.2',  sha256='3f6d78fe8807d1d6afb7bed27394f19467840a82bc36d65e66316fa0aa9d32a4')
    version('2.3.1',  sha256='9c4625c45a3ee7e49a604ef221778983dd9fd8104922a87f20b99d9bedb7725a')
    version('2.3.0',  sha256='6f75e49aa30de140525ccb58688667efe3a2d770576feb7fbc91023b7f552aa2')
    version('2.1.2',  sha256='b597f36bd29a2b4368998ddd32b28c8cdf3c8192237a81b99af83cc17d7fa374')
    version('2.0.2',  sha256='90f838853cc1c07e55893483faa7e923e4b4b1659c6bc9df3538366030a7e622')
    version('1.11.5', sha256='d4fdc3e987b9926545f0a514b4328cd733f2208442f8d03bde630fe1f7eff042')

    variant('libtool',   default=True,  description='Use libtool to build the library')
    variant('libz',      default=True,  description='Include libz support')
    variant('libiconv',  default=False, description='Include libiconv support')
    variant('liblzma',   default=True,  description='Include liblzma support')
    variant('zstd',      default=False, description='Include zstd support')
    variant('pg',        default=False, description='Include PostgreSQL support')
    variant('cfitsio',   default=False, description='Include FITS support')
    variant('png',       default=False, description='Include PNG support')
    variant('jpeg',      default=True,  description='Include JPEG support')
    variant('gif',       default=False, description='Include GIF support')
    variant('sosi',      default=False, description='Include SOSI support')
    variant('hdf4',      default=False, description='Include HDF4 support')
    variant('hdf5',      default=False, description='Include HDF5 support')
    variant('kea',       default=False, description='Include kealib')
    variant('netcdf',    default=False, description='Include netCDF support')
    variant('jasper',    default=False, description='Include JPEG-2000 support via JasPer library')
    variant('openjpeg',  default=False, description='Include JPEG-2000 support via OpenJPEG 2.x library')
    variant('xerces',    default=False, description='Use Xerces-C++ parser')
    variant('expat',     default=False, description='Use Expat XML parser')
    variant('libkml',    default=False, description='Use Google libkml')
    variant('odbc',      default=False, description='Include ODBC support')
    variant('curl',      default=False, description='Include curl')
    variant('xml2',      default=False, description='Include libxml2')
    variant('sqlite3',   default=False, description='Use SQLite 3 library')
    variant('pcre',      default=False, description='Include libpcre support')
    variant('geos',      default=False, description='Include GEOS support')
    variant('qhull',     default=False, description='Include QHull support')
    variant('opencl',    default=False, description='Include OpenCL (GPU) support')
    variant('poppler',   default=False, description='Include poppler (for PDF) support')
    variant('proj',      default=True,  description='Compile with PROJ.x')
    variant('perl',      default=False, description='Enable perl bindings')
    variant('python',    default=False, description='Enable python bindings')
    variant('java',      default=False, description='Include Java support')
    variant('mdb',       default=False, description='Include MDB driver')
    variant('armadillo', default=False, description='Include Armadillo support for faster TPS transform computation')
    variant('cryptopp',  default=False, description='Include cryptopp support')
    variant('crypto',    default=False, description='Include crypto (from openssl) support')
    variant('grib',      default=False, description='Include GRIB support')

    # FIXME: Allow packages to extend multiple packages
    # See https://github.com/spack/spack/issues/987
    # extends('jdk', when='+java')
    # extends('perl', when='+perl')
    extends('python', when='+python')

    # GDAL depends on GNUmake on Unix platforms.
    # https://trac.osgeo.org/gdal/wiki/BuildingOnUnix
    depends_on('gmake', type='build')
    depends_on('pkgconfig@0.25:', type='build')

    # Required dependencies
    depends_on('libtiff@3.6.0:')  # 3.9.0+ needed to pass testsuite
    depends_on('libgeotiff@1.2.1:1.4', when='@:2.4.0')
    depends_on('libgeotiff@1.2.1:1.5', when='@2.4.1:2.4.99')
    depends_on('libgeotiff@1.5:', when='@3.0.0:')
    depends_on('json-c')
    depends_on('json-c@0.12.1', when='@:2.2')

    # Optional dependencies
    depends_on('libtool', type='build', when='+libtool')
    depends_on('zlib', when='+libz')
    depends_on('iconv', when='+libiconv')
    depends_on('xz', when='+liblzma')
    depends_on('zstd', when='+zstd @2.3:')
    depends_on('postgresql', when='+pg')
    depends_on('cfitsio', when='+cfitsio')
    depends_on('libpng', when='+png')
    depends_on('jpeg', when='+jpeg')
    depends_on('giflib', when='+gif')
    depends_on('fyba', when='+sosi')
    depends_on('hdf', when='+hdf4')
    depends_on('hdf5', when='+hdf5')
    depends_on('kealib', when='+kea @2:')
    depends_on('netcdf-c', when='+netcdf')
    depends_on('jasper@1.900.1', patches='uuid.patch', when='+jasper')
    depends_on('openjpeg', when='+openjpeg')
    depends_on('xerces-c', when='+xerces')
    depends_on('expat', when='+expat')
    depends_on('libkml@1.3.0:', when='+libkml')
    depends_on('unixodbc', when='+odbc')
    depends_on('curl@7.10.8:', when='+curl')
    depends_on('libxml2', when='+xml2')
    depends_on('sqlite@3:', when='+sqlite3')
    depends_on('pcre', when='+pcre')
    depends_on('geos', when='+geos')
    depends_on('qhull', when='+qhull @2.1:')
    depends_on('opencl', when='+opencl')
    depends_on('poppler', when='+poppler')
    depends_on('poppler@:0.63', when='@:2.3 +poppler')
    depends_on('poppler@:0.71', when='@:2.4 +poppler')
    depends_on('poppler@0.24:', when='@3: +poppler')
    depends_on('proj@:4', when='+proj @2.3.0:2.3.999')
    depends_on('proj@:5', when='+proj @2.4.0:2.4.999')
    depends_on('proj@:6', when='+proj @2.5:2.999')
    depends_on('proj@6:', when='+proj @3:')
    depends_on('perl', type=('build', 'run'), when='+perl')
    depends_on('python', type=('build', 'link', 'run'), when='+python')
    # swig/python/setup.py
    depends_on('py-setuptools', type='build', when='+python')
    depends_on('py-numpy@1.0.0:', type=('build', 'run'), when='+python')
    depends_on('java@4:8', type=('build', 'link', 'run'), when='+java')
    depends_on('ant', type='build', when='+java')
    depends_on('swig', type='build', when='+java')
    depends_on('jackcess@1.2.0:1.2.999', type='run', when='+mdb')
    depends_on('armadillo', when='+armadillo')
    depends_on('cryptopp', when='+cryptopp @2.1:')
    depends_on('openssl', when='+crypto @2.3:')

    # https://trac.osgeo.org/gdal/wiki/SupportedCompilers
    msg = 'GDAL requires C++11 support'
    conflicts('%gcc@:4.8.0', msg=msg)
    conflicts('%clang@:3.2', msg=msg)
    conflicts('%intel@:12',  msg=msg)
    conflicts('%xl@:13.0',   msg=msg)
    conflicts('%xl_r@:13.0', msg=msg)

    conflicts('+mdb', when='~java', msg='MDB driver requires Java')

    executables = ['^gdal-config$']

    @classmethod
    def determine_version(cls, exe):
        return Executable(exe)('--version', output=str, error=str).rstrip()

    def setup_build_environment(self, env):
        # Needed to install Python bindings to GDAL installation
        # prefix instead of Python installation prefix.
        # See swig/python/GNUmakefile for more details.
        env.set('PREFIX', self.prefix)
        env.set('DESTDIR', '/')

    def setup_run_environment(self, env):
        if '+java' in self.spec:
            class_paths = find(self.prefix, '*.jar')
            classpath = os.pathsep.join(class_paths)
            env.prepend_path('CLASSPATH', classpath)

    def patch(self):
        if '+java platform=darwin' in self.spec:
            filter_file('linux', 'darwin', 'swig/java/java.opt', string=True)

    # https://trac.osgeo.org/gdal/wiki/BuildHints
    def configure_args(self):
        spec = self.spec
        libs = []

        # Required dependencies
        args = [
            # https://trac.osgeo.org/gdal/wiki/TIFF
            '--with-libtiff={0}'.format(spec['libtiff'].prefix),
            '--with-geotiff={0}'.format(spec['libgeotiff'].prefix),
            '--with-libjson-c={0}'.format(spec['json-c'].prefix),
        ]

        # Optional dependencies
        if spec.satisfies('@3:'):
            args.extend([
                '--disable-driver-bsb',
                '--disable-driver-mrf',
            ])

            if '+grib' in spec:
                args.append('--enable-driver-grib')
            else:
                args.append('--disable-driver-grib')
        else:
            args.append('--without-bsb')

            if '+grib' in spec:
                args.append('--with-grib=yes')
            else:
                args.append('--with-grib=no')

            if spec.satisfies('@2.3:'):
                args.append('--with-mrf=no')

        if spec.satisfies('@2.3:'):
            if '+zstd' in spec:
                args.append('--with-zstd={0}'.format(spec['zstd'].prefix))
            else:
                args.append('--with-zstd=no')

            if '+proj' in spec:
                args.append('--with-proj={0}'.format(spec['proj'].prefix))
            else:
                args.append('--with-proj=no')

            if '+crypto' in spec:
                args.append('--with-crypto={0}'.format(spec['openssl'].prefix))
            else:
                args.append('--with-crypto=no')

        if spec.satisfies('@2.1:'):
            if '+qhull' in spec:
                args.append('--with-qhull=yes')
            else:
                args.append('--with-qhull=no')

            if '+cryptopp' in spec:
                args.append('--with-cryptopp={0}'.format(
                    spec['cryptopp'].prefix))
            else:
                args.append('--with-cryptopp=no')

        if spec.satisfies('@2:'):
            if '+kea' in spec:
                args.append('--with-kea={0}'.format(
                    join_path(spec['kealib'].prefix.bin, 'kea-config')))
            else:
                args.append('--with-kea=no')

        if '+libtool' in spec:
            args.append('--with-libtool=yes')
        else:
            args.append('--with-libtool=no')

        if '+libz' in spec:
            args.append('--with-libz={0}'.format(spec['zlib'].prefix))
        else:
            args.append('--with-libz=no')

        if '+libiconv' in spec:
            args.append('--with-libiconv-prefix={0}'.format(
                spec['iconv'].prefix))
        else:
            args.append('--with-libiconv-prefix=no')

        if '+liblzma' in spec:
            args.append('--with-liblzma=yes')
        else:
            args.append('--with-liblzma=no')

        if '+pg' in spec:
            args.append('--with-pg={0}'.format(
                spec['postgresql'].prefix.bin.pg_config))
        else:
            args.append('--with-pg=no')

        if '+cfitsio' in spec:
            args.append('--with-cfitsio={0}'.format(spec['cfitsio'].prefix))
        else:
            args.append('--with-cfitsio=no')

        if '+png' in spec:
            args.append('--with-png={0}'.format(spec['libpng'].prefix))
        else:
            args.append('--with-png=no')

        if '+jpeg' in spec:
            args.append('--with-jpeg={0}'.format(spec['jpeg'].prefix))
        else:
            args.append('--with-jpeg=no')

        if '+gif' in spec:
            args.append('--with-gif={0}'.format(spec['giflib'].prefix))
        else:
            args.append('--with-gif=no')

        # https://trac.osgeo.org/gdal/wiki/SOSI
        if '+sosi' in spec:
            args.append('--with-sosi={0}'.format(spec['fyba'].prefix))
        else:
            args.append('--with-sosi=no')

        # https://trac.osgeo.org/gdal/wiki/HDF
        if '+hdf4' in spec:
            args.append('--with-hdf4={0}'.format(spec['hdf'].prefix))
            hdf4 = self.spec['hdf']
            if '+external-xdr' in hdf4 and hdf4['rpc'].name != 'libc':
                libs.append(hdf4['rpc'].libs.link_flags)
        else:
            args.append('--with-hdf4=no')

        if '+hdf5' in spec:
            args.append('--with-hdf5={0}'.format(spec['hdf5'].prefix))
        else:
            args.append('--with-hdf5=no')

        # https://trac.osgeo.org/gdal/wiki/NetCDF
        if '+netcdf' in spec:
            args.append('--with-netcdf={0}'.format(spec['netcdf-c'].prefix))
        else:
            args.append('--with-netcdf=no')

        # https://trac.osgeo.org/gdal/wiki/JasPer
        if '+jasper' in spec:
            args.append('--with-jasper={0}'.format(spec['jasper'].prefix))
        else:
            args.append('--with-jasper=no')

        if '+openjpeg' in spec:
            args.append('--with-openjpeg=yes')
        else:
            args.append('--with-openjpeg=no')

        if '+xerces' in spec:
            args.append('--with-xerces={0}'.format(spec['xerces-c'].prefix))
        else:
            args.append('--with-xerces=no')

        if '+expat' in spec:
            args.append('--with-expat={0}'.format(spec['expat'].prefix))
        else:
            args.append('--with-expat=no')

        # https://trac.osgeo.org/gdal/wiki/LibKML
        # https://gdal.org/drivers/vector/libkml.html
        if '+libkml' in spec:
            args.append('--with-libkml={0}'.format(spec['libkml'].prefix))
        else:
            args.append('--with-libkml=no')

        if '+odbc' in spec:
            args.append('--with-odbc={0}'.format(spec['unixodbc'].prefix))
        else:
            args.append('--with-odbc=no')

        # https://trac.osgeo.org/gdal/wiki/LibCurl
        if '+curl' in spec:
            args.append('--with-curl={0}'.format(
                join_path(spec['curl'].prefix.bin, 'curl-config')))
        else:
            args.append('--with-curl=no')

        if '+xml2' in spec:
            args.append('--with-xml2={0}'.format(
                join_path(spec['libxml2'].prefix.bin, 'xml2-config')))
        else:
            args.append('--with-xml2=no')

        # https://trac.osgeo.org/gdal/wiki/SQLite
        if '+sqlite3' in spec:
            args.append('--with-sqlite3={0}'.format(spec['sqlite'].prefix))
        else:
            args.append('--with-sqlite3=no')

        if '+pcre' in spec:
            args.append('--with-pcre={0}'.format(spec['pcre'].prefix))
        else:
            args.append('--with-pcre=no')

        if '+geos' in spec:
            args.append('--with-geos={0}'.format(
                join_path(spec['geos'].prefix.bin, 'geos-config')))
        else:
            args.append('--with-geos=no')

        if '+opencl' in spec:
            args.append('--with-opencl={0}'.format(spec['opencl'].prefix))
        else:
            args.append('--with-opencl=no')

        if '+poppler' in spec:
            args.append('--with-poppler={0}'.format(spec['poppler'].prefix))
        else:
            args.append('--with-poppler=no')

        if '+perl' in spec:
            args.append('--with-perl=yes')
        else:
            args.append('--with-perl=no')

        if '+python' in spec:
            args.append('--with-python={0}'.format(
                spec['python'].command.path))
        else:
            args.append('--with-python=no')

        # https://trac.osgeo.org/gdal/wiki/GdalOgrInJava
        # https://trac.osgeo.org/gdal/wiki/GdalOgrInJavaBuildInstructionsUnix
        if '+java' in spec:
            args.extend([
                '--with-java={0}'.format(spec['java'].home),
                '--with-jvm-lib={0}'.format(
                    spec['java'].libs.directories[0]),
                '--with-jvm-lib-add-rpath'
            ])
        else:
            args.append('--with-java=no')

        # https://trac.osgeo.org/gdal/wiki/mdbtools
        # http://www.gdal.org/drv_mdb.html
        if '+mdb' in spec:
            args.append('--with-mdb=yes')
        else:
            args.append('--with-mdb=no')

        if '+armadillo' in spec:
            args.append('--with-armadillo={0}'.format(
                spec['armadillo'].prefix))
        else:
            args.append('--with-armadillo=no')

        # TODO: add packages for these dependencies
        args.extend([
            # https://trac.osgeo.org/gdal/wiki/GRASS
            '--with-grass=no',
            '--with-libgrass=no',
            '--with-pcraster=no',
            '--with-dds=no',
            '--with-gta=no',
            '--with-pcidsk=no',
            '--with-ogdi=no',
            '--with-fme=no',
            # https://trac.osgeo.org/gdal/wiki/FileGDB
            '--with-fgdb=no',
            # https://trac.osgeo.org/gdal/wiki/ECW
            '--with-ecw=no',
            # https://trac.osgeo.org/gdal/wiki/JP2KAK
            '--with-kakadu=no',
            # https://trac.osgeo.org/gdal/wiki/MrSID
            '--with-mrsid=no',
            '--with-jp2mrsid=no',
            '--with-mrsid_lidar=no',
            # https://trac.osgeo.org/gdal/wiki/MSG
            '--with-msg=no',
            # https://trac.osgeo.org/gdal/wiki/Oracle
            '--with-oci=no',
            '--with-mysql=no',
            # https://trac.osgeo.org/gdal/wiki/Ingres
            '--with-ingres=no',
            '--with-dods-root=no',
            '--with-spatialite=no',
            '--with-idb=no',
            # https://trac.osgeo.org/gdal/wiki/ArcSDE
            '--with-sde=no',
            # https://trac.osgeo.org/gdal/wiki/Epsilon
            '--with-epsilon=no',
            '--with-webp=no',
            '--with-freexl=no',
            '--with-pam=no',
            '--with-podofo=no',
            '--with-rasdaman=no',
        ])

        # TODO: add packages for these dependencies (only for 2.3 and older)
        if spec.satisfies('@:2.3'):
            args.append('--with-php=no')

        # TODO: add packages for these dependencies (only for 2.3 and newer)
        if spec.satisfies('@2.3:'):
            args.extend([
                '--with-jp2lura=no',
                '--with-rasterlite2=no',
                # https://trac.osgeo.org/gdal/wiki/DxfDwg
                '--with-teigha=no',
                '--with-sfcgal=no',
            ])

        # TODO: add packages for these dependencies (only for 2.1 and newer)
        if spec.satisfies('@2.1:'):
            args.extend([
                '--with-mongocxx=no',
                '--with-gnm=no',
                '--with-pdfium=no',
            ])

        if libs:
            args.append('LIBS=' + ' '.join(libs))

        return args

    # https://trac.osgeo.org/gdal/wiki/GdalOgrInJavaBuildInstructionsUnix
    def build(self, spec, prefix):
        make()
        if '+java' in spec:
            with working_dir('swig/java'):
                make()

    def check(self):
        # no top-level test target
        if '+java' in self.spec:
            with working_dir('swig/java'):
                make('test')

    def install(self, spec, prefix):
        make('install')
        if '+java' in spec:
            with working_dir('swig/java'):
                make('install')
                install('*.jar', prefix)

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def import_module_test(self):
        if '+python' in self.spec:
            with working_dir('spack-test', create=True):
                for module in self.import_modules:
                    python('-c', 'import {0}'.format(module))

    @run_after('install')
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if 'platform=darwin' in self.spec:
            fix_darwin_install_name(self.prefix.lib)
