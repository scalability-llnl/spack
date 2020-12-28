# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDbi(RPackage):
    """A database interface definition for communication between R and
    relational database management systems. All classes in this package are
    virtual and need to be extended by the various R/DBMS implementations."""

    homepage = "http://rstats-db.github.io/DBI"
    url      = "https://cloud.r-project.org/src/contrib/DBI_0.7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/DBI"

    version('1.1.0', sha256='a96db7fa39a58f1ed34c6e78d8f5f7e4cf0882afb301323b5c6975d6729203e4')
    version('1.0.0', sha256='ff16f118eb3f759183441835e932b87358dd80ab9800ce576a8f3df1b6f01cf5')
    version('0.4-1', sha256='eff14a9af4975f23f8e1f4347d82c33c32c0b4f4f3e11370c582a89aeb8ac68e')
    version('0.7', sha256='2557d5d59a45620ec9de340c2c25eec4cc478d3fc3f8b87979cf337c5bcfde11')

    depends_on('r@3.0.0:', type=('build', 'run'))
