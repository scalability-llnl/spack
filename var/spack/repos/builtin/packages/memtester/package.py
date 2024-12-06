# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Memtester(MakefilePackage):
    """A userspace utility for testing the memory subsystem for faults."""

    homepage = "http://pyropus.ca/software/memtester/"
    url = "http://pyropus.ca/software/memtester/old-versions/memtester-4.3.0.tar.gz"

    license("GPL-2.0-or-later")

    version("4.3.0", sha256="f9dfe2fd737c38fad6535bbab327da9a21f7ce4ea6f18c7b3339adef6bf5fd88")
    version("4.2.2", sha256="a494569d58d642c796332a1b7f3b4b86845b52da66c15c96fbeecd74e48dae8e")
    version("4.2.1", sha256="3433e1c757e56457610f5a97bf1a2d612c609290eba5183dd273e070134a21d2")
    version("4.2.0", sha256="cb9d5437a0c429d18500bddef93084bb2fead0d5ccfedfd00ee28ff118e52695")
    version("4.1.3", sha256="ac56f0b6d6d6e58bcf2a3fa7f2c9b29894f5177871f21115a1906c535106acf6")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("INSTALLPATH\t= /usr/local", "INSTALLPATH\t= {0}".format(self.prefix))
