# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyNotebook(PythonPackage):
    """Jupyter Interactive Notebook"""

    homepage = "https://github.com/jupyter/notebook"
    url      = "https://pypi.io/packages/source/n/notebook/notebook-6.1.4.tar.gz"

    version('6.1.4', sha256='687d01f963ea20360c0b904ee7a37c3d8cda553858c8d6e33fd0afd13e89de32')
    version('6.0.3', sha256='47a9092975c9e7965ada00b9a20f0cf637d001db60d241d479f53c0be117ad48')
    version('6.0.1', sha256='660976fe4fe45c7aa55e04bf4bccb9f9566749ff637e9020af3422f9921f9a5d')
    version('5.7.8', sha256='573e0ae650c5d76b18b6e564ba6d21bf321d00847de1d215b418acb64f056eb8')
    version('4.2.3', sha256='39a9603d3fe88b60de2903680c965cf643acf2c16fb2c6bac1d905e1042b5851')
    version('4.2.2', sha256='418ba230c9b2e7e739940cae9fb4625e10a63f038e9c95cf1a9b7a244256ba38')
    version('4.2.1', sha256='a49de524dabb99f214bdf2a58f26c7892650251a23a3669c6492fb180492e197')
    version('4.2.0', sha256='e10c4916c77b48394796b5b1440d61d7b210f9941194048fe20ef88948016d84')
    version('4.1.0', sha256='b597437ba33538221008e21fea71cd01eda9da1515ca3963d7c74e44f4b03d90')
    version('4.0.6', sha256='f62e7a6afbc00bab3615b927595d27b1874cff3218bddcbab62f97f6dae567c3')
    version('4.0.4', sha256='a57852514bce1b1cf41fa0311f6cf894960cf68b083b55e6c408316b598d5648')
    version('4.0.2', sha256='8478d7e2ab474855b0ff841f693983388af8662d3af1adcb861acb900274f22a')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('python@3.5:',         type=('build', 'run'), when='@6:')
    depends_on('py-setuptools',       type=('build', 'run'), when='@5:')
    depends_on('py-jinja2',           type=('build', 'run'))
    depends_on('py-tornado@4.0:6.999', type=('build', 'run'), when='@:5.7.4')
    depends_on('py-tornado@4.1:6.999', type=('build', 'run'), when='@5.7.5:5.999')
    depends_on('py-tornado@5.0:',      type=('build', 'run'), when='@6:')
    depends_on('py-pyzmq@17:',         type=('build', 'run'), when='@6:')
    depends_on('py-argon2-cffi',       type=('build', 'run'), when='@6.1:')
    depends_on('py-ipython-genutils', type=('build', 'run'))
    depends_on('py-traitlets',        type=('build', 'run'))
    depends_on('py-traitlets@4.2.1:', type=('build', 'run'), when='@5:')
    depends_on('py-jupyter-core',        type=('build', 'run'))
    depends_on('py-jupyter-core@4.4.0:', type=('build', 'run'), when='@5.7.0:6.0.1')
    depends_on('py-jupyter-core@4.6.0:', type=('build', 'run'), when='@6.0.2')
    depends_on('py-jupyter-core@4.6.1:', type=('build', 'run'), when='@6.0.3:')
    depends_on('py-jupyter-client',        type=('build', 'run'))
    depends_on('py-jupyter-client@5.2.0:', type=('build', 'run'), when='@5.7.0:5.999')
    depends_on('py-jupyter-client@5.3.1:', type=('build', 'run'), when='@6.0.0:6.0.1')
    depends_on('py-jupyter-client@5.3.4:', type=('build', 'run'), when='@6.0.2:')
    depends_on('py-nbformat',         type=('build', 'run'))
    depends_on('py-nbconvert',        type=('build', 'run'))
    depends_on('py-ipykernel',        type=('build', 'run'))
    depends_on('py-send2trash',        type=('build', 'run'), when='@6:')
    depends_on('py-terminado@0.3.3:', type=('build', 'run'), when='@:5.7.0')
    depends_on('py-terminado@0.8.1:', type=('build', 'run'), when='@5.7.0:')
    depends_on('py-terminado@0.8.3:', type=('build', 'run'), when='@6.1:')
    depends_on('py-prometheus-client', type=('build', 'run'), when='@5.7.0:')
