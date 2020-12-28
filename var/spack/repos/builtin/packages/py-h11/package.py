# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyH11(PythonPackage):
    """A pure-Python, bring-your-own-I/O implementation of HTTP/1.1"""

    homepage = "https://github.com/python-hyper/h11"
    url      = "https://pypi.io/packages/source/h/h11/h11-0.10.0.tar.gz"

    version('0.10.0', sha256='311dc5478c2568cc07262e0381cdfc5b9c6ba19775905736c87e81ae6662b9fd')
    version('0.9.0', sha256='33d4bca7be0fa039f4e84d50ab00531047e53d6ee8ffbc83501ea602c169cae1')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
