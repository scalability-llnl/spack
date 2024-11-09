# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gatepet2stir(QMakePackage):
    """A QT/C++ application to convert GATE geometries to STIR format."""

    homepage = "https://gatepet2stir.sourceforge.io/"
    url = "http://sourceforge.net/projects/gatepet2stir/files/GATE_PET_2_STIR_1_3_2.tar.gz"

    version("1.3.2", sha256="c53b990e47b5856d47466cff62763d0a3bfdc12538b6842cce45271badb7a387")

    depends_on("cxx", type="build")  # generated

    depends_on("gperftools")
    depends_on("ncurses")
    depends_on("qt@:4")
    depends_on("qwt")
    depends_on("root")

    def url_for_version(self, version):
        url = "http://sourceforge.net/projects/gatepet2stir/files/GATE_PET_2_STIR_{0}.tar.gz"
        return url.format(version.underscored)

    def qmake_args(self):
        args = ["QMAKE_LIBS=-ltcmalloc"]
        return args

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("GATE_PET_2_STIR", prefix.bin)
