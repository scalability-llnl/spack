# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyJupyterlabServer(PythonPackage):
    """A set of server components for JupyterLab and JupyterLab
       like applications"""

    homepage = "https://pypi.org/project/jupyterlab-server/"
    url      = "https://pypi.io/packages/source/j/jupyterlab_server/jupyterlab_server-1.2.0.tar.gz"

    version('1.2.0', sha256='5431d9dde96659364b7cc877693d5d21e7b80cea7ae3959ecc2b87518e5f5d8c')
    version('1.1.0', sha256='bac27e2ea40f686e592d6429877e7d46947ea76c08c878081b028c2c89f71733')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')

    depends_on('py-requests', type=('build', 'run'))
    depends_on('py-json5', type=('build', 'run'))
    depends_on('py-jsonschema@3.0.1:', type=('build', 'run'))
    depends_on('py-notebook@4.2.0:', type=('build', 'run'))
    depends_on('py-jinja2@2.10:', type=('build', 'run'))
