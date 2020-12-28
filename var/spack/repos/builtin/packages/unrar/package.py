# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Unrar(MakefilePackage):
    """RAR archive extraction utility"""

    homepage = "https://www.rarlab.com"
    url = "https://www.rarlab.com/rar/unrarsrc-5.9.4.tar.gz"

    version('5.9.4', sha256='3d010d14223e0c7a385ed740e8f046edcbe885e5c22c5ad5733d009596865300')
    version('5.8.2', sha256='33386623fd3fb153b56292df4a6a69b457e69e1803b6d07b614e5fd22fb33dda')
    version('5.8.1', sha256='035f1f436f0dc2aea09aec146b9cc3e47ca2442f2c62b4ad9374c7c9cc20e632')

    def edit(self, spec, prefix):
        makefile = FileFilter("makefile")
        makefile.filter(
            "LIBFLAGS=-fPIC", "LIBFLAGS={0}".format(self.compiler.cc_pic_flag)
        )
        makefile.filter("DESTDIR=/usr", "DESTDIR={0}".format(self.prefix))

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install('unrar', prefix.bin.unrar)
