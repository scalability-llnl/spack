# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyGrpcio(PythonPackage):
    """HTTP/2-based RPC framework."""

    homepage = "https://grpc.io/"
    url      = "https://pypi.io/packages/source/g/grpcio/grpcio-1.32.0.tar.gz"

    version('1.32.0', sha256='01d3046fe980be25796d368f8fc5ff34b7cf5e1444f3789a017a7fe794465639')
    version('1.30.0', sha256='e8f2f5d16e0164c415f1b31a8d9a81f2e4645a43d1b261375d6bab7b0adf511f')
    version('1.29.0', sha256='a97ea91e31863c9a3879684b5fb3c6ab4b17c5431787548fc9f52b9483ea9c25')
    version('1.27.2', sha256='5ae532b93cf9ce5a2a549b74a2c35e3b690b171ece9358519b3039c7b84c887e')
    version('1.25.0', sha256='c948c034d8997526011960db54f512756fb0b4be1b81140a15b4ef094c6594a4')

    depends_on('python@3.5:', when='@1.30:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.5.2:', type=('build', 'run'))
    depends_on('py-futures@2.2.0:', when='^python@:3.1', type=('build', 'run'))
    depends_on('py-enum34@1.0.4:', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-cython@0.23:', type='build')
    depends_on('openssl')
    depends_on('zlib')
    depends_on('c-ares')

    def setup_build_environment(self, env):
        env.set('GRPC_PYTHON_BUILD_WITH_CYTHON', True)
        env.set('GRPC_PYTHON_BUILD_SYSTEM_OPENSSL', True)
        env.set('GRPC_PYTHON_BUILD_SYSTEM_ZLIB', True)
        env.set('GRPC_PYTHON_BUILD_SYSTEM_CARES', True)
        # https://github.com/grpc/grpc/pull/24449
        env.set('GRPC_BUILD_WITH_BORING_SSL_ASM', '')

        for dep in self.spec.dependencies(deptype='link'):
            query = self.spec[dep.name]
            env.prepend_path('LIBRARY_PATH', query.libs.directories[0])
            env.prepend_path('CPATH', query.headers.directories[0])

    def patch(self):
        if self.spec.satisfies('%fj'):
            filter_file("-std=gnu99", "", "setup.py")
