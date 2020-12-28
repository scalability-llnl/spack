# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPysqlite(PythonPackage):
    """Python DB-API module for SQLite 3."""

    homepage = "https://github.com/ghaering/pysqlite"
    url      = "https://pypi.io/packages/source/p/pysqlite/pysqlite-2.8.3.tar.gz"

    version('2.8.3', sha256='17d3335863e8cf8392eea71add33dab3f96d060666fe68ab7382469d307f4490')

    # pysqlite is built into Python3
    depends_on('python@2.7.0:2.7.999', type=('build', 'run'))
    depends_on('sqlite', type=('build', 'run'))
