# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Opencascade(CMakePackage):
    """Open CASCADE Technology is a software development kit (SDK)
    intended for development of applications dealing with 3D CAD data,
    freely available in open source. It includes a set of C++ class
    libraries providing services for 3D surface and solid modeling,
    visualization, data exchange and rapid application development."""

    homepage = "https://www.opencascade.com"
    url      = "http://git.dev.opencascade.org/gitweb/?p=occt.git;a=snapshot;h=refs/tags/V7_4_0;sf=tgz"

    version('7.4.0p1', extension='tar.gz',
            sha256='e00fedc221560fda31653c23a8f3d0eda78095c87519f338d4f4088e2ee9a9c0')
    version('7.4.0', extension='tar.gz',
            sha256='655da7717dac3460a22a6a7ee68860c1da56da2fec9c380d8ac0ac0349d67676')

    variant('tbb', default=False,
            description='Build with Intel Threading Building Blocks')
    variant('vtk', default=False,
            description='Enable VTK support')
    variant('freeimage', default=False,
            description='Build with FreeImage')
    variant('rapidjson', default=False,
            description='Build with rapidjson')

    depends_on('intel-tbb', when='+tbb')
    depends_on('vtk', when='+vtk')
    depends_on('freeimage', when='+freeimage')
    depends_on('rapidjson', when='+rapidjson')
    depends_on('freetype')
    depends_on('libxext')
    depends_on('libxmu')
    depends_on('libxi')
    depends_on('libxt')
    depends_on('tcl')
    depends_on('tk')
    depends_on('gl')

    def url_for_version(self, version):
        url = "http://git.dev.opencascade.org/gitweb/?p=occt.git;a=snapshot;h=refs/tags/V{0};sf=tgz"
        return url.format(version.underscored)

    def cmake_args(self):
        args = []

        if '+tbb' in self.spec:
            args.append('-DUSE_TBB=ON')
            args.append('-D3RDPARTY_VTK_DIR=%s' %
                        self.spec['intel-tbb'].prefix)
        else:
            args.append('-DUSE_TBB=OFF')

        if '+vtk' in self.spec:
            args.append('-DUSE_VTK=ON')
            args.append('-D3RDPARTY_VTK_DIR=%s' %
                        self.spec['vtk'].prefix)
        else:
            args.append('-DUSE_VTK=OFF')

        if '+freeimage' in self.spec:
            args.append('-DUSE_FREEIMAGE=ON')
            args.append('-D3RDPARTY_FREEIMAGE_DIR=%s' %
                        self.spec['freeimage'].prefix)
        else:
            args.append('-DUSE_FREEIMAGE=OFF')

        if '+rapidjson' in self.spec:
            args.append('-DUSE_RAPIDJSON=ON')
            args.append('-D3RDPARTY_RAPIDJSON_DIR=%s' %
                        self.spec['rapidjson'].prefix)
        else:
            args.append('-DUSE_RAPIDJSON=OFF')

        return args
