# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack import *


class Libspatialite(AutotoolsPackage):
    """SpatiaLite is an open source library intended to extend the
       SQLite core to support fully fledged Spatial SQL capabilities."""

    homepage = "http://www.gaia-gis.it"
    url      = "http://www.gaia-gis.it/gaia-sins/libspatialite-sources/libspatialite-4.3.0a.tar.gz"
    manual_download = True

    version('5.0.0', preferred=True, sha256='7b7fd70243f5a0b175696d87c46dde0ace030eacc27f39241c24bac5dfac6dac')
    # Must download manually from:
    #     https://www.gaia-gis.it/fossil/libspatialite/info/c7f67038bf06d98d
    # For instructions on the file:// below..
    #     https://github.com/spack/spack/issues/2489
    version('5.0.0.2.c7f67038bf',
            sha256='f8100f71b769c7db066c6f938af6b00e920e4b90ac14c00a4f3ed7171565caab',
            url="file://%s/SpatiaLite-c7f67038bf.tar.gz" % os.getcwd())

    version('5.0.0-beta0', sha256='caacf5378a5cfab9b8e98bb361e2b592e714e21f5c152b795df80d0ab1da1c42')
    version('4.3.0a',
            sha256='88900030a4762904a7880273f292e5e8ca6b15b7c6c3fb88ffa9e67ee8a5a499')
    version('3.0.1', sha256='4983d6584069fd5ff0cfcccccee1015088dab2db177c0dc7050ce8306b68f8e6')

    depends_on('pkgconfig', type='build')
    depends_on('sqlite+rtree')
    depends_on('proj@:5', when='@:4.999.999')
    # PROJ.6 is OK w/ newer versions
    # https://www.gaia-gis.it/fossil/libspatialite/wiki?name=PROJ.6
    depends_on('proj')
    depends_on('geos')
    depends_on('freexl')
    depends_on('iconv')
    depends_on('libxml2')
    depends_on('minizip', when='@5.0.0:')
