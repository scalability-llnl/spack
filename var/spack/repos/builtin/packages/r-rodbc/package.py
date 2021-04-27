# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRodbc(RPackage):
    """ODBC Database Access

    An ODBC database interface."""

    homepage = "https://cloud.r-project.org/package=RODBC"
    url      = "https://cloud.r-project.org/src/contrib/RODBC_1.3-13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RODBC/"

    version('1.3-17', sha256='469fc835f65c344d5c3eaa097ff278ee8e9f12f845722a9aad340115faa704f7')
    version('1.3-15', sha256='c43e5a2f0aa2f46607e664bfc0bb3caa230bbb779f4ff084e01727642da136e1')
    version('1.3-13', sha256='e8ea7eb77a07be36fc2d824c28bb426334da7484957ffbc719140373adf1667c')

    depends_on('unixodbc')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r@4.0.0:', when='@1.3-17:', type=('build', 'run'))
