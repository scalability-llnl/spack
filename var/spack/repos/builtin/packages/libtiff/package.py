# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libtiff(AutotoolsPackage):
    """LibTIFF - Tag Image File Format (TIFF) Library and Utilities."""

    homepage = "http://www.simplesystems.org/libtiff/"
    url      = "http://download.osgeo.org/libtiff/tiff-4.0.10.tar.gz"

    version('4.0.10', sha256='2c52d11ccaf767457db0c46795d9c7d1a8d8f76f68b0b800a3dfe45786b996e4')
    version('4.0.9', sha256='6e7bdeec2c310734e734d19aae3a71ebe37a4d842e0e23dbb1b8921c0026cfcd')
    version('4.0.8', sha256='59d7a5a8ccd92059913f246877db95a2918e6c04fb9d43fd74e5c3390dac2910')
    version('4.0.7', sha256='9f43a2cfb9589e5cecaa66e16bf87f814c945f22df7ba600d63aac4632c4f019')
    version('4.0.6', sha256='4d57a50907b510e3049a4bba0d7888930fdfc16ce49f1bf693e5b6247370d68c')
    version('4.0.3', md5='051c1068e6a0627f461948c365290410')
    version('3.9.7', sha256='f5d64dd4ce61c55f5e9f6dc3920fbe5a41e02c2e607da7117a35eb5c320cef6a')

    depends_on('jpeg')
    depends_on('zlib')
    depends_on('xz')
