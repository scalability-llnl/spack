# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySeaborn(PythonPackage):
    """Seaborn: statistical data visualization.

    Seaborn is a library for making attractive and informative statistical
    graphics in Python. It is built on top of matplotlib and tightly
    integrated with the PyData stack, including support for numpy and pandas
    data structures and statistical routines from scipy and statsmodels."""

    homepage = "http://seaborn.pydata.org/"
    url      = "https://pypi.io/packages/source/s/seaborn/seaborn-0.7.1.tar.gz"

    version('0.9.0', sha256='76c83f794ca320fb6b23a7c6192d5e185a5fcf4758966a0c0a54baee46d41e2f')
    version('0.7.1', sha256='fa274344b1ee72f723bab751c40a5c671801d47a29ee9b5e69fcf63a18ce5c5d')

    depends_on('py-setuptools', type='build')

    depends_on('py-numpy',      type=('build', 'run'))
    depends_on('py-scipy',      type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-pandas',     type=('build', 'run'))
