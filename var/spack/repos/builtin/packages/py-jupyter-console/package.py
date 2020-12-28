# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterConsole(PythonPackage):
    """Jupyter Terminal Console"""

    homepage = "https://github.com/jupyter/jupyter_console"
    url      = "https://github.com/jupyter/jupyter_console/archive/5.0.0.tar.gz"

    version('6.1.0', sha256='838c95c99ce52978e1660e7a30dd933dede158e2f4da1bc5fad1a8fad44570b7')
    version('5.2.0', sha256='371d03aeefcf48967f2f00af4c1709f52d2a688deee33f395c6330e4e8aa171c')
    version('5.0.0', sha256='e966b2b5bf9a1e8c5bd11a6335bb11f68ec585ea39b801721b2ed9dd964468fa')
    version('4.1.1', sha256='0bb06a1f878d0c44c2f6f66406a80f949bcd86f3508035500af7dceffb9cc7dc')
    version('4.1.0', sha256='9c72097721676ba13d036e68d82ef9ef76772254c8a995a474339a8bd48aaf91')
    version('4.0.3', sha256='b1867a89b693f247e9089a8f367fa4f27af6eac27930cad2966054adfa7b9aa1')
    version('4.0.2', sha256='116a56763899bbb12c762f865372eb52c08619ef070c237c7f1387e192bfd3df')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('python@3.5:', type=('build', 'run'), when='@6:')
    depends_on('py-jupyter-client', type=('build', 'run'))
    depends_on('py-ipython@:5.8.0', type=('build', 'run'), when='@:5')
    depends_on('py-ipython', type=('build', 'run'))
    depends_on('py-ipykernel', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-prompt-toolkit@1.0.0:1.999', type=('build', 'run'), when='@:5')
    depends_on('py-prompt-toolkit@2.0.0:2.999,3.0.2:3.0.999', type=('build', 'run'), when='@6:')
