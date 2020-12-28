# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Drill(Package):
    """
    Apache Drill is a distributed MPP query layer that supports SQL and
    alternative query languages against NoSQL and Hadoop data storage
    systems.
    """

    homepage = "http://drill.apache.org/"
    url      = "https://www-eu.apache.org/dist/drill/drill-1.17.0/apache-drill-1.17.0.tar.gz"

    version('1.17.0', sha256='a3d2d544bcc32b915fb53fced0f982670bd6fe2abd764423e566a5f6b54debf1')
    version('1.16.0', sha256='fd195d2b38f393459b37d8f13ac1f36cdbe38495eabb08252da38e3544e87839')
    version('1.15.0', sha256='188c1d0df28e50f0265f4bc3c5871b4e7abc9450a4e5a7dbe7f0b23146bec76b')
    version('1.14.0', sha256='1145bdbb723119f271d32daf4cdd77cdeebe88ddcb7d04facd585b715bb5723b')
    version('1.13.0', sha256='8da6d56f75ae01e0bee6176095d32760e7183dd0200f10ee68b8cd3f882def6a')

    depends_on('java@7:', type='run')

    def install(self, spec, prefix):
        install_tree('.', prefix)
