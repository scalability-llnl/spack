# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttpx(PythonPackage):
    """HTTPX is a fully featured HTTP client for Python 3, which provides sync
    and async APIs, and support for both HTTP/1.1 and HTTP/2."""

    homepage = "https://github.com/encode/httpx"
    url      = "https://pypi.io/packages/source/h/httpx/httpx-0.15.2.tar.gz"

    version('0.15.2', sha256='713a2deaf96d85bbd4a1fbdf0edb27d6b4ee2c9aaeda8433042367e4b9e1628d')
    version('0.11.1', sha256='7d2bfb726eeed717953d15dddb22da9c2fcf48a4d70ba1456aa0a7faeda33cf7')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-certifi')
    depends_on('py-sniffio')
    depends_on('py-httpcore@0.11:')
    depends_on('py-rfc3986+idna2008@1.3:1.99')
