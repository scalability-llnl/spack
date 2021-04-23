# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJupyterLatexEnvs(PythonPackage):
    """(some) LaTeX environments for Jupyter notebook"""

    homepage = "https://github.com/jfbercher/jupyter_latex_envs"
    url      = "https://pypi.io/packages/source/j/jupyter_latex_envs/jupyter_latex_envs-1.4.6.tar.gz"

    version('1.4.6', sha256='070a31eb2dc488bba983915879a7c2939247bf5c3b669b398bdb36a9b5343872')

    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-ipython', type=('build', 'run'))
    depends_on('py-jupyter-core', type=('build', 'run'))
    depends_on('py-nbconvert', type=('build', 'run'))
    depends_on('py-notebook@4.0:', type=('build', 'run'))
    depends_on('py-traitlets@4.1:', type=('build', 'run'))

    @run_after('install')
    def install_nbext(self):
        jupyter = which('jupyter')
        jupyter('nbextension', 'install', '--py', 'latex_envs', '--sys-prefix')
        jupyter('nbextension', 'enable', '--py', 'latex_envs', '--sys-prefix')
