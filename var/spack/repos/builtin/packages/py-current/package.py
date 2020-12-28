# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCurrent(PythonPackage):
    """Current module relative paths and imports"""

    homepage = "http://github.com/xflr6/current"
    url      = "https://pypi.io/packages/source/c/current/current-0.3.1.zip"

    version('0.3.1', sha256='207613dc19a6cc8e1a756f26e416733c8f82a70e4ae81103d22f483aae6492a8')

    depends_on('py-setuptools', type='build')
