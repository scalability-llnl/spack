# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEntrypoints(PythonPackage):
    """Discover and load entry points from installed packages."""

    homepage = "https://pypi.python.org/pypi/entrypoints"
    url      = "https://pypi.io/packages/source/e/entrypoints/entrypoints-0.2.3.tar.gz"

    version('0.3', sha256='c70dd71abe5a8c85e55e12c19bd91ccfeec11a6e99044204511f9ed547d48451')
    version('0.2.3', sha256='d2d587dde06f99545fb13a383d2cd336a8ff1f359c5839ce3a64c917d10c029f')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-configparser', when='^python@:2.8', type=('build', 'run'))
