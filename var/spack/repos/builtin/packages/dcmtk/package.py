# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dcmtk(CMakePackage):
    """DCMTK is a collection of libraries and applications implementing large
       parts of the DICOM standard."""

    homepage = "https://dicom.offis.de"
    url      = "https://github.com/DCMTK/dcmtk/archive/DCMTK-3.6.3.tar.gz"

    version('3.6.3', sha256='57f4f71ee4af9114be6408ff6fcafc441c349e4c2954e17c9c22c8ce0fb065bf')
    version('3.6.2', sha256='e9bf6e8805bbcf8a25274566541798785fd4e73bd046045ef27a0109ab520924')

    variant('ssl', default=True, description="Suuport DICOM Security Enhancements one")
    depends_on('openssl', type=('build', 'link'), when="+ssl")

    variant('zlib', default=True, description="Support 'Deflated Explicit VR Little Endian' Transfer Syntax")
    depends_on('zlib', type=('build', 'link'), when="+zlib")

    variant('tiff', default=True, description="Support for TIFF output")
    depends_on('libtiff', type=('build', 'link'), when='+tiff')

    variant('png', default=True, description="Support for PNG output")
    depends_on('libpng', type=('build', 'link'), when='+png')

    variant('xml', default=True, description="Support for XML input")
    depends_on('libxml2', type=('build', 'link'), when='+xml')

    variant('iconv', default=True, description="Charset conversion support (iconv)")
    depends_on('iconv', type=('build', 'link'))

    variant('cxx11', default=False, description="Enable c++11 features")
    variant('stl', default=True, description="Use native STL implementation")

    def patch(self):
        # Backport 3.6.4
        if self.spec.satisfies('@:3.6.3 %fj'):
            filter_file(
                'OFintegral_constant<size_t,-1>',
                'OFintegral_constant<size_t,~OFstatic_cast(size_t,0)>',
                'ofstd/include/dcmtk/ofstd/variadic/helpers.h',
                string=True
            )

    def cmake_args(self):
        args = ["-DDCMTK_WITH_OPENSSL={0}".format(
            'ON' if '+ssl' in self.spec else 'OFF')]
        args += ["-DDCMTK_WITH_ZLIB={0}".format(
            'ON' if '+zlib' in self.spec else 'OFF')]
        args += ["-DDCMTK_WITH_TIFF={0}".format(
            'ON' if '+tiff' in self.spec else 'OFF')]
        args += ["-DDCMTK_WITH_PNG={0}".format(
            'ON' if '+png' in self.spec else 'OFF')]
        args += ["-DDCMTK_WITH_XML={0}".format(
            'ON' if '+xml' in self.spec else 'OFF')]
        args += ["-DDCMTK_WITH_ICONV={0}".format(
            'ON' if '+iconv' in self.spec else 'OFF')]
        args += ["-DDCMTK_ENABLE_CXX11={0}".format(
            'ON' if '+cxx11' in self.spec else 'OFF')]
        args += ["-DDCMTK_ENABLE_STL={0}".format(
            'ON' if '+stl' in self.spec else 'OFF')]
        return args
