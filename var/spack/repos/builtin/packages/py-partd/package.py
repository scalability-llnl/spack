# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPartd(PythonPackage):
    """Key-value byte store with appendable values."""

    homepage = "http://github.com/dask/partd/"
    url      = "https://pypi.io/packages/source/p/partd/partd-0.3.8.tar.gz"

    version('1.1.0', sha256='6e258bf0810701407ad1410d63d1a15cfd7b773fd9efe555dac6bb82cc8832b0')
    version('0.3.10', sha256='33722a228ebcd1fa6f44b1631bdd4cff056376f89eb826d7d880b35b637bcfba')
    version('0.3.8', sha256='67291f1c4827cde3e0148b3be5d69af64b6d6169feb9ba88f0a6cfe77089400f')

    depends_on('python@3.5:', type=('build', 'run'), when='@1.1.0:')
    depends_on('py-setuptools', type='build')
    depends_on('py-locket', type=('build', 'run'))
    depends_on('py-toolz', type=('build', 'run'))
