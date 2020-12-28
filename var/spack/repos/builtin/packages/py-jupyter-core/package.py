# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterCore(PythonPackage):
    """Core Jupyter functionality"""

    homepage = "http://jupyter-core.readthedocs.io/"
    url      = "https://pypi.io/packages/source/j/jupyter-core/jupyter_core-4.6.0.tar.gz"

    version('4.6.3', sha256='394fd5dd787e7c8861741880bdf8a00ce39f95de5d18e579c74b882522219e7e')
    version('4.6.1', sha256='a183e0ec2e8f6adddf62b0a3fc6a2237e3e0056d381e536d3e7c7ecc3067e244')
    version('4.6.0', sha256='85103cee6548992780912c1a0a9ec2583a4a18f1ef79a248ec0db4446500bce3')
    version('4.4.0', sha256='ba70754aa680300306c699790128f6fbd8c306ee5927976cbe48adacf240c0b7')
    version('4.2.0', sha256='44ec837a53bebf4e937112d3f9ccf31fee4f8db3e406dd0dd4f0378a354bed9c')
    version('4.1.1', sha256='ae0e69435258126466c86cd989e465a9c334c50107ef4f257decc8693650bf4c')
    version('4.1.0', sha256='146af0679c33c56db4b85b785f3dacd933ffaca97e7d2d56ff577a5485c2bd13')
    version('4.0.6', sha256='96a68a3b1d018ff7776270b26b7cb0cfd7a18a53ef2061421daff435707d198c')
    version('4.0.5', sha256='9f6581b827f56cfa1771d7b1bd8ecc1274afa7f6e3e1046b7e0d4e05d52bf6e8')
    version('4.0.4', sha256='fcf45478025f34174943993947f51a41ad871ac998a14bf1cb87d8eb61e75c6d')
    version('4.0.3', sha256='12258d8c593c53bb08e09f3da63a418d7cb5b5852b3d0ffa29639402f56dcbdb')
    version('4.0.2', sha256='13a46b3c493ac63bd75048d6d2142cfc44258bc6c260d96c506f0214fcd78a70')
    version('4.0.1', sha256='7c165f7de7a063596f8be1bcfc86e9ba6897e38baf24e8510514690963600122')
    version('4.0.0', sha256='9025208cdfc40718c7e3ab62b5e17aacf68e3fc66e34ff21fe032d553620122a')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'), when='@4.6.2:')
    depends_on('py-setuptools', when='@4.5.0:', type=('build', 'run'))
    depends_on('py-traitlets', type=('build', 'run'))
