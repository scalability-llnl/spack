# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFilelock(PythonPackage):
    """This package contains a single module, which implements a platform
    independent file lock in Python, which provides a simple way of
    inter-process communication"""

    homepage = "https://github.com/benediktschmitt/py-filelock"
    url      = "https://pypi.io/packages/source/f/filelock/filelock-3.0.4.tar.gz"

    version('3.0.12',  sha256='18d82244ee114f543149c66a6e0c14e9c4f8a1044b5cdaadd0f82159d6a6ff59')
    version('3.0.4',  sha256='011327d4ed939693a5b28c0fdf2fd9bda1f68614c1d6d0643a89382ce9843a71')
    version('3.0.3',  sha256='7d8a86350736aa0efea0730e6a7f774195cbb1c2d61134c15f6be576399e87ff')
    version('3.0.0',  sha256='b3ad481724adfb2280773edd95ce501e497e88fa4489c6e41e637ab3fd9a456c')
    version('2.0.13', sha256='d05079e7d7cae7576e192749d3461999ca6b0843d35b0f79f1fa956b0f6fc7d8')
    version('2.0.12', sha256='eb4314a9a032707a914b037433ce866d4ed363fce8605d45f0c9d2cd6ac52f98')
    version('2.0.11', sha256='e9e370efe86c30b19a2c8c36dd9fcce8e5ce294ef4ed6ac86664b666eaf852ca')
    version('2.0.10', sha256='c73bf706d8a0c5722de0b745495fed9cda0e46c0eabb44eb18ee3f00520fa85f')
    version('2.0.9',  sha256='0f91dce339c9f25d6f2e0733a17e4f9a47b139dffda52619a0e61e013e5c6782')
    version('2.0.8',  sha256='7e48e4906de3c9a5d64d8f235eb3ae1050dfefa63fd65eaf318cc915c935212b')

    depends_on('py-setuptools', type=('build', 'run'))
