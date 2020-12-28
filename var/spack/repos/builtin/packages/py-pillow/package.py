# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPillowBase(PythonPackage):
    """Base class for Pillow and its fork Pillow-SIMD."""

    maintainers = ['adamjstewart']

    provides('pil')

    # These defaults correspond to Pillow defaults
    # https://pillow.readthedocs.io/en/stable/installation.html#external-libraries
    variant('zlib',       default=True,  description='Compressed PNG functionality')
    variant('jpeg',       default=True,  description='JPEG functionality')
    variant('tiff',       default=False, description='Compressed TIFF functionality')
    variant('freetype',   default=False, description='Type related services')
    variant('lcms',       default=False, description='Color management')
    variant('webp',       default=False, description='WebP format')
    variant('webpmux',    default=False, description='WebP metadata')
    variant('jpeg2000',   default=False, description='JPEG 2000 functionality')
    variant('imagequant', default=False, description='Improved color quantization')
    variant('xcb',        default=False, description='X11 screengrab support')

    # Required dependencies
    # https://pillow.readthedocs.io/en/latest/installation.html#notes
    depends_on('python@3.6:3.9',         when='@8:',          type=('build', 'run'))
    depends_on('python@3.5:3.8',         when='@7.0:7.2',     type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:3.8', when='@6.2.1:6.2.2', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:3.7', when='@6.0:6.2.0',   type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:3.7', when='@5.2:5.4',     type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:3.6', when='@5.0:5.1',     type=('build', 'run'))
    depends_on('python@2.7:2.8,3.3:3.6', when='@4.0:4.999',   type=('build', 'run'))
    depends_on('python@2.6:2.8,3.2:3.5', when='@2:3',         type=('build', 'run'))
    depends_on('python@2.4:2.7',         when='@:1',          type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    # Optional dependencies
    depends_on('zlib', when='+zlib')
    depends_on('jpeg', when='+jpeg')
    depends_on('libtiff', when='+tiff')
    depends_on('freetype', when='+freetype')
    depends_on('lcms@2:', when='+lcms')
    depends_on('libwebp', when='+webp')
    depends_on('libwebp+libwebpmux+libwebpdemux', when='+webpmux')
    depends_on('openjpeg', when='+jpeg2000')
    depends_on('libimagequant', when='+imagequant')
    depends_on('libxcb', when='+xcb')

    conflicts('+webpmux', when='~webp', msg='Webpmux relies on WebP support')
    conflicts('+imagequant', when='@:3.2', msg='imagequant support was added in 3.3')
    conflicts('+xcb', when='@:7.0', msg='XCB support was added in 7.1')

    phases = ['build_ext', 'install']

    def patch(self):
        """Patch setup.py to provide library and include directories
        for dependencies."""

        library_dirs = []
        include_dirs = []
        for dep in self.spec.dependencies(deptype='link'):
            query = self.spec[dep.name]
            library_dirs.extend(query.libs.directories)
            include_dirs.extend(query.headers.directories)

        setup = FileFilter('setup.py')
        setup.filter('library_dirs = []',
                     'library_dirs = {0}'.format(library_dirs), string=True)
        setup.filter('include_dirs = []',
                     'include_dirs = {0}'.format(include_dirs), string=True)

        def variant_to_cfg(variant):
            able = 'enable' if '+' + variant in self.spec else 'disable'
            return '{0}-{1}=1\n'.format(able, variant)

        with open('setup.cfg', 'a') as setup:
            setup.write('[build_ext]\n')
            variants = list(self.spec.variants)

            if self.spec.satisfies('@:7.0'):
                variants.remove('xcb')
            if self.spec.satisfies('@:3.2'):
                variants.remove('imagequant')

            for variant in variants:
                setup.write(variant_to_cfg(variant))

            setup.write('rpath={0}\n'.format(':'.join(self.rpath)))
            setup.write('[install]\n')

    def setup_build_environment(self, env):
        env.set('MAX_CONCURRENCY', str(make_jobs))

    # Tests need to be re-added since `phases` was overridden
    run_after('install')(
        PythonPackage._run_default_install_time_test_callbacks)
    run_after('install')(PythonPackage.sanity_check_prefix)


class PyPillow(PyPillowBase):
    """Pillow is a fork of the Python Imaging Library (PIL). It adds image
    processing capabilities to your Python interpreter. This library supports
    many file formats, and provides powerful image processing and graphics
    capabilities."""

    homepage = "https://python-pillow.org/"
    url      = "https://pypi.io/packages/source/P/Pillow/Pillow-7.2.0.tar.gz"

    version('8.0.0', sha256='59304c67d12394815331eda95ec892bf54ad95e0aa7bc1ccd8e0a4a5a25d4bf3')
    version('7.2.0', sha256='97f9e7953a77d5a70f49b9a48da7776dc51e9b738151b22dacf101641594a626')
    version('7.0.0', sha256='4d9ed9a64095e031435af120d3c910148067087541131e82b3e8db302f4c8946')
    version('6.2.2', sha256='db9ff0c251ed066d367f53b64827cc9e18ccea001b986d08c265e53625dab950')
    version('6.2.1', sha256='bf4e972a88f8841d8fdc6db1a75e0f8d763e66e3754b03006cbc3854d89f1cb1')
    version('6.2.0', sha256='4548236844327a718ce3bb182ab32a16fa2050c61e334e959f554cac052fb0df')
    version('6.0.0', sha256='809c0a2ce9032cbcd7b5313f71af4bdc5c8c771cb86eb7559afd954cab82ebb5')
    version('5.4.1', sha256='5233664eadfa342c639b9b9977190d64ad7aca4edc51a966394d7e08e7f38a9f')
    version('5.1.0', sha256='cee9bc75bff455d317b6947081df0824a8f118de2786dc3d74a3503fd631f4ef')
    version('3.2.0', sha256='64b0a057210c480aea99406c9391180cd866fc0fd8f0b53367e3af21b195784a')
    version('3.0.0', sha256='ad50bef540fe5518a4653c3820452a881b6a042cb0f8bb7657c491c6bd3654bb')

    for ver in [
        '7.2.0', '7.0.0', '6.2.2', '6.2.1', '6.2.0', '6.0.0',
        '5.4.1', '5.1.0', '3.2.0', '3.0.0'
    ]:
        provides('pil@' + ver, when='@' + ver)
