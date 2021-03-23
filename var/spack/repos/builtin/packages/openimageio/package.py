# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.boost import Boost


class Openimageio(CMakePackage):
    """OpenImageIO is a library for reading and writing images, and a bunch of
       related classes, utilities, and applications."""

    homepage = "http://www.openimageio.org"
    url      = "https://github.com/OpenImageIO/oiio/archive/Release-1.8.15.tar.gz"

    version('2.2.7.0', sha256='857ac83798d6d2bda5d4d11a90618ff19486da2e5a4c4ff022c5976b5746fe8c')
    version('1.8.15', sha256='4d5b4ed3f2daaed69989f53c0f9364dd87c82dc0a09807b5b6e9008e2426e86f')

    # Core dependencies
    depends_on('cmake@3.2.2:', type='build')
    depends_on('boost@1.53:', type=('build', 'link'))

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, type=('build', 'link'))
    depends_on('libtiff@4.0:', type=('build', 'link'))
    depends_on('openexr@2.3:', type=('build', 'link'))
    depends_on('libpng@1.6:', type=('build', 'link'))

    # Optional dependencies
    variant('ffmpeg', default=False, description="Support video frames")
    depends_on('ffmpeg', when='+ffmpeg')

    variant('jpeg2k', default=False, description="Support for JPEG2000 format")
    depends_on('openjpeg', when='+jpeg2k')

    variant('python', default=False, description="Build python bindings")
    extends('python', when='+python')
    depends_on('py-numpy', when='+python', type=('build', 'run'))
    depends_on('py-pybind11', when='+python', type=('build', 'run'))

    variant('qt', default=False, description="Build qt viewer")
    depends_on('qt@5.6.0:+opengl', when='+qt')

    conflicts('target=aarch64:', when='@:1.8.15')

    def cmake_args(self):
        args = ["-DUSE_FFMPEG={0}".format(
            'ON' if '+ffmpeg' in self.spec else 'OFF')]
        args += ["-DUSE_OPENJPEG={0}".format(
            'ON' if '+jpeg2k' in self.spec else 'OFF')]
        args += ["-DUSE_PYTHON={0}".format(
            'ON' if '+python' in self.spec else 'OFF')]
        args += ["-DUSE_QT={0}".format('ON' if '+qt' in self.spec else 'OFF')]
        return args
