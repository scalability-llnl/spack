# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyPyzmq(PythonPackage):
    """PyZMQ: Python bindings for zeromq."""
    homepage = "https://github.com/zeromq/pyzmq"
    url      = "https://github.com/zeromq/pyzmq/archive/v14.7.0.tar.gz"

    import_modules = [
        'zmq', 'zmq.green', 'zmq.green.eventloop', 'zmq.sugar', 'zmq.auth',
        'zmq.auth.asyncio', 'zmq.utils', 'zmq.backend', 'zmq.backend.cffi',
        'zmq.backend.cython', 'zmq.ssh', 'zmq.eventloop',
        'zmq.eventloop.minitornado', 'zmq.eventloop.minitornado.platform',
        'zmq.log', 'zmq.asyncio', 'zmq.devices'
    ]

    version('18.1.0', sha256='32f7618b8104021bc96cbd60be4330bdf37b929e8061dbce362c9f3478a08e21')
    version('18.0.1', sha256='7b0107992d8cc4c43d9af1c2e13d573ea761c7feb23d7e0e7da9dc963811e68f')
    version('17.1.2', sha256='77a32350440e321466b1748e6063b34a8a73768b62cb674e7d799fbc654b7c45')
    version('16.0.2', sha256='717dd902c3cf432b1c68e7b299ad028b0de0d0a823858e440b81d5f1baa2b1c1')
    version('14.7.0', sha256='809a5fcc720d286c840f7f64696e60322b5b2544795a73db626f09b344d16a15')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'), when='@18:')
    depends_on('py-cython@0.16:', type='build')
    depends_on('py-cython@0.20:', type='build', when='@18:')
    depends_on('py-py', type=('build', 'run'))
    depends_on('py-cffi', type=('build', 'run'))
    depends_on('py-gevent', type=('build', 'run'))
    depends_on('libzmq')

    def setup_build_environment(self, env):
        # Needed for `spack install --test=root py-pyzmq`
        # Fixes import failure for zmq.backend.cffi
        # https://github.com/zeromq/pyzmq/issues/395#issuecomment-22041019
        env.prepend_path(
            'C_INCLUDE_PATH', self.spec['libzmq'].headers.directories[0])
        env.prepend_path(
            'LIBRARY_PATH', self.spec['libzmq'].libs.directories[0])

    # Needed for `spack test run py-pyzmq`
    setup_run_environment = setup_build_environment
