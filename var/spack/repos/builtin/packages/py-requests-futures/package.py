# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRequestsFutures(PythonPackage):
    """Asynchronous Python HTTP Requests for Humans using Futures"""

    homepage = "https://github.com/ross/requests-futures"
    url      = "https://pypi.io/packages/source/r/requests-futures/requests-futures-1.0.0.tar.gz"

    version('1.0.0', sha256='35547502bf1958044716a03a2f47092a89efe8f9789ab0c4c528d9c9c30bc148')

    depends_on('py-setuptools@38.6.1:', type='build')
    depends_on('py-futures@2.1.3:', type=('build', 'run'), when='^python@:3.1')
    depends_on('py-requests@1.2.0:', type=('build', 'run'))
