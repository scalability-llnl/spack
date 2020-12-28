# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Filtlong(MakefilePackage):
    """Filtlong is a tool for filtering long reads by quality. It can
    take a set of long reads and produce a smaller, better subset. """

    homepage = "https://github.com/rrwick/Filtlong"
    url      = "https://github.com/rrwick/Filtlong/archive/v0.2.0.tar.gz"

    version('0.2.0', sha256='a4afb925d7ced8d083be12ca58911bb16d5348754e7c2f6431127138338ee02a')
    version('0.1.1', sha256='ddae7a5850efeb64424965a443540b1ced34286fbefad9230ab71f4af314081b')

    depends_on('zlib')

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install_tree('bin', prefix.bin)

        mkdir(prefix.test)
        install_tree('test', prefix.test)
