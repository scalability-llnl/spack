# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPytest(PythonPackage):
    """pytest: simple powerful testing with Python."""

    homepage = "http://pytest.org/"
    url      = "https://pypi.io/packages/source/p/pytest/pytest-5.2.1.tar.gz"

    version('5.3.4', sha256='1d122e8be54d1a709e56f82e2d85dcba3018313d64647f38a91aec88c239b600')
    version('5.2.1', sha256='ca563435f4941d0cb34767301c27bc65c510cb82e90b9ecf9cb52dc2c63caaa0')
    version('5.1.1', sha256='c3d5020755f70c82eceda3feaf556af9a341334414a8eca521a18f463bcead88')
    version('4.6.9', sha256='19e8f75eac01dd3f211edd465b39efbcbdc8fc5f7866d7dd49fedb30d8adf339')
    version('4.6.5', sha256='8fc39199bdda3d9d025d3b1f4eb99a192c20828030ea7c9a0d2840721de7d347')
    version('4.6.2', sha256='bea27a646a3d74cbbcf8d3d4a06b2dfc336baf3dc2cc85cf70ad0157e73e8322')
    version('4.3.0', sha256='067a1d4bf827ffdd56ad21bd46674703fce77c5957f6c1eef731f6146bfcef1c')
    version('3.7.2', sha256='3459a123ad5532852d36f6f4501dfe1acf4af1dd9541834a164666aa40395b02')
    version('3.7.1', sha256='86a8dbf407e437351cef4dba46736e9c5a6e3c3ac71b2e942209748e76ff2086')
    version('3.5.1', sha256='54713b26c97538db6ff0703a12b19aeaeb60b5e599de542e7fca0ec83b9038e8')
    version('3.0.7', sha256='b70696ebd1a5e6b627e7e3ac1365a4bc60aaf3495e843c1e70448966c5224cab')
    version('3.0.2', sha256='64d8937626dd2a4bc15ef0edd307d26636a72a3f3f9664c424d78e40efb1e339')

    depends_on('python@3.5:', when='@5:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', when='@3.3:4', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.3:', when='@:3.2', type=('build', 'run'))

    # Most Python packages only require setuptools as a build dependency.
    # However, pytest requires setuptools during runtime as well.
    # FIXME: May no longer be needed at runtime, see:
    # https://github.com/pytest-dev/pytest/pull/5063
    depends_on('py-setuptools@40.0:', when='@3.9.2:', type=('build', 'run'))
    depends_on('py-setuptools@30.3:', when='@3.9.0:3.9.1', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-setuptools-scm', when='@3.1:', type='build')
    depends_on('py-py@1.5.0:', when='@3.3:', type=('build', 'run'))
    depends_on('py-py@1.4.33:', when='@3.1.2:3.2.3,3.2.5:3.2.999', type=('build', 'run'))
    depends_on('py-py@1.4.33:1.4.999', when='@3.2.4', type=('build', 'run'))
    depends_on('py-py@1.4.29:', when='@:3.1.1', type=('build', 'run'))
    depends_on('py-six@1.10.0:', when='@3.3:4', type=('build', 'run'))
    depends_on('py-packaging', when='@4.6:', type=('build', 'run'))
    depends_on('py-attrs@17.2.0:', when='@3.3:3.4', type=('build', 'run'))
    depends_on('py-attrs@17.4.0:', when='@3.5:', type=('build', 'run'))
    depends_on('py-more-itertools@4.0.0:', when='@3.5.1:', type=('build', 'run'))
    depends_on('py-more-itertools@4.0.0:6.0.0', when='@4.2.1:4.6.9 ^python@:2', type=('build', 'run'))
    depends_on('py-atomicwrites@1.0:', when='@3.6:5.2.999', type=('build', 'run'))
    depends_on('py-pluggy@0.12:0.999', when='@4.6:', type=('build', 'run'))
    depends_on('py-pluggy@0.9.0:0.9.999,0.11:0.999', when='@4.5.0:4.5.999', type=('build', 'run'))
    depends_on('py-pluggy@0.11:', when='@4.4.2:4.4.999', type=('build', 'run'))
    depends_on('py-pluggy@0.9:', when='@4.4.0:4.4.1', type=('build', 'run'))
    depends_on('py-pluggy@0.7:', when='@3.7:4.3', type=('build', 'run'))
    depends_on('py-pluggy@0.5:0.7', when='@3.6.4:3.6.999', type=('build', 'run'))
    depends_on('py-pluggy@0.5:0.6', when='@:3.6.3', type=('build', 'run'))
    depends_on('py-funcsigs@1.0:', when='@4.4: ^python@:2', type=('build', 'run'))
    depends_on('py-funcsigs', when='@3.3:4.3 ^python@:2', type=('build', 'run'))
    depends_on('py-pathlib2@2.2.0:', when='@3.7.1: ^python@:3.5', type=('build', 'run'))
    depends_on('py-pathlib2', when='@3.7.0 ^python@:3.5', type=('build', 'run'))
    depends_on('py-importlib-metadata@0.12:', when='@4.6:5.0', type=('build', 'run'))
    depends_on('py-importlib-metadata@0.12:', when='@5.1: ^python@:3.7', type=('build', 'run'))
    depends_on('py-wcwidth', when='@4.5:', type=('build', 'run'))
