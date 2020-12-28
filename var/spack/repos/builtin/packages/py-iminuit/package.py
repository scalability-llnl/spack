# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIminuit(PythonPackage):
    """Interactive IPython-Friendly Minimizer based on SEAL Minuit2."""

    homepage = "https://pypi.python.org/pypi/iminuit"
    url      = "https://pypi.io/packages/source/i/iminuit/iminuit-1.2.tar.gz"

    version('1.3.6', sha256='d79a197f305d4708a0e3e52b0a6748c1a6997360d2fbdfd09c022995a6963b5e')
    version('1.2', sha256='7651105fc3f186cfb5742f075ffebcc5088bf7797d8ed124c00977eebe0d1c64')

    # Required dependencies
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'), when='@1.3:')
