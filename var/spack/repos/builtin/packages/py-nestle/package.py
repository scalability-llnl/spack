# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyNestle(PythonPackage):
    """Nested sampling algorithms for evaluating Bayesian evidence."""

    homepage = "http://kbarbary.github.io/nestle/"
    url = "https://pypi.io/packages/source/n/nestle/nestle-0.1.1.tar.gz"

    version('0.1.1', sha256='d236a04f25494af5cda572eecf62729592b3231fbd874b1f72aff54718a3bb08')

    # Required dependencies
    depends_on('py-numpy', type=('build', 'run'))

    # Optional dependencies
    depends_on('py-scipy', type=('build', 'run'))
