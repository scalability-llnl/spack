# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySqlalchemyUtils(PythonPackage):
    """Various utility functions and custom data types for SQLAlchemy."""

    homepage = "https://github.com/kvesteri/sqlalchemy-utils"
    url      = "https://pypi.io/packages/source/s/sqlalchemy-utils/SQLAlchemy-Utils-0.36.8.tar.gz"

    version('0.36.8', sha256='fb66e9956e41340011b70b80f898fde6064ec1817af77199ee21ace71d7d6ab0')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-sqlalchemy@1.0:', type=('build', 'run'))
