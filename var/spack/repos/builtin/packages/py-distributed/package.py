# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDistributed(PythonPackage):
    """Distributed scheduler for Dask"""

    homepage = "https://distributed.dask.org/"
    url      = "https://pypi.io/packages/source/d/distributed/distributed-2.10.0.tar.gz"

    version('2.10.0', sha256='2f8cca741a20f776929cbad3545f2df64cf60207fb21f774ef24aad6f6589e8b')
    version('1.28.1', sha256='3bd83f8b7eb5938af5f2be91ccff8984630713f36f8f66097e531a63f141c48a')

    depends_on('python@2.7:2.8,3.5:', when='@:1', type=('build', 'run'))
    depends_on('python@3.6:', when='@2:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@6.6:', type=('build', 'run'))
    depends_on('py-cloudpickle@0.2.2:', type=('build', 'run'))
    depends_on('py-msgpack', type=('build', 'run'))
    depends_on('py-psutil@5.0:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'), when='@:1')
    depends_on('py-sortedcontainers@:1.999,2.0.2:', type=('build', 'run'))
    depends_on('py-tblib', type=('build', 'run'))
    depends_on('py-toolz@0.7.4:', type=('build', 'run'))
    depends_on('py-tornado@5:', type=('build', 'run'))
    depends_on('py-zict@0.1.3:', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-futures', when='@:1 ^python@2.7:2.8', type=('build', 'run'))
    depends_on('py-singledispatch', when='@:1 ^python@2.7:2.8', type=('build', 'run'))

    def patch(self):
        filter_file('^dask .*', '', 'requirements.txt')
