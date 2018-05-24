##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import sys


class Gdal(AutotoolsPackage):
    """GDAL (Geospatial Data Abstraction Library) is a translator library for
    raster and vector geospatial data formats that is released under an X/MIT
    style Open Source license by the Open Source Geospatial Foundation. As a
    library, it presents a single raster abstract data model and vector
    abstract data model to the calling application for all supported formats.
    It also comes with a variety of useful command line utilities for data
    translation and processing.
    """

    homepage   = "http://www.gdal.org/"
    url        = "http://download.osgeo.org/gdal/2.3.0/gdal-2.3.0.tar.xz"
    list_url   = "http://download.osgeo.org/gdal/"
    list_depth = 1

    version('2.3.0', '2fe9d64fcd9dc37645940df020d3e200')
    version('2.1.2', 'ae85b78888514c75e813d658cac9478e')
    version('2.0.2', '940208e737c87d31a90eaae43d0efd65')

    variant('libz',      default=False, description='Include libz support')
    variant('libiconv',  default=False, description='Include libiconv support')
    variant('liblzma',   default=False, description='Include liblzma support')
    variant('zstd',      default=False, description='Include zstd support')
    variant('pg',        default=False, description='Include PostgreSQL support')
    variant('cfitsio',   default=False, description='Include FITS support')
    variant('png',       default=False, description='Include PNG support')
    variant('jpeg',      default=False, description='Include JPEG support')
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
    variant('odbc',      default=False, description='Include ODBC support')
    variant('curl',      default=False, description='Include curl')
    variant('xml2',      default=False, description='Include libxml2')
    variant('sqlite3',   default=False, description='Use SQLite 3 library')
    variant('pcre',      default=False, description='Include libpcre support')
    variant('geos',      default=False, description='Include GEOS support')
    variant('qhull',     default=False, description='Include QHull support')
    variant('opencl',    default=False, description='Include OpenCL (GPU) support')
    variant('poppler',   default=False, description='Include poppler (for PDF) support')
    variant('proj',      default=False, description='Compile with PROJ.x')
    variant('perl',      default=False, description='Enable perl bindings')
    variant('python',    default=False, description='Enable python bindings')
    variant('java',      default=False, description='Include Java support')
    variant('armadillo', default=False, description='Include Armadillo support for faster TPS transform computation')
    variant('cryptopp',  default=False, description='Include cryptopp support')
    variant('crypto',    default=False, description='Include crypto (from openssl) support')

    extends('perl', when='+perl')
    extends('python', when='+python')

    # GDAL depends on GNUmake on Unix platforms.
    # https://trac.osgeo.org/gdal/wiki/BuildingOnUnix
    depends_on('gmake', type='build')

    # Required dependencies
    # https://trac.osgeo.org/gdal/wiki/TIFF
    depends_on('libtiff@3.6.0:')  # 3.9.0+ needed to pass testsuite
    depends_on('libgeotiff@1.2.1:')
    depends_on('json-c')

    # Optional dependencies
    depends_on('zlib', when='+libz')
    depends_on('libiconv', when='+libiconv')
    depends_on('xz', when='+liblzma')
    depends_on('zstd', when='+zstd')
    depends_on('postgresql', when='+pg')
    depends_on('cfitsio', when='+cfitsio')
    depends_on('libpng', when='+png')
    depends_on('jpeg', when='+jpeg')
    depends_on('giflib', when='+gif')
    depends_on('fyba', when='+sosi')
    depends_on('hdf', when='+hdf4')
    depends_on('hdf5', when='+hdf5')
    depends_on('kealib', when='+kea')
    depends_on('netcdf', when='+netcdf')
    depends_on('jasper', when='+jasper')
    depends_on('openjpeg', when='+openjpeg')
    depends_on('xerces-c', when='+xerces')
    depends_on('expat', when='+expat')
    depends_on('unixodbc', when='+odbc')
    depends_on('curl', when='+curl')
    depends_on('libxml2', when='+xml2')
    depends_on('sqlite', when='+sqlite3')
    depends_on('pcre', when='+pcre')
    depends_on('qhull', when='+qhull')
    depends_on('opencl', when='+opencl')
    depends_on('poppler', when='+poppler')
    depends_on('proj', when='+proj')
    depends_on('java', type=('build', 'run'), when='+java')
    depends_on('armadillo', when='+armadillo')
    depends_on('cryptopp', when='+cryptopp')
    depends_on('openssl', when='+crypto')

    # https://trac.osgeo.org/gdal/wiki/SupportedCompilers
    msg = 'GDAL requires C++11 support'
    conflicts('%gcc@:4.8.0', msg=msg)
    conflicts('%clang@:3.2', msg=msg)
    conflicts('%intel@:12',  msg=msg)
    conflicts('%xl@:13.0',   msg=msg)
    conflicts('%xl_r@:13.0', msg=msg)

    parallel = False

    # https://trac.osgeo.org/gdal/wiki/BuildHints
    def configure_args(self):
        spec = self.spec

        # Required dependencies
        args = [
            '--with-libtiff={0}'.format(spec['libtiff'].prefix),
            '--with-geotiff={0}'.format(spec['libgeotiff'].prefix),
            '--with-libjson-c={0}'.format(spec['json-c'].prefix),
        ]

        # Optional dependencies
        if '+libz' in spec:
            args.append('--with-libz={0}'.format(spec['zlib'].prefix))
        else:
            args.append('--with-libz=no')

        if '+libiconv' in spec:
            args.append('--with-libiconv-prefix={0}'.format(
                spec['libiconv'].prefix))
        else:
            args.append('--with-libiconv-prefix=no')

        if '+liblzma' in spec:
            args.append('--with-liblzma={0}'.format(spec['xz'].prefix))
        else:
            args.append('--with-liblzma=no')

        if '+zstd' in spec:
            args.append('--with-zstd={0}'.format(spec['zstd'].prefix))
        else:
            args.append('--with-zstd=no')

        if '+pg' in spec:
            args.append('--with-pg={0}'.format(spec['postgresql'].prefix))
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

        if '+sosi' in spec:
            args.append('--with-sosi={0}'.format(spec['fyba'].prefix))
        else:
            args.append('--with-sosi=no')

        if '+hdf4' in spec:
            args.append('--with-hdf4={0}'.format(spec['hdf'].prefix))
        else:
            args.append('--with-hdf4=no')

        if '+hdf5' in spec:
            args.append('--with-hdf5={0}'.format(spec['hdf5'].prefix))
        else:
            args.append('--with-hdf5=no')

        if '+kea' in spec:
            args.append('--with-kea={0}'.format(spec['kealib'].prefix))
        else:
            args.append('--with-kea=no')

        if '+netcdf' in spec:
            args.append('--with-netcdf={0}'.format(spec['netcdf'].prefix))
        else:
            args.append('--with-netcdf=no')

        if '+jasper' in spec:
            args.append('--with-jasper={0}'.format(spec['jasper'].prefix))
        else:
            args.append('--with-jasper=no')

        if '+openjpeg' in spec:
            args.append('--with-openjpeg={0}'.format(spec['openjpeg'].prefix))
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

        if '+odbc' in spec:
            args.append('--with-odbc={0}'.format(spec['unixodbc'].prefix))
        else:
            args.append('--with-odbc=no')

        if '+curl' in spec:
            args.append('--with-curl={0}'.format(spec['curl'].prefix))
        else:
            args.append('--with-curl=no')

        if '+xml2' in spec:
            args.append('--with-xml2={0}'.format(spec['libxml2'].prefix))
        else:
            args.append('--with-xml2=no')

        if '+sqlite3' in spec:
            args.append('--with-sqlite3={0}'.format(spec['sqlite'].prefix))
        else:
            args.append('--with-sqlite3=no')

        if '+pcre' in spec:
            args.append('--with-pcre={0}'.format(spec['pcre'].prefix))
        else:
            args.append('--with-pcre=no')

        if '+geos' in spec:
            args.append('--with-geos={0}'.format(spec['geos'].prefix))
        else:
            args.append('--with-geos=no')

        if '+qhull' in spec:
            args.append('--with-qhull={0}'.format(spec['qhull'].prefix))
        else:
            args.append('--with-qhull=no')

        if '+opencl' in spec:
            args.append('--with-opencl={0}'.format(spec['opencl'].prefix))
        else:
            args.append('--with-opencl=no')

        if '+poppler' in spec:
            args.append('--with-poppler={0}'.format(spec['poppler'].prefix))
        else:
            args.append('--with-poppler=no')

        if '+proj' in spec:
            args.append('--with-proj={0}'.format(spec['proj'].prefix))
            if spec.satisfies('^proj@5.0:5.999'):
                args.append('--with-proj5-api=yes')
            else:
                args.append('--with-proj5-api=no')
        else:
            args.append('--with-proj=no')

        if '+perl' in spec:
            args.append('--with-perl={0}'.format(spec['perl'].prefix))
        else:
            args.append('--with-perl=no')

        if '+python' in spec:
            args.append('--with-python={0}'.format(spec['python'].prefix))
        else:
            args.append('--with-python=no')

        if '+java' in spec:
            args.append('--with-java={0}'.format(spec['java'].prefix))
        else:
            args.append('--with-java=no')

        if '+armadillo' in spec:
            args.append('--with-armadillo={0}'.format(
                spec['armadillo'].prefix))
        else:
            args.append('--with-armadillo=no')

        if '+cryptopp' in spec:
            args.append('--with-cryptopp={0}'.format(spec['cryptopp'].prefix))
        else:
            args.append('--with-cryptopp=no')

        if '+crypto' in spec:
            args.append('--with-crypto={0}'.format(spec['openssl'].prefix))
        else:
            args.append('--with-crypto=no')

        # TODO: add packages for these dependencies
        args.extend([
            '--with-grass=no',
            '--with-libgrass=no',
            '--with-pcraster=no',
            '--with-dds=no',
            '--with-gta=no',
            '--with-pcidsk=no',
            '--with-ogdi=no',
            '--with-fme=no',
            '--with-mongocxx=no',
            '--with-fgdb=no',
            '--with-ecw=no',
            '--with-kakadu=no',
            '--with-mrsid=no',
            '--with-jp2mrsid=no',
            '--with-mrsid_lidar=no',
            '--with-jp2lura=no',
            '--with-msg=no',
            '--with-bsb=no',
            '--with-oci=no',
            '--with-grib=no',
            '--with-gnm=no',
            '--with-mysql=no',
            '--with-ingres=no',
            '--with-libkml=no',
            '--with-dods-root=no',
            '--with-spatialite=no',
            '--with-rasterlite2=no',
            '--with-teigha=no',
            '--with-idb=no',
            '--with-sde=no',
            '--with-epsilon=no',
            '--with-webp=no',
            '--with-sfcgal=no',
            '--with-freexl=no',
            '--with-pam=no',
            '--with-podofo=no',
            '--with-pdfium=no',
            '--with-php=no',
            '--with-mdb=no',
            '--with-rasdaman=no',
            '--with-mrf=no',
        ])

        return args

    @run_after('install')
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if sys.platform == 'darwin':
            fix_darwin_install_name(self.prefix.lib)
