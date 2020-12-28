# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNumexpr(PythonPackage):
    """Fast numerical expression evaluator for NumPy"""
    homepage = "https://pypi.python.org/pypi/numexpr"
    url      = "https://github.com/pydata/numexpr/archive/v2.7.0.tar.gz"

    version('2.7.0', sha256='1923f038b90cc69635871968ed742be7775c879451c612f173c2547c823c9561')
    version('2.6.9', sha256='d57267bbdf10906f5ed7841b3484bec4af0494102b50e89ba316924cc7a7fd46')
    version('2.6.5', sha256='fe78a78e002806e87e012b6105f3b3d52d47fc7a72bafb56341fcec7ce02cfd7')
    version('2.6.1', sha256='e92c83d066fa8da63864d69b5f218287cc31437ae844db77390f2183123aab22')
    version('2.5',   sha256='4ca111a9a27c9513c2e2f5b70c0a84ea69081d7d8e4512d4c3f26a485292de0d')
    version('2.4.6', sha256='2681faf55a3f19ba4424cc3d6f0a10610ebd49f029f8453f0ba64dd5c0fe4e0f')

    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-numpy@1.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
