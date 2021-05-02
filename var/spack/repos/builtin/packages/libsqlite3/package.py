# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libsqlite3(AutotoolsPackage):
    """sqlite3 is a slick embedded SQL server written in C."""

    homepage = "https://github.com/LuaDist/libsqlite3"
    url      = "https://github.com/LuaDist/libsqlite3/archive/3.7.7.1.tar.gz"

    version('3.7.7.1', sha256='b1eb700a46a7429a1a587fadd31e8ef5a3fd84bb6a75b898715baf71fedc412e')
