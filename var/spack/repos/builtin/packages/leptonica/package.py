# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Leptonica(CMakePackage):
    """Leptonica is an open source library containing software that is
    broadly useful for image processing and image analysis applications."""

    homepage = "http://www.leptonica.org/"
    url      = "https://github.com/DanBloomberg/leptonica/archive/1.80.0.tar.gz"

    version('1.80.0', sha256='3952b974ec057d24267aae48c54bca68ead8275604bf084a73a4b953ff79196e')
    version('1.79.0', sha256='bf9716f91a4844c2682a07ef21eaf68b6f1077af1f63f27c438394fd66218e17')
    version('1.78.0', sha256='f8ac4d93cc76b524c2c81d27850bfc342e68b91368aa7a1f7d69e34ce13adbb4')

    depends_on('zlib')

    def cmake_args(self):
        args = ['-DCMAKE_C_FLAGS=' + self.compiler.cc_pic_flag]
        return args
