# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPlac(PythonPackage):
    """The smartest command line arguments parser in the world."""

    homepage = "https://github.com/micheles/plac"
    url      = "https://pypi.io/packages/source/p/plac/plac-1.1.3.tar.gz"

    version('1.1.3', sha256='398cb947c60c4c25e275e1f1dadf027e7096858fb260b8ece3b33bcff90d985f')

    depends_on('py-setuptools', type='build')
    depends_on('py-argparse', when='^python@:2.6', type=('build', 'run'))
