# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsToolbelt(PythonPackage):
    """A toolbelt of useful classes and functions to be used with
    python-requests"""

    homepage = "https://toolbelt.readthedocs.org/"
    url      = "https://pypi.io/packages/source/r/requests-toolbelt/requests-toolbelt-0.9.1.tar.gz"

    version('0.9.1', sha256='968089d4584ad4ad7c171454f0a5c6dac23971e9472521ea3b6d49d610aa6fc0')
    version('0.8.0', sha256='f6a531936c6fa4c6cfce1b9c10d5c4f498d16528d2a54a22ca00011205a187b5')

    depends_on('py-setuptools', type='build')
    depends_on('py-requests@2.0.1:2.999', type=('build', 'run'))
