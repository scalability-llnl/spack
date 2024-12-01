# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libisal(AutotoolsPackage):
    """ISA-L is a collection of optimized low-level functions targeting
    storage applications."""

    homepage = "https://github.com/intel/isa-l"
    url = "https://github.com/intel/isa-l/archive/v2.29.0.tar.gz"

    license("BSD-3-Clause")

    version("2.31.0", sha256="e218b7b2e241cfb8e8b68f54a6e5eed80968cc387c4b1af03708b54e9fb236f1")
    version("2.29.0", sha256="832d9747ef3f0c8c05d39e3d7fd6ee5299a844e1ee7382fc8c8b52a268f36eda")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("nasm", type="build")

    def autoreconf(self, spec, prefix):
        autogen = Executable("./autogen.sh")
        autogen()
