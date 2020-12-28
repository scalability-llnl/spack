# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRnacocktail(PythonPackage):
    """RNACocktail: A comprehensive framework
    for accurate and efficient RNA-Seq analysis."""

    homepage = "http://bioinform.github.io/rnacocktail/"
    url      = "https://github.com/bioinform/rnacocktail/archive/v0.2.2.tar.gz"

    version('0.2.2', sha256='34aa0d1d7bd9d80303fe7dac5acc0519f7c1ed986397692588343d82ce45c7a5')

    depends_on('python@2.7:2.8', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-pybedtools', type=('build', 'run'))
    depends_on('py-pysam', type=('build', 'run'))
    # Higher version of py-pandas and py-numpy
    # depends on python@3: which conflicts with py-rnacocktail
    depends_on('py-pandas@:0.24.2', type=('build', 'run'))
    depends_on('py-numpy@:1.16.5', type=('build', 'run'))
