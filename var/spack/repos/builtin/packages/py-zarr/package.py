# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyZarr(PythonPackage):
    """Zarr is a Python package providing an implementation of chunked,
    compressed, N-dimensional arrays."""

    homepage = "https://zarr.readthedocs.io"
    pypi = "zarr/zarr-2.3.2.tar.gz"

    version('2.6.1', sha256='fa7eac1e4ff47ff82d09c42bb4679e18e8a05a73ee81ce59cee6a441a210b2fd')
    version('2.5.0', sha256='d54f060739208392494c3dbcbfdf41c8df9fa23d9a32b91aea0549b4c5e2b77f')
    version('2.4.0', sha256='53aa21b989a47ddc5e916eaff6115b824c0864444b1c6f3aaf4f6cf9a51ed608')
    version('2.3.2', sha256='c62d0158fb287151c978904935a177b3d2d318dea3057cfbeac8541915dfa105')

    depends_on('python@3.5:',               type=('build', 'run'), when='@2.4.0:')
    depends_on('python@3.6:',               type=('build', 'run'), when='@2.6.0:')
    depends_on('py-asciitree',              type=('build', 'run'))
    depends_on('py-fasteners',              type=('build', 'run'))
    depends_on('py-msgpack',                type=('build', 'run'), when='@:2.3.2')
    depends_on('py-setuptools@18.0:',       type='build')
    depends_on('py-setuptools@38.6.0:',     type='build', when='@2.4.0:')
    depends_on('py-setuptools-scm@1.5.5:',  type='build')
    depends_on('py-numcodecs@0.6.2:',       type=('build', 'run'))
    depends_on('py-numcodecs@0.6.4:',       type=('build', 'run'), when='@2.4.0:')
    depends_on('py-numpy@1.7:',             type=('build', 'run'))
    depends_on('py-scandir',                type=('build', 'run'), when='^python@:3.4')
