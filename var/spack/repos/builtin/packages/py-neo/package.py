# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNeo(PythonPackage):
    """Neo is a package for representing electrophysiology data in Python,
    together with support for reading a wide range of neurophysiology
    file formats"""

    homepage = "http://neuralensemble.org/neo"
    url      = "https://pypi.io/packages/source/n/neo/neo-0.4.1.tar.gz"

    version('0.5.2', sha256='1de436b7d5e72a5b4f1baa68bae5b790624a9ac44b2673811cb0b6ef554d3f8b')
    version('0.4.1', sha256='a5a4f3aa31654d52789f679717c9fb622ad4f59b56d227dca490357b9de0a1ce')

    depends_on('py-setuptools',        type='build')
    depends_on('py-numpy@1.7.1:',      type=('build', 'run'))
    depends_on('py-quantities@0.9.0:', type=('build', 'run'))
