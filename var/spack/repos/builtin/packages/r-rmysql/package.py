# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRmysql(RPackage):
    """Implements 'DBI' Interface to 'MySQL' and 'MariaDB' Databases."""

    homepage = "https://github.com/rstats-db/rmysql"
    url      = "https://cloud.r-project.org/src/contrib/RMySQL_0.10.9.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RMySQL"

    version('0.10.17', sha256='754df4fce159078c1682ef34fc96aa5ae30981dc91f4f2bada8d1018537255f5')
    version('0.10.9', sha256='41289c743dc8ee2e0dea8b8f291d65f0a7cd11e799b713d94840406ff296fd42')

    depends_on('r-dbi@0.4:', type=('build', 'run'))
    depends_on('mariadb@:5.5')

    depends_on('r@2.8.0:', type=('build', 'run'))
