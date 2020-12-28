# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDill(PythonPackage):
    """Serialize all of python """

    homepage = "https://github.com/uqfoundation/dill"
    url      = "https://pypi.io/packages/source/d/dill/dill-0.2.7.tar.gz"

    version('0.3.1', sha256='d3ddddf2806a7bc9858b20c02dc174396795545e9d62f243b34481fd26eb3e2c')
    version('0.2.9', sha256='f6d6046f9f9195206063dd0415dff185ad593d6ee8b0e67f12597c0f4df4986f')
    version('0.2.7', sha256='ddda0107e68e4eb1772a9f434f62a513c080c7171bd0dd6fb65d992788509812')
    version('0.2.6', sha256='6c1ccca68be483fa8c66e85a89ffc850206c26373aa77a97b83d8d0994e7f1fd')
    version('0.2.5', sha256='e82b3db7b9d962911c9c2d5cf2bb4a04f43933f505a624fb7dc5f68b949f0a5c')
    version('0.2.4', sha256='db68929eef0e886055d6bcd86f830141c1f653ddbf5d081c086e9d1c45efb334')
    version('0.2.3', sha256='9abf049a5305cb982ebbdccf084273b108c8042b826a7606ba568fc5e063e582')
    version('0.2.2', sha256='6ad223cc41614dcc8cf217e8d7a32857f13752cd0a5332580c80b9fa054ece69')
    version('0.2.1', sha256='a54401bdfae419cfe1c9e0b48e9b290afccaa413d2319d9bb0fdb85c130a7923')
    version('0.2', sha256='aba8d4c81c4136310e6ce333bd6f4f3ea2d53bd367e2f69c864428f260c0308c')

    depends_on('python@2.5:2.8,3.1:', type=('build', 'run'))
    depends_on('python@2.6:2.8,3.1:', type=('build', 'run'), when='@0.3.0:')

    depends_on('py-setuptools@0.6:', type='build')

    def url_for_version(self, version):
        url = "https://pypi.io/packages/source/d/dill/"

        if version >= Version('0.2.7'):
            url += 'dill-{0}.tar.gz'
        else:
            url += 'dill-{0}.zip'

        url = url.format(version)
        return url
