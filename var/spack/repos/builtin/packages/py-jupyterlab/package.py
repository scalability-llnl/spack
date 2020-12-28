# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyJupyterlab(PythonPackage):
    """JupyterLab is the next-generation web-based user interface
       for Project Jupyter."""

    homepage = "https://jupyterlab.readthedocs.io/"
    url      = "https://pypi.io/packages/source/j/jupyterlab/jupyterlab-2.2.7.tar.gz"

    version('2.2.7', sha256='a72ffd0d919cba03a5ef8422bc92c3332a957ff97b0490494209c83ad93826da')
    version('2.1.0', sha256='8c239aababf5baa0b3d36e375fddeb9fd96f3a9a24a8cda098d6a414f5bbdc81')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-notebook@4.3.1:', type=('build', 'run'))
    depends_on('py-tornado@:5,6.0.3:', type=('build', 'run'))
    depends_on('py-jupyterlab-server@1.1.5:1.999', type=('build', 'run'))
    depends_on('py-jinja2@2.10:', type=('build', 'run'))
