# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nicstat(MakefilePackage, SourceforgePackage):
    """
    Nicstat is a Solaris and Linux command-line that prints out network
    statistics for all network interface cards (NICs), including packets,
    kilobytes per second, average packet sizes and more.
    """

    homepage = "https://github.com/scotte/nicstat"
    sourceforge_mirror_path = "nicstat/nicstat-1.95.tar.gz"

    license("Artistic-2.0")

    version("1.95", sha256="c4cc33f8838f4523f27c3d7584eedbe59f4c587f0821612f5ac2201adc18b367")

    depends_on("c", type="build")  # generated

    def edit(self, spec, prefix):
        copy("Makefile.Linux", "makefile")
        filter_file(r"CMODEL =\s+-m32", "", "makefile")
        filter_file("sudo", "", "makefile", string=True)

    def install(self, spec, prefix):
        install_tree(".", prefix)
