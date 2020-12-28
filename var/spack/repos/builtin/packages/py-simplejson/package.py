# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySimplejson(PythonPackage):
    """Simplejson is a simple, fast, extensible JSON encoder/decoder for
    Python"""

    homepage = "https://github.com/simplejson/simplejson"
    url      = "https://pypi.io/packages/source/s/simplejson/simplejson-3.10.0.tar.gz"

    version('3.16.0', sha256='b1f329139ba647a9548aa05fb95d046b4a677643070dc2afc05fa2e975d09ca5')
    version('3.10.0', sha256='953be622e88323c6f43fad61ffd05bebe73b9fd9863a46d68b052d2aa7d71ce2')
    version('3.9.0',  sha256='e9abeee37424f4bfcd27d001d943582fb8c729ffc0b74b72bd0e9b626ed0d1b6')
    version('3.8.2',  sha256='d58439c548433adcda98e695be53e526ba940a4b9c44fb9a05d92cd495cdd47f')
    version('3.8.1',  sha256='428ac8f3219c78fb04ce05895d5dff9bd813c05a9a7922c53dc879cd32a12493')
    version('3.8.0',  sha256='217e4797da3a9a4a9fbe6722e0db98070b8443a88212d7acdbd241a7668141d9')

    depends_on('py-setuptools', type='build')
