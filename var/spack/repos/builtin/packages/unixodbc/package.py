# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Unixodbc(AutotoolsPackage):
    """ODBC is an open specification for providing application developers with
    a predictable API with which to access Data Sources. Data Sources include
    SQL Servers and any Data Source with an ODBC Driver."""

    homepage = "http://www.unixodbc.org/"
    url      = "http://www.unixodbc.org/unixODBC-2.3.4.tar.gz"

    version('2.3.4', sha256='2e1509a96bb18d248bf08ead0d74804957304ff7c6f8b2e5965309c632421e39')

    depends_on('iconv')
    depends_on('libtool')
