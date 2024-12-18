# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class Subread(MakefilePackage):
    """The Subread software package is a tool kit for processing next-gen
    sequencing data."""

    homepage = "https://subread.sourceforge.net/"
    url = "https://sourceforge.net/projects/subread/files/subread-1.5.2/subread-1.5.2-source.tar.gz/download"
    maintainers("snehring")

    license("GPL-3.0-or-later")

    version("2.0.6", sha256="f0fdda6b98634d2946028948c220253e10a0f27c7fa5f24913b65b3ac6cbb045")
    version("2.0.4", sha256="c54b37ed83b34318d8f119b5c02fb9d0a65c811195bcc9e1745df6daf74ca2db")
    version("2.0.2", sha256="0b64bd51f39f8d322c4594697fa5f0f64fbe60283113eadadff9f4268f897079")
    version("2.0.0", sha256="bd7b45f7d8872b0f5db5d23a385059f21d18b49e432bcb6e3e4a879fe51b41a8")
    version("1.6.4", sha256="b7bd0ee3b0942d791aecce6454d2f3271c95a010beeeff2daf1ff71162e43969")
    version("1.6.2", sha256="77b4896c1c242967c5883a06c0a5576a5ff220008a12aa60af9669d2f9a87d7a")
    version("1.6.0", sha256="31251ec4c134e3965d25ca3097890fb37e2c7a4163f6234515534fd325b1002a")
    version("1.5.2", sha256="a8c5f0e09ed3a105f01866517a89084c7302ff70c90ef8714aeaa2eab181a0aa")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api")

    def build(self, spec, prefix):
        plat = sys.platform
        with working_dir("src"):
            if plat.startswith("linux"):
                filter_file("CC_EXEC = gcc", "CC_EXEC = {0}".format(spack_cc), "Makefile.Linux")
                filter_file("-mtune=core2", "", "Makefile.Linux")
                if spec.satisfies("@1.6.2:"):
                    filter_file("-mtune=core2", "", "longread-one/Makefile")
                if spec.satisfies("@1.6.0"):
                    filter_file("-mtune=core2", "", "longread-mapping/Makefile")
                make("-f", "Makefile.Linux")
            elif plat.startswith("darwin"):
                make("-f", "Makefile.MacOS")
            else:
                raise InstallError("The communication mechanism %s is not" "supported" % plat)

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
