# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qhull(CMakePackage):
    """Qhull computes the convex hull, Delaunay triangulation, Voronoi
       diagram, halfspace intersection about a point, furt hest-site
       Delaunay triangulation, and furthest-site Voronoi diagram. The
       source code runs in 2-d, 3-d, 4-d, and higher dimensions. Qhull
       implements the Quickhull algorithm for computing the convex
       hull. It handles roundoff errors from floating point
       arithmetic. It computes volumes, surface areas, and
       approximations to the convex hull."""

    homepage = "http://www.qhull.org"

    version('2020.1', sha256='1ac92a5538f61e297c72aebe4d4ffd731ceb3e6045d6d15faf1c212713798df4',
            url="http://www.qhull.org/download/qhull-2020-src-8.0.0.tgz")
    version('2019.1', sha256='2b7990558c363076261564f61b74db4d0d73b71869755108a469038c07dc43fb',
            url="http://www.qhull.org/download/qhull-2019-src-7.3.2.tgz")
    version('2015.2', sha256='78b010925c3b577adc3d58278787d7df08f7c8fb02c3490e375eab91bb58a436',
            url="http://www.qhull.org/download/qhull-2015-src-7.2.0.tgz")
    version('2012.1', sha256='a35ecaa610550b7f05c3ce373d89c30cf74b059a69880f03080c556daebcff88',
            url="http://www.qhull.org/download/qhull-2012.1-src.tgz")

    patch('qhull-unused-intel-17.02.patch', when='@2015.2')

    depends_on('cmake@3.0:', type='build')

    def flag_handler(self, name, flags):
        # See https://github.com/qhull/qhull/issues/65
        if name == 'cxxflags' and self.version == Version('2020.1'):
            flags.append(self.compiler.cxx11_flag)
        return (flags, None, None)
