# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHpack(PythonPackage):
    """Pure-Python HPACK header compression"""

    homepage = "https://github.com/python-hyper/hpack"
    url      = "https://pypi.io/packages/source/h/hpack/hpack-4.0.0.tar.gz"

    version('4.0.0', sha256='fc41de0c63e687ebffde81187a948221294896f6bdc0ae2312708df339430095')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
