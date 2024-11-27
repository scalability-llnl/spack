# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Unixodbc(AutotoolsPackage):
    """ODBC is an open specification for providing application developers with
    a predictable API with which to access Data Sources. Data Sources include
    SQL Servers and any Data Source with an ODBC Driver."""

    homepage = "https://www.unixodbc.org/"
    url = "https://www.unixodbc.org/unixODBC-2.3.4.tar.gz"

    license("LGPL-2.0-or-later")

    version("2.3.12", sha256="f210501445ce21bf607ba51ef8c125e10e22dffdffec377646462df5f01915ec")
    version("2.3.4", sha256="2e1509a96bb18d248bf08ead0d74804957304ff7c6f8b2e5965309c632421e39")

    depends_on("c", type="build")

    depends_on("iconv")

    @property
    def libs(self):
        return find_libraries("libodbc", root=self.prefix, recursive=True)
