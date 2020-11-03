# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyIpyparallel(PythonPackage):
    """IPython's architecture for parallel and distributed computing."""

    homepage = "https://github.com/ipython/ipyparallel"
    url      = "https://github.com/ipython/ipyparallel/archive/6.3.0.tar.gz"

    version('6.3.0', sha256='b18f6e10ffbcf6f97cac9ce6edc32365302e8496a5252407b91c61b654882147')
    version('6.2.5', sha256='f6de54a29f7beb97872aa49dfa606dea5f3ed20d2433e3a7200ac2ea9b2a4388')
    version('6.2.4', sha256='84aa117647b358133643aad1082ea8a56ab8a17693cc3bc2b150746a37e7332e')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-ipython-genutils', type=('build', 'run'))
    depends_on('py-decorator', type=('build', 'run'))
    depends_on('py-pyzmq@13:', type=('build', 'run'))
    depends_on('py-traitlets@4.3:', type=('build', 'run'))
    depends_on('py-ipython@4:', type=('build', 'run'))
    depends_on('py-jupyter-client', type=('build', 'run'))
    depends_on('py-ipykernel@4.4:', type=('build', 'run'))
    depends_on('py-python-dateutil@2.1:', type=('build', 'run'))
    depends_on('py-tornado@4:', type=('build', 'run'))
