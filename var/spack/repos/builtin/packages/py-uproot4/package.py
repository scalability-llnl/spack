# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUproot4(PythonPackage):
    """ROOT I/O in pure Python and NumPy."""

    homepage = "https://uproot4.readthedocs.io"
    git      = "https://github.com/scikit-hep/uproot4"
    url      = "https://github.com/scikit-hep/uproot4/archive/0.0.27.tar.gz"

    maintainers = ['vvolkl']

    tags = ['hep']

    version('master', branch='master')
    version('0.0.27', sha256='de87555937332998b476f3e310392962bc983bddc008ed2b3c07a25c0379c4c9')

    variant('xrootd', default=True,
            description='Build with xrootd support ')
    variant('lz4', default=True,
            description='Build with support for reading '
                        'lz4-compressed rootfiles ')

    variant('zstd', default=True,
            description='Build with support for reading '
                        'zstd-compressed rootfiles ')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))

    depends_on('xrootd', when="+xrootd")

    depends_on('lz4', when="+lz4")
    depends_on('xxhash', when="+lz4")

    depends_on('zstd', when="+zstd")
