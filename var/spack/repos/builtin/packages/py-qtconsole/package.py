# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyQtconsole(PythonPackage):
    """Jupyter Qt console"""

    homepage = "http://ipython.org"
    url      = "https://pypi.io/packages/source/q/qtconsole/qtconsole-4.2.1.tar.gz"

    version('4.5.1', sha256='4af84facdd6f00a6b9b2927255f717bb23ae4b7a20ba1d9ef0a5a5a8dbe01ae2')
    version('4.2.1', sha256='25ec7d345528b3e8f3c91be349dd3c699755f206dc4b6ec668e2e5dd60ea18ef')

    variant('doc', default=False, description='Build documentation')

    depends_on('python@2.7:2.8,3.3:',    type=('build', 'run'))
    depends_on('py-ipykernel@4.1:',      type=('build', 'run'))
    depends_on('py-jupyter-client@4.1:', type=('build', 'run'))
    depends_on('py-jupyter-core',        type=('build', 'run'))
    depends_on('py-pygments',            type=('build', 'run'))
    depends_on('py-traitlets',           type=('build', 'run'))
    depends_on('py-ipython-genutils',    type=('build', 'run'), when='@4.5.1:')
    depends_on('py-sphinx@1.3:',         type=('build', 'run'), when='+docs')
    depends_on('py-pyqt5',               type='run')
