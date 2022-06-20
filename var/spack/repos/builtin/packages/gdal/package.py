# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *
from spack.util.environment import filter_system_paths


class Gdal(CMakePackage):
    """GDAL: Geospatial Data Abstraction Library.

    GDAL is a translator library for raster and vector geospatial data formats that
    is released under an MIT style Open Source License by the Open Source Geospatial
    Foundation. As a library, it presents a single raster abstract data model and
    single vector abstract data model to the calling application for all supported
    formats. It also comes with a variety of useful command line utilities for data
    translation and processing.
    """

    homepage   = "https://www.gdal.org/"
    url        = "https://download.osgeo.org/gdal/3.2.0/gdal-3.2.0.tar.xz"
    list_url   = "https://download.osgeo.org/gdal/"
    list_depth = 1

    maintainers = ['adamjstewart']

    version('3.5.0', sha256='d49121e5348a51659807be4fb866aa840f8dbec4d1acba6d17fdefa72125bfc9')
    version('3.4.3', sha256='02a27b35899e1c4c3bcb6007da900128ddd7e8ab7cd6ccfecf338a301eadad5a')
    version('3.4.2', sha256='16baf03dfccf9e3f72bb2e15cd2d5b3f4be0437cdff8a785bceab0c7be557335')
    version('3.4.1', sha256='332f053516ca45101ef0f7fa96309b64242688a8024780a5d93be0230e42173d')
    version('3.4.0', sha256='ac7bd2bb9436f3fc38bc7309704672980f82d64b4d57627d27849259b8f71d5c')
    version('3.3.3', sha256='1e8fc8b19c77238c7f4c27857d04857b65d8b7e8050d3aac256d70fa48a21e76')
    version('3.3.2', sha256='630e34141cf398c3078d7d8f08bb44e804c65bbf09807b3610dcbfbc37115cc3')
    version('3.3.1', sha256='48ab00b77d49f08cf66c60ccce55abb6455c3079f545e60c90ee7ce857bccb70')
    version('3.3.0', sha256='190c8f4b56afc767f43836b2a5cd53cc52ee7fdc25eb78c6079c5a244e28efa7')
    version('3.2.3', sha256='d9ec8458fe97fd02bf36379e7f63eaafce1005eeb60e329ed25bb2d2a17a796f')
    version('3.2.2', sha256='a7e1e414e5c405af48982bf4724a3da64a05770254f2ce8affb5f58a7604ca57')
    version('3.2.1', sha256='6c588b58fcb63ff3f288eb9f02d76791c0955ba9210d98c3abd879c770ae28ea')
    version('3.2.0', sha256='b051f852600ffdf07e337a7f15673da23f9201a9dbb482bd513756a3e5a196a6')
    version('3.1.4', sha256='7b82486f71c71cec61f9b237116212ce18ef6b90f068cbbf9f7de4fc50b576a8')
    version('3.1.3', sha256='161cf55371a143826f1d76ce566db1f0a666496eeb4371aed78b1642f219d51d')
    version('3.1.2', sha256='767c8d0dfa20ba3283de05d23a1d1c03a7e805d0ce2936beaff0bb7d11450641')
    version('3.1.1', sha256='97154a606339a6c1d87c80fb354d7456fe49828b2ef9a3bc9ed91771a03d2a04')
    version('3.1.0', sha256='e754a22242ccbec731aacdb2333b567d4c95b9b02d3ba1ea12f70508d244fcda')
    version('3.0.4', sha256='5569a4daa1abcbba47a9d535172fc335194d9214fdb96cd0f139bb57329ae277')
    version('3.0.3', sha256='e20add5802265159366f197a8bb354899e1693eab8dbba2208de14a457566109')
    version('3.0.2', sha256='c3765371ce391715c8f28bd6defbc70b57aa43341f6e94605f04fe3c92468983')
    version('3.0.1', sha256='45b4ae25dbd87282d589eca76481c426f72132d7a599556470d5c38263b09266')
    version('3.0.0', sha256='ad316fa052d94d9606e90b20a514b92b2dd64e3142dfdbd8f10981a5fcd5c43e')
    version('2.4.4', sha256='a383bd3cf555d6e1169666b01b5b3025b2722ed39e834f1b65090f604405dcd8')
    version('2.4.3', sha256='d52dc3e0cff3af3e898d887c4151442989f416e839948e73f0994f0224bbff60')
    version('2.4.2', sha256='dcc132e469c5eb76fa4aaff238d32e45a5d947dc5b6c801a123b70045b618e0c')
    version('2.4.1', sha256='fd51b4900b2fc49b98d8714f55fc8a78ebfd07218357f93fb796791115a5a1ad')
    version('2.4.0', sha256='c3791dcc6d37e59f6efa86e2df2a55a4485237b0a48e330ae08949f0cdf00f27')
    version('2.3.3', sha256='c3635e41766a648f945d235b922e3c5306e26a2ee5bbd730d2181e242f5f46fe')
    version('2.3.2', sha256='3f6d78fe8807d1d6afb7bed27394f19467840a82bc36d65e66316fa0aa9d32a4')
    version('2.3.1', sha256='9c4625c45a3ee7e49a604ef221778983dd9fd8104922a87f20b99d9bedb7725a')
    version('2.3.0', sha256='6f75e49aa30de140525ccb58688667efe3a2d770576feb7fbc91023b7f552aa2')
    version('2.2.4', sha256='441eb1d1acb35238ca43a1a0a649493fc91fdcbab231d0747e9d462eea192278')
    version('2.2.3', sha256='a328d63d476b3653f5a25b5f7971e87a15cdf8860ab0729d4b1157ba988b8d0b')
    version('2.2.2', sha256='eb25d6ee85f4f5ac1d5581958f8c6eed9b1d50746f82866fe92e507541def35b')
    version('2.2.1', sha256='927098d54083ac919a497f787b835b099e9a194f2e5444dbff901f7426b86066')
    version('2.2.0', sha256='0d4c326862e0f118e17418c042c2bcd037b25abd3fb198e1fc5d40b11a9fc8ea')
    version('2.1.4', sha256='e06a7ae4c4ed2fd678cd045ff50a10ff5002f3b81cdfcd8ab03c39ce962d9b63')
    version('2.1.3', sha256='b489793627e6cb8d2ff8d7737b61daf58382fe189fae4c581ddfd48c04b49005')
    version('2.1.2', sha256='b597f36bd29a2b4368998ddd32b28c8cdf3c8192237a81b99af83cc17d7fa374')
    version('2.1.1', sha256='87ce516ce757ad1edf1e21f007fbe232ed2e932af422e9893f40199711c41f92')
    version('2.1.0', sha256='568b43441955b306364fcf97fb47d4c1512ac6f2f5f76b2ec39a890d2418ee03')
    version('2.0.3', sha256='3c6c5ade299c7a52fc9c5d2111110c97032e1f0c2593ce6091c364b1a43b442a')
    version('2.0.2', sha256='90f838853cc1c07e55893483faa7e923e4b4b1659c6bc9df3538366030a7e622')
    version('2.0.1', sha256='2564c91ed8ed36274ee31002a25798f5babc4221e879cb5013867733d80f9920')
    version('2.0.0', sha256='91704fafeea2349c5e268dc1e2d03921b3aae64b05ee01d59fdfc1a6b0ffc061')

    # Optional dependencies
    variant('armadillo', default=False, description='Speed up computations related to the Thin Plate Spline transformer')
    variant('arrow', default=False, when='@3.5:', description='Required for Arrow driver')
    variant('blosc', default=False, description='Required for Zarr driver')
    variant('brunsli', default=True, description='Required for MRF driver')
    variant('cfitsio', default=False, description='Required for FITS driver')
    # variant('crnlib', default=False, description='Required for DDS driver')
    variant('curl', default=False, description='Required for network access')
    variant('cryptopp', default=False, when='@2.1:', description='Required for EEDAI driver')
    variant('deflate', default=False, description='Required for Deflate compression')
    # variant('ecw', default=False, description='Required for ECW driver')
    variant('expat', default=True, description='Required for XML parsing in many OGR drivers')
    # variant('filegdb', default=False, description='Required for FileGDB driver')
    variant('freexl', default=False, description='Required for XLS driver')
    variant('fyba', default=False, description='Required for SOSI driver')
    variant('geos', default=True, description='Required for geometry processing operations in OGR')
    variant('gif', default=False, description='Required for GIF driver')
    # variant('gta', default=False, description='Required for GTA driver')
    # variant('heif', default=False, description='Required for HEIF driver')
    variant('hdf4', default=False, description='Required for HDF4 driver')
    variant('hdf5', default=False, description='Required for HDF5, BAG, and KEA drivers')
    variant('hdfs', default=False, description='Required for Hadoop filesystem support')
    variant('iconv', default=False, description='Required for text encoding conversion')
    # variant('idb', default=False, description='Required for IDB driver')
    variant('jpeg', default=True, description='Required for JPEG driver')
    # variant('jxl', default=False, description='Required for JPEGXL driver')
    # variant('kdu', default=False, description='Required for JP2KAK and JPIPKAK drivers')
    variant('kea', default=False, when='@2:', description='Required for KEA driver')
    variant('lerc', default=True, description='Required for LERC compression')
    variant('libkml', default=False, description='Required for LIBKML driver')
    variant('liblzma', default=False, description='Required for Zarr driver')
    variant('libxml2', default=False, description='Required for XML validation in many OGR drivers')
    # variant('luratech', default=False, description='Required for JP2Lura driver')
    variant('lz4', default=False, description='Required for Zarr driver')
    variant('mongocxx', default=False, description='Required for MongoDBv3 driver')
    # variant('mrsid', default=False, description='Required for MrSID driver')
    # variant('mssql_ncli', default=False, when='@3.5:', description='Required for MSSQLSpatial driver')
    # variant('mssql_odbc', default=False, when='@3.5:', description='Required for MSSQLSpatial driver')
    variant('mysql', default=False, description='Required for MySQL driver')
    variant('netcdf', default=False, description='Required for NetCDF driver')
    variant('odbc', default=False, description='Required for many OGR drivers')
    # variant('odbccpp', default=False, description='Required for SAP HANA driver')
    # variant('ogdi', default=False, description='Required for OGDI driver')
    # variant('opencad', default=False, when='@3.5:', description='Required for CAD driver')
    variant('opencl', default=False, description='Required to accelerate warping computations')
    variant('openexr', default=False, description='Required for EXR driver')
    variant('openjpeg', default=False, description='Required for JP2OpenJPEG driver')
    variant('openssl', default=False, description='Required for EEDAI driver')
    variant('oracle', default=False, description='Required for OCI and GeoRaster drivers')
    variant('parquet', default=False, when='@3.5:', description='Required for Parquet driver')
    variant('pcre2', default=False, when='@3.4.1:', description='Required for REGEXP operator in drivers using SQLite3')
    # variant('pdfium', default=False, description='Possible backend for PDF driver')
    variant('png', default=True, description='Required for PNG driver')
    variant('poppler', default=False, description='Possible backend for PDF driver')
    variant('postgresql', default=False, description='Required for PostgreSQL and PostGISRaster drivers')
    # variant('qb3', default=False, when='@3.5:', description='Required for MRF driver')
    variant('qhull', default=True, description='Used for linear interpolation of gdal_grid')
    # variant('rasterlite2', default=False, description='Required for RasterLite2 driver')
    # variant('rdb', default=False, description='Required for RDB driver')
    variant('spatialite', default=False, description='Required for SQLite and GPKG drivers')
    variant('sqlite3', default=True, description='Required for SQLite and GPKG drivers')
    variant('sfcgal', default=False, description='Provides 3D geometry operations')
    # variant('teigha', default=False, description='Required for DWG and DGNv8 drivers')
    # variant('tiledb', default=False, description='Required for TileDB driver')
    variant('webp', default=False, description='Required for WEBP driver')
    variant('xercesc', default=False, description='Required for XML parsing capabilities in many OGR drivers')
    variant('zstd', default=False, description='Required for Zarr driver')



    # variant('jasper',    default=False, description='Include JPEG-2000 support via JasPer library', when='@:3.4')
    # variant('pcre',      default=False, description='Include libpcre support')
    # variant('mdb',       default=False, description='Include MDB driver', when='@:3.4 +java')
    # variant('grib',      default=False, description='Include GRIB support')


    # Language bindings
    variant('python', default=False, description='Build Python bindings')
    variant('java', default=False, description='Build Java bindings')
    variant('csharp', default=False, when='@3.5:', description='Build C# bindings')
    variant('perl', default=False, when='@:3.4', description='Build Perl bindings')

    # Required dependencies
    depends_on('cmake@3.9:', when='@3.5:', type='build')
    depends_on('ninja', when='@3.5:', type='build')
    depends_on('gmake', when='@:3.4', type='build')
    depends_on('proj@6:', when='@3:')
    depends_on('proj@:6', when='@2.5:2')
    depends_on('proj@:5', when='@2.4')
    depends_on('proj@:4', when='@2.3')
    depends_on('zlib')
    depends_on('libtiff@4:', when='@3:')
    depends_on('libtiff@3.6.0:')  # 3.9.0+ needed to pass testsuite
    depends_on('libgeotiff@1.5:', when='@3:')
    depends_on('libgeotiff@1.2.1:1.5', when='@2.4.1:2')
    depends_on('libgeotiff@1.2.1:1.4', when='@:2.4.0')
    depends_on('json-c')
    depends_on('json-c@0.12.1', when='@:2.2')

    # Optional dependencies
    depends_on('armadillo', when='+armadillo')
    depends_on('blas', when='+armadillo')
    depends_on('lapack', when='+armadillo')
    depends_on('arrow', when='+arrow')
    depends_on('c-blosc', when='+blosc')
    depends_on('brunsli', when='+brunsli')
    depends_on('cfitsio', when='+cfitsio')
    # depends_on('crunch', when='+crnlib')
    depends_on('curl', when='+curl')
    depends_on('cryptopp', when='+cryptopp')
    depends_on('libdeflate', when='+deflate')
    # depends_on('ecw', when='+ecw')
    depends_on('expat', when='+expat')
    # depends_on('filegdb', when='+filegdb')
    depends_on('freexl', when='+freexl')
    depends_on('fyba', when='+fyba')
    depends_on('geos', when='+geos')
    depends_on('giflib', when='+gif')
    # depends_on('gta', when='+gta')
    # depends_on('heif@1.1:', when='+heif')
    depends_on('hdf', when='+hdf4')
    depends_on('hdf5+cxx', when='+hdf5')
    depends_on('hdf5@:1.12', when='@:3.4.1 +hdf5')
    depends_on('hadoop', when='+hdfs')
    depends_on('iconv', when='+iconv')
    # depends_on('idb', when='+idb')
    depends_on('jpeg', when='+jpeg')
    # depends_on('libjxl', when='+jxl')
    # depends_on('kakadu', when='+kdu')
    depends_on('kealib', when='+kea')
    depends_on('lerc', when='+lerc')
    depends_on('libkml@1.3:', when='+libkml')
    depends_on('xz', when='+liblzma')
    depends_on('libxml2', when='+libxml2')
    # depends_on('luratech', when='+luratech')
    depends_on('lz4', when='+lz4')
    depends_on('mongo-cxx-driver', when='+mongocxx')
    # depends_on('bsoncxx', when='+mongocxx')
    # depends_on('mrsid', when='+mrsid')
    # depends_on('mssql_ncli', when='+mssql_ncli')
    # depends_on('mssql_odbc', when='+mssql_odbc')
    depends_on('mysql', when='+mysql')
    depends_on('netcdf-c', when='+netcdf')
    depends_on('unixodbc', when='+odbc')
    # depends_on('odbc-cpp-wrapper', when='+odbccpp')
    # depends_on('ogdi', when='+ogdi')
    # depends_on('lib-opencad', when='+opencad')
    depends_on('opencl', when='+opencl')
    depends_on('openexr@2.2:', when='+openexr')
    depends_on('openjpeg', when='+openjpeg')
    depends_on('openssl', when='+openssl')
    depends_on('oracle-instant-client', when='+oracle')
    depends_on('parquet-cpp', when='+parquet')
    depends_on('pcre2', when='+pcre2')
    # depends_on('pdfium', when='+pdfium')
    depends_on('libpng', when='+png')
    depends_on('poppler', when='+poppler')
    depends_on('poppler@0.24:', when='@3: +poppler')
    depends_on('poppler@:0.63', when='@:2.3 +poppler')
    depends_on('poppler@:0.71', when='@:2.4 +poppler')
    depends_on('poppler@:21', when='@:3.4.1 +poppler')
    depends_on('postgresql', when='+postgresql')
    # depends_on('qb3', when='+qb3')
    depends_on('qhull', when='+qhull')
    # depends_on('rasterlite2@1.1:', when='+rasterlite2')
    # depends_on('rdblib', when='+rdb')
    depends_on('libspatialite', when='+spatialite')
    depends_on('sqlite@3', when='+sqlite3')
    depends_on('sfcgal', when='+sfcgal')
    # depends_on('teigha', when='+teigha')
    # depends_on('tiledb', when='+tiledb')
    depends_on('libwebp', when='+webp')
    depends_on('xerces-c', when='+xercesc')
    depends_on('zstd', when='+zstd')


    # depends_on('jasper@1.900.1', patches=[patch('uuid.patch')], when='+jasper')
    # depends_on('pcre', when='+pcre')
    # depends_on('jackcess@1.2.0:1.2', type='run', when='+mdb')


    # Language bindings
    # FIXME: Allow packages to extend multiple packages
    # See https://github.com/spack/spack/issues/987
    extends('python', when='+python')
    # extends('openjdk', when='+java')
    # extends('perl', when='+perl')

    # see gdal_version_and_min_supported_python_version
    # in swig/python/osgeo/__init__.py
    depends_on('python@3.6:', type=('build', 'link', 'run'), when='@3.3:+python')
    depends_on('python@2.0:', type=('build', 'link', 'run'), when='@3.2:+python')
    depends_on('python', type=('build', 'link', 'run'), when='+python')
    # swig/python/setup.py
    depends_on('py-setuptools@:57', type='build', when='@:3.2+python')  # needs 2to3
    depends_on('py-setuptools', type='build', when='+python')
    depends_on('py-numpy@1.0.0:', type=('build', 'run'), when='+python')
    depends_on('swig', type='build', when='+python')
    depends_on('java@7:', type=('build', 'link', 'run'), when='@3.2:+java')
    depends_on('java@6:', type=('build', 'link', 'run'), when='@2.4:+java')
    depends_on('java@5:', type=('build', 'link', 'run'), when='@2.1:+java')
    depends_on('java@4:', type=('build', 'link', 'run'), when='@:2.0+java')
    depends_on('ant', type='build', when='+java')
    depends_on('swig', type='build', when='+java')
    depends_on('perl', type=('build', 'run'), when='+perl')
    depends_on('swig', type='build', when='+perl')

    # https://trac.osgeo.org/gdal/wiki/SupportedCompilers
    msg = 'GDAL requires C++11 support'
    conflicts('%gcc@:4.8.0', msg=msg)
    conflicts('%clang@:3.2', msg=msg)
    conflicts('%intel@:12',  msg=msg)
    conflicts('%xl@:13.0',   msg=msg)
    conflicts('%xl_r@:13.0', msg=msg)

    # conflicts('+pcre2', when='+pcre', msg='+pcre2 and +pcre are mutually exclusive')

    # https://github.com/OSGeo/gdal/issues/3782
    patch('https://github.com/OSGeo/gdal/pull/3786.patch?full_index=1', when='@3.3.0', level=2,
          sha256='9f9824296e75b34b3e78284ec772a5ac8f8ba92c17253ea9ca242caf766767ce')

    generator = 'Ninja'
    executables = ['^gdal-config$']

    @classmethod
    def determine_version(cls, exe):
        return Executable(exe)('--version', output=str, error=str).rstrip()

    @property
    def import_modules(self):
        modules = ['osgeo']
        if self.spec.satisfies('@3.3:'):
            modules.append('osgeo_utils')
        else:
            modules.append('osgeo.utils')
        return modules

    @when('@:3.4')
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

        # `spack test run gdal+python` requires these for the Python bindings
        # to find the correct libraries
        libs = []
        for dep in self.spec.dependencies(deptype='link'):
            query = self.spec[dep.name]
            libs.extend(filter_system_paths(query.libs.directories))
        if sys.platform == 'darwin':
            env.prepend_path('DYLD_FALLBACK_LIBRARY_PATH', ':'.join(libs))
        else:
            env.prepend_path('LD_LIBRARY_PATH', ':'.join(libs))

    def patch(self):
        if '+java platform=darwin' in self.spec:
            filter_file('linux', 'darwin', 'swig/java/java.opt', string=True)

    def cmake_args(self):
        # https://gdal.org/build_hints.html
        return [
            # Only use Spack-installed dependencies
            self.define('GDAL_USE_EXTERNAL_LIBS', False),
            self.define('GDAL_USE_INTERNAL_LIBS', False),

            # Required dependencies
            self.define('GDAL_USE_GEOTIFF', True),
            self.define('GDAL_USE_JSONC', True),
            self.define('GDAL_USE_TIFF', True),
            self.define('GDAL_USE_ZLIB', True),

            # Optional dependencies
            self.define_from_variant('GDAL_USE_ARMADILLO', 'armadillo'),
            self.define_from_variant('GDAL_USE_ARROW', 'arrow'),
            self.define_from_variant('GDAL_USE_BLOSC', 'blosc'),
            self.define_from_variant('GDAL_USE_BRUNSLI', 'brunsli'),
            self.define_from_variant('GDAL_USE_CFITSIO', 'cfitsio'),
            # self.define_from_variant('GDAL_USE_CRNLIB', 'crnlib'),
            self.define_from_variant('GDAL_USE_CURL', 'curl'),
            self.define_from_variant('GDAL_USE_DEFLATE', 'deflate'),
            # self.define_from_variant('GDAL_USE_ECW', 'ecw'),
            self.define_from_variant('GDAL_USE_EXPAT', 'expat'),
            # self.define_from_variant('GDAL_USE_FILEGDB', 'filegdb'),
            self.define_from_variant('GDAL_USE_FREEXL', 'freexl'),
            self.define_from_variant('GDAL_USE_FYBA', 'fyba'),
            self.define_from_variant('GDAL_USE_GEOS', 'geos'),
            self.define_from_variant('GDAL_USE_GIF', 'gif'),
            # self.define_from_variant('GDAL_USE_GTA', 'gta'),
            # self.define_from_variant('GDAL_USE_HEIF', 'heif'),
            self.define_from_variant('GDAL_USE_HDF4', 'hdf4'),
            self.define_from_variant('GDAL_USE_HDF5', 'hdf5'),
            self.define_from_variant('GDAL_USE_HDFS', 'hdfs'),
            self.define_from_variant('GDAL_USE_ICONV', 'iconv'),
            # self.define_from_variant('GDAL_USE_IDB', 'idb'),
            self.define_from_variant('GDAL_USE_JPEG', 'jpeg'),
            # self.define_from_variant('GDAL_USE_JXL', 'jxl'),
            # self.define_from_variant('GDAL_USE_KDU', 'kdu'),
            self.define_from_variant('GDAL_USE_KEA', 'kea'),
            self.define_from_variant('GDAL_USE_LIBKML', 'libkml'),
            self.define_from_variant('GDAL_USE_LIBLZMA', 'liblzma'),
            self.define_from_variant('GDAL_USE_LIBXML2', 'libxml2'),
            # self.define_from_variant('GDAL_USE_LURATECH', 'luratech'),
            self.define_from_variant('GDAL_USE_LZ4', 'lz4'),
            self.define_from_variant('GDAL_USE_MONGOCXX', 'mongocxx'),
            # self.define_from_variant('GDAL_USE_MRSID', 'mrsid'),
            # self.define_from_variant('GDAL_USE_MSSQL_NCLI', 'mssql_ncli'),
            # self.define_from_variant('GDAL_USE_MSSQL_ODBC', 'mssql_odbc'),
            self.define_from_variant('GDAL_USE_MYSQL', 'mysql'),
            self.define_from_variant('GDAL_USE_NETCDF', 'netcdf'),
            self.define_from_variant('GDAL_USE_ODBC', 'odbc'),
            # self.define_from_variant('GDAL_USE_ODBCCPP', 'odbccpp'),
            # self.define_from_variant('GDAL_USE_OGDI', 'ogdi'),
            # self.define_from_variant('GDAL_USE_OPENCAD', 'opencad'),
            self.define_from_variant('GDAL_USE_OPENCL', 'opencl'),
            self.define_from_variant('GDAL_USE_OPENEXR', 'openexr'),
            self.define_from_variant('GDAL_USE_OPENJPEG', 'openjpeg'),
            self.define_from_variant('GDAL_USE_OPENSSL', 'openssl'),
            self.define_from_variant('GDAL_USE_ORACLE', 'oracle'),
            self.define_from_variant('GDAL_USE_PARQUET', 'parquet'),
            self.define_from_variant('GDAL_USE_PCRE2', 'pcre2'),
            # self.define_from_variant('GDAL_USE_PDFIUM', 'pdfium'),
            self.define_from_variant('GDAL_USE_PNG', 'png'),
            self.define_from_variant('GDAL_USE_POSTGRESQL', 'postgresql'),
            # self.define_from_variant('GDAL_USE_QB3', 'qb3'),
            self.define_from_variant('GDAL_USE_QHULL', 'qhull'),
            # self.define_from_variant('GDAL_USE_RASTERLITE2', 'rasterlite2'),
            # self.define_from_variant('GDAL_USE_RDB', 'rdb'),
            self.define_from_variant('GDAL_USE_SPATIALITE', 'spatialite'),
            self.define_from_variant('GDAL_USE_SQLITE3', 'sqlite3'),
            self.define_from_variant('GDAL_USE_SFCGAL', 'sfcgal'),
            # self.define_from_variant('GDAL_USE_TEIGHA', 'teigha'),
            # self.define_from_variant('GDAL_USE_TILEDB', 'tiledb'),
            self.define_from_variant('GDAL_USE_WEBP', 'webp'),
            self.define_from_variant('GDAL_USE_XERCESC', 'xercesc'),
            self.define_from_variant('GDAL_USE_ZSTD', 'zstd'),

            # Language bindings
            self.define_from_variant('BUILD_PYTHON_BINDINGS', 'python'),
            self.define_from_variant('BUILD_JAVA_BINDINGS', 'java'),
            self.define_from_variant('BUILD_CSHARP_BINDINGS', 'csharp'),
        ]

    def with_or_without(self, name, variant=None, package=None):
        if not variant:
            variant = name

        if variant not in self.variants:
            msg = '"{}" is not a variant of "{}"'
            raise KeyError(msg.format(variant, self.name))

        if variant not in self.spec.variants:
            return ''

        if self.spec.variants[variant].value:
            if package:
                return '--with-{}={}'.format(name, self.spec[package].prefix)
            else:
                return '--with-{}'.format(name)
        else:
            return '--without-{}'.format(name)

    def configure_args(self):
        # https://trac.osgeo.org/gdal/wiki/BuildHints
        spec = self.spec
        args = [
            '--prefix={}'.format(self.prefix),

            # Required dependencies
            '--with-geotiff={}'.format(spec['libgeotiff'].prefix),
            '--with-libjson-c={}'.format(spec['json-c'].prefix),
            '--with-proj={}'.format(spec['proj'].prefix),
            '--with-libtiff={}'.format(spec['libtiff'].prefix),
            '--with-libz={}'.format(spec['zlib'].prefix),

            # Optional dependencies
            self.with_or_without('armadillo', package='armadillo'),
            self.with_or_without('blosc', package='c-blosc'),
            self.with_or_without('brunsli'),
            self.with_or_without('cfitsio', package='cfitsio'),
            '--without-dds',
            # self.with_or_without('dds', variant='crnlib', package='crunch'),
            self.with_or_without('curl', package='curl'),
            self.with_or_without('cryptopp', package='cryptopp'),
            self.with_or_without('libdeflate', variant='deflate', package='libdeflate'),
            '--without-ecw',
            # self.with_or_without('ecw', package='ecw'),
            self.with_or_without('expat', package='expat'),
            '--without-fgdb',
            # self.with_or_without('fgdb', variant='filegdb', package='filegdb'),
            self.with_or_without('freexl', package='freexl'),
            self.with_or_without('sosi', variant='fyba', package='fyba'),
            self.with_or_without('geos', package='geos'),
            self.with_or_without('gif', package='giflib'),
            '--without-gta',
            # self.with_or_without('gta', package='gta'),
            '--without-heif',
            # self.with_or_without('heif'),
            self.with_or_without('hdf4', package='hdf'),
            self.with_or_without('hdf5', package='hdf5'),
            self.with_or_without('hdfs', package='hadoop'),
            self.with_or_without('libiconv-prefix', variant='iconv', package='iconv'),
            '--without-idb',
            # self.with_or_without('idb', package='idb'),
            self.with_or_without('jpeg', package='jpeg'),
            '--without-jxl',
            # self.with_or_without('jxl'),
            '--without-kakadu',
            # self.with_or_without('kakadu', variant='kdu'),
            self.with_or_without('kea', package='kealib'),
            self.with_or_without('lerc', package='lerc'),
            self.with_or_without('libkml', package='libkml'),
            self.with_or_without('liblzma'),
            self.with_or_without('xml2', variant='libxml2'),
            '--without-j2lura',
            # self.with_or_without('j2lura', variant='luratech', package='luratech'),
            self.with_or_without('lz4', package='lz4'),
            self.with_or_without('mongocxxv3', variant='mongocxx'),
            '--without-mrsid',
            # self.with_or_without('mrsid', package='mrsid'),
            self.with_or_without('mysql', package='mysql'),
            self.with_or_without('netcdf', package='netcdf-c'),
            self.with_or_without('odbc', package='unixodbc'),
            '--without-hana',
            # self.with_or_without('hana', variant='odbccpp', package='odbc-cpp-wrapper'),
            '--without-ogdi',
            # self.with_or_without('ogdi', package='ogdi'),
            self.with_or_without('opencl'),
            self.with_or_without('exr', variant='openexr'),
            self.with_or_without('openjpeg'),
            self.with_or_without('crypto', variant='openssl', package='openssl'),
            self.with_or_without('oci', variant='oracle', package='oracle-instant-client'),
            self.with_or_without('pcre2'),
            '--without-pdfium',
            # self.with_or_without('pdfium', package='pdfium'),
            self.with_or_without('png', package='libpng'),
            self.with_or_without('poppler', package='poppler'),
            self.with_or_without('pg', variant='postgresql'),
            self.with_or_without('qhull'),
            '--without-rasterlite2',
            # self.with_or_without('rasterlite2', package='rasterlite2'),
            '--without-rdb',
            # self.with_or_without('rdb', package='rdb'),
            self.with_or_without('spatialite', package='spatialite'),
            self.with_or_without('sqlite3', package='sqlite'),
            self.with_or_without('sfcgal', package='sfcgal'),
            '--without-teigha',
            # self.with_or_without('teigha', package='teigha'),
            '--without-tiledb',
            # self.with_or_without('tiledb', package='tiledb'),
            self.with_or_without('webp', package='libwebp'),
            self.with_or_without('xerces', variant='xercesc', package='xerces-c'),
            self.with_or_without('zstd', package='zstd'),

            # Language bindings
            self.with_or_without('python', package='python'),
            self.with_or_without('java', package='java'),
            self.with_or_without('perl'),
        ]

        # TODO: add flags only available in Autotools
        # TODO: diff each release to see when variants exist

        # # Optional dependencies
        # if spec.satisfies('@3:'):
        #     pass
        # else:
        #     args.append('--with-bsb=no')

        #     if '+grib' in spec:
        #         args.append('--with-grib=yes')
        #     else:
        #         args.append('--with-grib=no')

        #     if spec.satisfies('@2.3:'):
        #         args.append('--with-mrf=no')

        # libs = []
        # if '+hdf4' in spec:
        #     hdf4 = self.spec['hdf']
        #     if '+external-xdr' in hdf4 and hdf4['rpc'].name != 'libc':
        #         libs.append(hdf4['rpc'].libs.link_flags)

        # # https://trac.osgeo.org/gdal/wiki/JasPer
        # if '+jasper' in spec:
        #     args.append('--with-jasper={0}'.format(spec['jasper'].prefix))
        # else:
        #     args.append('--with-jasper=no')

        # if '+pcre' in spec:
        #     args.append('--with-pcre={0}'.format(spec['pcre'].prefix))
        # else:
        #     args.append('--with-pcre=no')

        # # https://trac.osgeo.org/gdal/wiki/mdbtools
        # # https://www.gdal.org/drv_mdb.html
        # if '+mdb' in spec:
        #     args.append('--with-mdb=yes')
        # else:
        #     args.append('--with-mdb=no')

        # # TODO: add packages for these dependencies
        # args.extend([
        #     # https://trac.osgeo.org/gdal/wiki/GRASS
        #     '--with-grass=no',
        #     '--with-libgrass=no',
        #     '--with-pcraster=no',
        #     '--with-pcidsk=no',
        #     '--with-fme=no',
        #     # https://trac.osgeo.org/gdal/wiki/MSG
        #     '--with-msg=no',
        #     # https://trac.osgeo.org/gdal/wiki/Ingres
        #     '--with-ingres=no',
        #     '--with-dods-root=no',
        #     '--with-pam=no',
        #     '--with-podofo=no',
        #     '--with-rasdaman=no',
        # ])

        # # TODO: add packages for these dependencies (only for 3.2 and older)
        # if spec.satisfies('@:3.2'):
        #     # https://trac.osgeo.org/gdal/wiki/Epsilon
        #     args.append('--with-epsilon=no')

        # # TODO: add packages for these dependencies (only for 3.1 and older)
        # if spec.satisfies('@:3.1'):
        #     # https://trac.osgeo.org/gdal/wiki/ArcSDE
        #     args.append('--with-sde=no')

        # # TODO: add packages for these dependencies (only for 2.3 and older)
        # if spec.satisfies('@:2.3'):
        #     args.append('--with-php=no')

        # if libs:
        #     args.append('LIBS=' + ' '.join(libs))

        return args

    @when('@:3.4')
    def cmake(self, spec, prefix):
        configure(*self.configure_args())

    @when('@:3.4')
    def build(self, spec, prefix):
        # https://trac.osgeo.org/gdal/wiki/GdalOgrInJavaBuildInstructionsUnix
        make()
        if '+java' in spec:
            with working_dir('swig/java'):
                make()

    @when('@:3.4')
    def check(self):
        # no top-level test target
        if '+java' in self.spec:
            with working_dir('swig/java'):
                make('test')

    @when('@:3.4')
    def install(self, spec, prefix):
        make('install')
        if '+java' in spec:
            with working_dir('swig/java'):
                make('install')
                install('*.jar', prefix)

    @run_after('install')
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if self.spec.satisfies('@:3.4 platform=darwin'):
            fix_darwin_install_name(self.prefix.lib)

    def test(self):
        """Attempts to import modules of the installed package."""

        if '+python' in self.spec:
            # Make sure we are importing the installed modules,
            # not the ones in the source directory
            for module in self.import_modules:
                self.run_test(self.spec['python'].command.path,
                              ['-c', 'import {0}'.format(module)],
                              purpose='checking import of {0}'.format(module),
                              work_dir='spack-test')
