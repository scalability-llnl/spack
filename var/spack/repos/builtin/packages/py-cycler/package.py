# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCycler(PythonPackage):
    """Composable style cycles."""

    homepage = "http://matplotlib.org/cycler/"
    url      = "https://github.com/matplotlib/cycler/archive/v0.10.0.tar.gz"

    version('0.10.0', sha256='b6d217635e03024196225367b1a438996dbbf0271bec488f00584f0e7dc15cfa')

    depends_on('py-setuptools', type='build')
    depends_on('py-six',        type=('build', 'run'))
