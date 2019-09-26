# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys


class PyPillow(PythonPackage):
    """Pillow is a fork of the Python Imaging Library (PIL). It adds image
    processing capabilities to your Python interpreter. This library supports
    many file formats, and provides powerful image processing and graphics
    capabilities."""

    homepage = "https://python-pillow.org/"
    url = "https://pypi.io/packages/source/P/Pillow/Pillow-5.1.0.tar.gz"

    version('5.4.1', 'f7d0ce066fc7ea7a685739227887aeaf')
    version('5.1.0', '308f9c13b376abce96ab6ebd6c889cc4')
    version('3.2.0', '7cfd093c11205d9e2ebe3c51dfcad510')
    version('3.0.0', 'fc8ac44e93da09678eac7e30c9b7377d')

    provides('pil')

    # These defaults correspond to Pillow defaults
    variant('jpeg', default=True, description='Provide JPEG functionality')
    variant('zlib', default=True, description='Access to compressed PNGs')
    variant('tiff', default=False, description='Access to TIFF files')
    variant('freetype', default=False, description='Font related services')
    variant('lcms', default=False, description='Color management')
    variant('jpeg2000', default=False, description='Provide JPEG 2000 functionality')

    # Spack does not (yet) support these modes of building
    # variant('webp', default=False, description='Provide the WebP format')
    # variant('webpmux', default=False,
    #         description='WebP metadata, relies on WebP support')
    # variant('imagequant', default=False,
    #         description='Provide improved color quantization')

    # Required dependencies
    depends_on('binutils', type='build', when=sys.platform != 'darwin')
    depends_on('py-setuptools', type='build')

    # Recommended dependencies
    depends_on('jpeg', when='+jpeg')
    depends_on('zlib', when='+zlib')

    # Optional dependencies
    depends_on('libtiff', when='+tiff')
    depends_on('freetype', when='+freetype')
    depends_on('lcms', when='+lcms')
    depends_on('openjpeg', when='+jpeg2000')

    # Spack does not (yet) support these modes of building
    # depends_on('webp', when='+webp')
    # depends_on('webpmux', when='+webpmux')
    # depends_on('imagequant', when='+imagequant')

    phases = ['build_ext', 'install']

    def patch(self):
        """Patch setup.py to provide lib and include directories
        for dependencies."""

        spec = self.spec
        setup = FileFilter('setup.py')

        if '+jpeg' in spec:
            setup.filter('JPEG_ROOT = None',
                         'JPEG_ROOT=("{0}","{1}")'.format(
                             spec['jpeg'].libs.directories[0],
                             spec['jpeg'].prefix.include))
        if '+zlib' in spec:
            setup.filter('ZLIB_ROOT = None',
                         'ZLIB_ROOT = ("{0}", "{1}")'.format(
                             spec['zlib'].prefix.lib,
                             spec['zlib'].prefix.include))
        if '+tiff' in spec:
            setup.filter('TIFF_ROOT = None',
                         'TIFF_ROOT = ("{0}", "{1}")'.format(
                             spec['libtiff'].prefix.lib,
                             spec['libtiff'].prefix.include))
        if '+freetype' in spec:
            setup.filter('FREETYPE_ROOT = None',
                         'FREETYPE_ROOT = ("{0}", "{1}")'.format(
                             spec['freetype'].prefix.lib,
                             spec['freetype'].prefix.include))
        if '+lcms' in spec:
            setup.filter('LCMS_ROOT = None',
                         'LCMS_ROOT = ("{0}", "{1}")'.format(
                             spec['lcms'].prefix.lib,
                             spec['lcms'].prefix.include))
        if '+jpeg2000' in spec:
            setup.filter('JPEG2K_ROOT = None',
                         'JPEG2K_ROOT = ("{0}", "{1}")'.format(
                             spec['openjpeg'].prefix.lib,
                             spec['openjpeg'].prefix.include))

    def build_ext_args(self, spec, prefix):
        def variant_to_flag(variant):
            able = 'enable' if '+{0}'.format(variant) in spec else 'disable'
            return '--{0}-{1}'.format(able, variant)

        variants = ['jpeg', 'zlib', 'tiff', 'freetype', 'lcms', 'jpeg2000']
        args = list(map(variant_to_flag, variants))
        args.extend(['--rpath=%s' % ":".join(self.rpath)])
        return args
