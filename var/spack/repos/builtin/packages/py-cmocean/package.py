# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyCmocean(PythonPackage):
    """Colormaps for Oceanography."""

    homepage = "https://matplotlib.org/cmocean/"
    pypi = "cmocean/cmocean-2.0.tar.gz"

    version('2.0', sha256='13eea3c8994d8e303e32a2db0b3e686f6edfb41cb21e7b0e663c2b17eea9b03a')

    depends_on('py-setuptools', type='build')
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
