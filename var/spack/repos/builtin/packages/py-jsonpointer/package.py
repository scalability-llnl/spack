# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonpointer(PythonPackage):
    """Library to resolve JSON Pointers according to RFC 6901"""

    homepage = "https://github.com/stefankoegl/python-json-pointer"
    url      = "https://pypi.io/packages/source/j/jsonpointer/jsonpointer-2.0.tar.gz"

    version('2.0', sha256='c192ba86648e05fdae4f08a17ec25180a9aef5008d973407b581798a83975362')

    depends_on('py-setuptools', type='build')
