# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyUproot(PythonPackage):
    """ROOT I/O in pure Python and NumPy.

    Uproot is a reader and a writer of the ROOT file format using only Python
    and Numpy. Unlike the standard C++ ROOT implementation, Uproot is only an
    I/O library, primarily intended to stream data into machine learning
    libraries in Python. Unlike PyROOT and root_numpy, Uproot does not depend
    on C++ ROOT. Instead, it uses Numpy to cast blocks of data from the ROOT
    file as Numpy arrays."""

    homepage = "https://github.com/scikit-hep/uproot4"
    pypi     = "uproot/uproot-4.0.6.tar.gz"

    maintainers = ['vvolkl']

    tags = ['hep']

    version('4.0.7', sha256='7adb688601fda1e9ab8eeb9a9de681f645827dac0943c6180cf85f03f73fb789')
    version('4.0.6', sha256='1bea2ccc899c6959fb2af69d7e5d1e2df210caab30d3510e26f3fc07c143c37e')

    variant('xrootd', default=True,
            description='Build with xrootd support ')
    variant('lz4', default=True,
            description='Build with support for reading '
                        'lz4-compressed rootfiles ')

    variant('zstd', default=True,
            description='Build with support for reading '
                        'zstd-compressed rootfiles ')

    depends_on('python@2.6:2.999,3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))

    depends_on('xrootd', when="+xrootd")

    depends_on('lz4', when="+lz4")
    depends_on('xxhash', when="+lz4")

    depends_on('zstd', when="+zstd")
