# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAlembic(PythonPackage):
    """Alembic is a database migrations tool."""

    homepage = "https://pypi.org/project/alembic/"
    url      = "https://pypi.io/packages/source/a/alembic/alembic-1.0.7.tar.gz"

    version('1.0.7', sha256='16505782b229007ae905ef9e0ae6e880fddafa406f086ac7d442c1aaf712f8c2')

    depends_on('py-setuptools', type='build')
    depends_on('py-sqlalchemy@1.1.0:', type=('build', 'run'))
    depends_on('py-mako', type=('build', 'run'))
    depends_on('py-python-dateutil', type=('build', 'run'))
    depends_on('py-python-editor@0.3:', type=('build', 'run'))
