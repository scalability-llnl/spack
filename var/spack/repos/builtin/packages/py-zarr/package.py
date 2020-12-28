# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZarr(PythonPackage):
    """Zarr is a Python package providing an implementation of chunked,
    compressed, N-dimensional arrays."""

    homepage = "https://zarr.readthedocs.io"
    url      = "https://pypi.io/packages/source/z/zarr/zarr-2.3.2.tar.gz"

    version('2.3.2', sha256='c62d0158fb287151c978904935a177b3d2d318dea3057cfbeac8541915dfa105')

    depends_on('py-asciitree',              type=('build', 'run'))
    depends_on('py-fasteners',              type=('build', 'run'))
    depends_on('py-msgpack',                type=('build', 'run'))
    depends_on('py-setuptools@18.1:',       type='build')
    depends_on('py-setuptools-scm@1.5.5:',  type='build')
    depends_on('py-numcodecs@0.6.2:',       type=('build', 'run'))
    depends_on('py-numpy@1.7:',             type=('build', 'run'))
    depends_on('py-scandir',     type=('build', 'run'), when='^python@:3.4')
