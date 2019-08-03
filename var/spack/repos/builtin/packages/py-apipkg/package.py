# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyApipkg(PythonPackage):
    """apipkg: namespace control and lazy-import mechanism"""

    homepage = "https://pypi.python.org/pypi/apipkg"
    url      = "https://pypi.io/packages/source/a/apipkg/apipkg-1.4.tar.gz"

    version('1.5', sha256='2e38399dbe842891fe85392601aab8f40a8f4cc5a9053c326de35a1cc0297ac6')
    version('1.4', sha256='37228cda29411948b422fae072f57e31d3396d2ee1c9783775980ee9c9990af6')

    depends_on('py-setuptools', type='build')
