# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRgl(RPackage):
    """Provides medium to high level functions for 3D interactive graphics,
    including functions modelled on base graphics (plot3d(), etc.) as well as
    functions for constructing representations of geometric objects (cube3d(),
    etc.). Output may be on screen using OpenGL, or to various standard
    3D file formats including WebGL, PLY, OBJ, STL as well as 2D image formats,
    including PNG, Postscript, SVG, PGF."""

    homepage = "https://r-forge.r-project.org/projects/rgl"
    url      = "https://cloud.r-project.org/src/contrib/rgl_0.99.16.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rgl"

    version('0.100.26', sha256='e1889c2723ad458b39fdf9366fdaf590d7657d3762748f8534a8491ef754e740')
    version('0.100.24', sha256='1233a7bdc5a2b908fc64d5f56e92a0e123e8f7c0b9bac93dfd005608b78fa35a')
    version('0.100.19', sha256='50630702554e422e0603f27d499aad3b6f822de5a73da7fdf70404ac50df7025')
    version('0.99.16', sha256='692a545ed2ff0f5e15289338736f0e3c092667574c43ac358d8004901d7a1a61')
    version('0.98.1', sha256='5f49bed9e092e672f73c8a1a5365cdffcda06db0315ac087e95ab9c9c71a6986')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r-htmlwidgets', type=('build', 'run'))
    depends_on('r-htmltools', type=('build', 'run'))
    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-jsonlite@0.9.20:', type=('build', 'run'))
    depends_on('r-shiny', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-crosstalk', when='@0.99.16:', type=('build', 'run'))
    depends_on('r-manipulatewidget@0.9.0:', when='@0.99.16:', type=('build', 'run'))
    depends_on('zlib', type='link')
    depends_on('libpng@1.2.9:', type='link')
    depends_on('libx11')
    depends_on('freetype', type='link')
    depends_on('gl')
    depends_on('glu')
    depends_on('pandoc@1.14:', type='build')

    def configure_args(self):
        args = ['--x-includes=%s' % self.spec['libx11'].prefix.include,
                '--x-libraries=%s' % self.spec['libx11'].prefix.lib,
                '--with-gl-includes=%s' % self.spec['gl'].prefix.include,
                '--with-gl-libraries=%s' % self.spec['gl'].prefix.lib,
                '--with-gl-prefix=%s' % self.spec['gl'].prefix]
        return args
