# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJedi(PythonPackage):
    """An autocompletion tool for Python that can be used for text editors."""

    homepage = "https://github.com/davidhalter/jedi"
    url      = "https://pypi.io/packages/source/j/jedi/jedi-0.9.0.tar.gz"

    version('0.13.3', sha256='2bb0603e3506f708e792c7f4ad8fc2a7a9d9c2d292a358fbbd58da531695595b')
    # unfortunately pypi.io only offers a .whl for 0.10.0
    version('0.10.0', sha256='d6a7344df9c80562c3f62199278004ccc7c5889be9f1a6aa5abde117ec085123',
            url='https://github.com/davidhalter/jedi/archive/v0.10.0.tar.gz')
    version('0.9.0', sha256='3b4c19fba31bdead9ab7350fb9fa7c914c59b0a807dcdd5c00a05feb85491d31')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.2:', type=('build', 'run'), when='@0.9.0')
    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'), when='@0.10.0')
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'), when='@0.13.3')
    depends_on('py-parso@0.1.0', type=('build', 'run'), when='@0.11.0')
    depends_on('py-parso@0.1.1', type=('build', 'run'), when='@0.11.1')
    depends_on('py-parso@0.2.0:', type=('build', 'run'), when='@0.12.0')
    depends_on('py-parso@0.3.0:', type=('build', 'run'), when='@0.12.1:0.14.0')
