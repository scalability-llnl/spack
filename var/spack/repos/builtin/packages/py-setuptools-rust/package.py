# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PySetuptoolsRust(PythonPackage):
    """Setuptools rust extension plugin."""

    homepage = "https://github.com/PyO3/setuptools-rust"
    url      = "https://github.com/PyO3/setuptools-rust/archive/v0.10.6.tar.gz"

    version('0.10.6', sha256='1446d3985e4aaf4cc679fda8a48a73ac1390b627c8ae1bebe7d9e08bb3b33769')

    depends_on('py-setuptools', type='build')
    depends_on('py-semantic-version@2.6.0:', type=('build', 'run'))
    depends_on('py-toml@0.9.0:', type=('build', 'run'))
    depends_on('rust', type='run')
