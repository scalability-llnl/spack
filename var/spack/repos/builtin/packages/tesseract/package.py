# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tesseract(AutotoolsPackage):
    """Tesseract Open Source OCR Engine."""

    homepage = "https://github.com/tesseract-ocr/tesseract"
    url      = "https://github.com/tesseract-ocr/tesseract/archive/4.1.1.tar.gz"

    version('4.1.1',       sha256='2a66ff0d8595bff8f04032165e6c936389b1e5727c3ce5a27b3e059d218db1cb')
    version('4.1.0',       sha256='5c5ed5f1a76888dc57a83704f24ae02f8319849f5c4cf19d254296978a1a1961')
    version('4.0.0',       sha256='a1f5422ca49a32e5f35c54dee5112b11b99928fc9f4ee6695cdc6768d69f61dd')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('leptonica')
    depends_on('libarchive')

    @when('@:4.0.0')
    def configure_args(self):
        args = ['LDFLAGS=-lz']
        return args
