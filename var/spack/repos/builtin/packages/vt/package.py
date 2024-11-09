# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Vt(MakefilePackage):
    """A tool set for short variant discovery in genetic sequence data."""

    homepage = "https://genome.sph.umich.edu/wiki/vt"
    url = "https://github.com/atks/vt/archive/0.577.tar.gz"

    version("0.57721", sha256="8f06d464ec5458539cfa30f81a034f47fe7f801146fe8ca80c14a3816b704e17")
    version("0.5772", sha256="b147520478a2f7c536524511e48133d0360e88282c7159821813738ccbda97e7")
    version("0.577", sha256="009e2592e787ab37e471b4e8a66520141bb2791ca78142ca1767d27036f460d0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")

    def install(self, spec, spack):
        mkdirp(prefix.bin)
        install("vt", prefix.bin)
