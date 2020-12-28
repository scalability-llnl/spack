# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCfgv(PythonPackage):
    """Validate configuration and produce human readable error messages."""

    homepage = "https://github.com/asottile/cfgv/"
    url      = "https://pypi.io/packages/source/c/cfgv/cfgv-2.0.1.tar.gz"

    version('2.0.1', sha256='edb387943b665bf9c434f717bf630fa78aecd53d5900d2e05da6ad6048553144')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-six',        type=('build', 'run'))
