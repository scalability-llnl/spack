# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyter(PythonPackage):
    """Jupyter metapackage. Install all the Jupyter components in one go."""

    homepage = "https://jupyter.org/"
    url      = "https://pypi.io/packages/source/j/jupyter/jupyter-1.0.0.tar.gz"

    version('1.0.0', sha256='d9dc4b3318f310e34c82951ea5d6683f67bed7def4b259fafbfe4f1beb1d8e5f')

    depends_on('py-notebook', type=('build', 'run'))
    depends_on('py-qtconsole', type=('build', 'run'))
    depends_on('py-jupyter-console', type=('build', 'run'))
    depends_on('py-nbconvert', type=('build', 'run'))
    depends_on('py-ipykernel', type=('build', 'run'))
    depends_on('py-ipywidgets', type=('build', 'run'))
