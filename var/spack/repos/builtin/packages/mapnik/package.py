# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Mapnik(AutotoolsPackage):
    """
    mapnik combines pixel-perfect image output with lightning-fast
    cartographic algorithms, and exposes interfaces in C++, Python, and Node
    """

    homepage = "https://mapnik.org/"
    url      = "https://github.com/mapnik/mapnik/releases/download/v3.0.22/mapnik-v3.0.22.tar.bz2"

    version('3.0.22', sha256='930612ad9e604b6a29b9cea1bc1de85cf7cf2b2b8211f57ec8b6b94463128ab9')

    depends_on('python', type=('build', 'run'))
    # Build fails with boost@1.70
    depends_on('boost@:1.69.0+regex+filesystem+system+icu+program_options cxxstd=11')
    depends_on('icu4c')
    depends_on('zlib')
    depends_on('freetype')
    depends_on('libxml2')
    depends_on('harfbuzz')
    depends_on('libpng')
    depends_on('libjpeg')
    depends_on('libtiff')
    depends_on('proj')
    depends_on('cairo')
    depends_on('postgresql', type=('build', 'link', 'run'))
    depends_on('gdal', type=('build', 'link', 'run'))
    depends_on('sqlite+rtree', type=('build', 'link', 'run'))
    depends_on('libwebp')

    conflicts('%gcc@9.0.0:')

    def setup_environment(self, spack_env, run_env):
        spec = self.spec
        spack_env.set('GDAL_DATA', spec['gdal'].prefix.share.gdal)

    def configure_args(self):
        return [
            'CXXFLAGS="-std=c++11"',
            'PREFIX=' + self.prefix,
            'BOOST_INCLUDES=' + self.spec['boost'].prefix.include,
            'BOOST_LIBS=' + self.spec['boost'].prefix.lib.directories[0],
            'PROJ_INCLUDES=' + self.spec['proj'].prefix.include,
            'PROJ_LIBS=' + self.spec['proj'].prefix.lib.directories[0],
            'CAIRO_INCLUDES=' + self.spec['cairo'].prefix.include,
            'CAIRO_LIBS=' + self.spec['cairo'].prefix.lib.directories[0],
        ]
