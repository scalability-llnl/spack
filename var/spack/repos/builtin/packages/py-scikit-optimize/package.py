# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyScikitOptimize(PythonPackage):
    """Scikit-Optimize, or skopt, is a simple and efficient library to
       minimize (very) expensive and noisy black-box functions. It implements
       several methods for sequential model-based optimization. skopt aims to
       be accessible and easy to use in many contexts.

       The library is built on top of NumPy, SciPy and Scikit-Learn."""

    homepage = "https://scikit-optimize.github.io"
    url      = "https://pypi.io/packages/source/s/scikit-optimize/scikit-optimize-0.5.2.tar.gz"

    version('0.5.2', sha256='1d7657a4b8ef9aa6d81e49b369c677c584e83269f11710557741d3b3f8fa0a75')

    variant('plots', default=True,
            description='Build with plot support from py-matplotlib')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy@0.14.0:', type=('build', 'run'))
    depends_on('py-scikit-learn@0.19.1:', type=('build', 'run'))

    depends_on('py-matplotlib',   when='+plots')
