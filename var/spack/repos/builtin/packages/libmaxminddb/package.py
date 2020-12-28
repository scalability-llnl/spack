# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libmaxminddb(AutotoolsPackage):
    """C library for the MaxMind DB file format"""

    homepage = "https://github.com/maxmind/libmaxminddb"
    url      = "https://github.com/maxmind/libmaxminddb/releases/download/1.3.2/libmaxminddb-1.3.2.tar.gz"

    version('1.3.2', sha256='e6f881aa6bd8cfa154a44d965450620df1f714c6dc9dd9971ad98f6e04f6c0f0')

    def configure_args(self):
        args = ['--disable-debug',
                '--disable-dependency-tracking',
                '--disable-silent-rules']
        return args
