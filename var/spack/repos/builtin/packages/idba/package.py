# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Idba(AutotoolsPackage):
    """IDBA is a practical iterative De Bruijn Graph De Novo Assembler for
    sequence assembly in bioinfomatics."""

    homepage = "https://i.cs.hku.hk/~alse/hkubrg/projects/idba/"
    url = "https://github.com/loneknightpy/idba/archive/1.1.3.tar.gz"

    version("1.1.3", sha256="6b1746a29884f4fa17b110d94d9ead677ab5557c084a93b16b6a043dbb148709")

    depends_on("cxx", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
