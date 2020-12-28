# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCodecov(PythonPackage):
    """Hosted coverage reports for Github, Bitbucket and Gitlab."""

    homepage = "https://github.com/codecov/codecov-python"
    url      = "https://pypi.io/packages/source/c/codecov/codecov-2.0.15.tar.gz"

    version('2.0.15', sha256='8ed8b7c6791010d359baed66f84f061bba5bd41174bf324c31311e8737602788')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-requests@2.7.9:', type=('build', 'run'))
    depends_on('py-coverage', type=('build', 'run'))
    depends_on('py-argparse', when='^python@:2.6', type=('build', 'run'))
