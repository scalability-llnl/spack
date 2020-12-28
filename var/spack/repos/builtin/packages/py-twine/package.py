# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTwine(PythonPackage):
    """Twine is a utility for publishing Python packages on PyPI."""

    homepage = "https://twine.readthedocs.io/"
    url      = "https://pypi.io/packages/source/t/twine/twine-2.0.0.tar.gz"

    version('2.0.0', sha256='9fe7091715c7576df166df8ef6654e61bada39571783f2fd415bdcba867c6993')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-pkginfo@1.4.2:', type=('build', 'run'))
    depends_on('py-readme-renderer@21.0:', type=('build', 'run'))
    depends_on('py-requests-toolbelt@0.8.0:0.8.999,0.9.1:', type=('build', 'run'))
    depends_on('py-setuptools@0.7.0:', type=('build', 'run'))
    depends_on('py-tqdm@4.14:', type=('build', 'run'))
