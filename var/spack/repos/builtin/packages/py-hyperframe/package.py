# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHyperframe(PythonPackage):
    """HTTP/2 framing layer for Python"""

    homepage = "https://github.com/python-hyper/hyperframe/"
    url      = "https://pypi.io/packages/source/h/hyperframe/hyperframe-6.0.0.tar.gz"

    version('6.0.0', sha256='742d2a4bc3152a340a49d59f32e33ec420aa8e7054c1444ef5c7efff255842f1')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
