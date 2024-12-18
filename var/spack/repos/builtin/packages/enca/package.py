# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Enca(AutotoolsPackage):
    """Extremely Naive Charset Analyser."""

    homepage = "https://cihar.com/software/enca/"
    url = "https://github.com/nijel/enca/archive/1.19.tar.gz"

    license("GPL-2.0-only")

    version("1.19", sha256="c4fd9a3d7c086803138842b18eed6072ec8810859b0e1ef091f1e1138d283f25")
    version("1.18", sha256="b87c8d1bffc7d06ba74f82ae86eb21a921e94629203b2a971c966064c7eadab2")
    version("1.17", sha256="b20372440c500e6463bd61dab0e68131cdfe857c6b7ca139b5c6cbf01e24fdc7")
    version("1.16", sha256="14457b185c77b947ca2f8e09a2c3ec66940d97a2ccea28b8e61a6e0f3a0033f6")

    depends_on("c", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")
