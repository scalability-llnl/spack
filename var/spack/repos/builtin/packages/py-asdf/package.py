# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsdf(PythonPackage):
    """The Advanced Scientific Data Format (ASDF) is a next-generation
    interchange format for scientific data. This package contains the Python
    implementation of the ASDF Standard."""

    homepage = "https://github.com/spacetelescope/asdf"
    url      = "https://pypi.io/packages/source/a/asdf/asdf-2.4.2.tar.gz"

    version('2.4.2', sha256='6ff3557190c6a33781dae3fd635a8edf0fa0c24c6aca27d8679af36408ea8ff2')

    depends_on('python@3.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-semantic-version@2.3.1:2.6.0', type=('build', 'run'))
    depends_on('py-pyyaml@3.10:', type=('build', 'run'))
    depends_on('py-jsonschema@2.3:3.999', type=('build', 'run'))
    depends_on('py-six@1.9.0:', type=('build', 'run'))
    depends_on('py-numpy@1.8:', type=('build', 'run'))
