# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyJupyterlabPygments(PythonPackage):
    """Pygments theme using JupyterLab CSS variables."""

    homepage = "https://jupyter.org/"
    url      = "https://pypi.io/packages/source/j/jupyterlab-pygments/jupyterlab_pygments-0.1.1.tar.gz"

    version('0.1.1', sha256='19a0ccde7daddec638363cd3d60b63a4f6544c9181d65253317b2fb492a797b9')

    depends_on('py-setuptools', type='build')
    depends_on('py-pygments@2.4.1:2.999', type=('build', 'run'))
