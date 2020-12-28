# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyIpykernel(PythonPackage):
    """IPython Kernel for Jupyter"""

    homepage = "https://pypi.python.org/pypi/ipykernel"
    url      = "https://pypi.io/packages/source/i/ipykernel/ipykernel-5.3.4.tar.gz"

    version('5.3.4',  sha256='9b2652af1607986a1b231c62302d070bc0534f564c393a5d9d130db9abbbe89d')
    version('5.1.1',  sha256='f0e962052718068ad3b1d8bcc703794660858f58803c3798628817f492a8769c')
    version('5.1.0',  sha256='0fc0bf97920d454102168ec2008620066878848fcfca06c22b669696212e292f')
    version('4.10.0', sha256='699103c8e64886e3ec7053f2a6aa83bb90426063526f63a818732ff385202bad')
    version('4.5.0',  sha256='245a798edb8fd751b95750d8645d736dd739a020e7fc7d5627dac4d1c35d8295')
    version('4.4.1',  sha256='6d48398b3112efb733b254edede4b7f3262c28bd19f665b64ef1acf6ec5cd74f')
    version('4.4.0',  sha256='d516427c3bd689205e6693c9616302ef34017b91ada3c9ea3fca6e90702b7ffe')
    version('4.3.1',  sha256='8219d3eaa3e4d4efc5f349114e41a40f0986c91a960846bb81d5da817fb7cc3f')
    version('4.3.0',  sha256='f214c661328c836e02b6f185f98f3eccd7ce396791937493ffa1babf5e3267ab')
    version('4.2.2',  sha256='a876da43e01acec2c305abdd8e6aa55f052bab1196171ccf1cb9a6aa230298b0')
    version('4.2.1',  sha256='081a5d4db33db58697be2d682b92f79b2c239493445f13dd457c15bc3e52c874')
    version('4.2.0',  sha256='723b3d4baac20f0c9cd91fc75c3e813636ecb6c6e303fb34d628c3df078985a7')
    version('4.1.1',  sha256='d8c5555386d0f18f1336dea9800f9f0fe96dcecc9757c0f980e11fdfadb661ff')
    version('4.1.0',  sha256='e0e150ad55e487e49054efc9a4b0e2e17f27e1de77444b26760789077b146d86')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('python@3.4:', when='@5.0:', type=('build', 'run'))
    depends_on('python@3.5:', when='@5.2:', type=('build', 'run'))
    depends_on('py-setuptools', type='build', when='@5:')
    depends_on('py-ipython@4.0:', when='@:4.999', type=('build', 'run'))
    depends_on('py-ipython@5.0:', when='@5.0.0:', type=('build', 'run'))
    depends_on('py-traitlets@4.1.0:', type=('build', 'run'))
    depends_on('py-jupyter-client', type=('build', 'run'))
    depends_on('py-tornado@4.0:', when='@:4.999', type=('build', 'run'))
    depends_on('py-tornado@4.2:', when='@5.0.0:', type=('build', 'run'))
    depends_on('py-appnope', when='platform=darwin', type=('build', 'run'))

    phases = ['build', 'install', 'install_data']

    def install_data(self, spec, prefix):
        """ install the Jupyter kernel spec """
        self.spec['python'].command(
            '-m', 'ipykernel', 'install', '--prefix=' + prefix)
