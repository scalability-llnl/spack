# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMerlin(PythonPackage):
    """Merlin Workflow for HPC."""

    homepage = "https://github.com/LLNL/merlin"
    url      = "https://pypi.io/packages/source/m/merlin/merlin-1.4.1.tar.gz"
    git      = "https://github.com/LLNL/merlin.git"

    version('1.7.5', sha256='1994c1770ec7fc9da216f9d0ca8214684dcc0daa5fd55337b96e308b2e68daaa')
    version('1.7.4', sha256='9a6f8a84a1b52d0bfb0dc7bdbd7e15677e4a1041bd25a49a2d965efe503a6c20')
    version('1.4.1', sha256='9d515cfdbcde2443892afd92b78dbc5bf2aed2060ed3a336e683188e015bca7c')
    version('master', branch='master')
    version('develop', branch='develop')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cached-property', type=('build', 'run'))
    depends_on('py-celery@5.0.0+redis+sqlalchemy', when="@1.7.5:", type=('build', 'run'))
    depends_on('py-celery@4.3.0:4.999+redis+sqlalchemy', when="@:1.7.4", type=('build', 'run'))
    depends_on('py-coloredlogs@10.0:', type=('build', 'run'))
    depends_on('py-cryptography', type=('build', 'run'))
    depends_on('py-importlib-resources', when="^python@3.0:3.6.99", type=('build', 'run'))
    depends_on('py-maestrowf@1.1.7dev0', when="@1.2.0:", type=('build', 'run'))
    depends_on('py-maestrowf@1.1.6:', when="@:1.1.99", type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-parse', type=('build', 'run'))
    depends_on('py-psutil@5.1.0:', type=('build', 'run'))
    depends_on('py-pyyaml@5.1.2:', type=('build', 'run'))
    depends_on('py-tabulate', type=('build', 'run'))
