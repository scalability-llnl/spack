# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Msprime(PythonPackage):
    """The library is a reimplementation of Hudson's seminal ms program,
    and aims to eventually reproduce all its functionality."""

    homepage = "https://msprime.readthedocs.io/en/stable/"
    url      = "https://pypi.io/packages/source/m/msprime/msprime-0.7.4.tar.gz"

    version('0.7.4',   sha256='cbbee83879444d99c0a79b9cc3688ff74c7c39426d92134d0ccf17a1e15716ba')

    depends_on('python@3.6:',      type=('build', 'run'))
    depends_on('py-setuptools',    type=('build', 'run'))
    depends_on('py-attrs@19.1.0:', type=('build', 'run'))
    depends_on('gsl',              type=('build', 'link'))
    depends_on('tskit@0.3:',       type=('build', 'run'))
    depends_on('py-numpy@1.7:',    type='run')
