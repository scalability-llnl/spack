# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Qgraf(Package):
    """Qgraf is a computer program that generates Feynman diagrams
    for various types of QFT models"""

    homepage = "http://cfif.ist.utl.pt/~paulo/qgraf.html"
    url = "http://anonymous:anonymous@qgraf.tecnico.ulisboa.pt/v3.4/qgraf-3.4.2.tgz"

    tags = ["hep"]

    version("3.4.2", sha256="cfc029fb871c78943865ef8b51ebcd3cd4428448b8816714b049669dfdeab8aa")

    depends_on("fortran", type="build")  # generated

    def install(self, spec, prefix):
        fortran = Executable(spack_fc)
        fortran("qgraf-{0}.f".format(self.spec.version), "-o", "qgraf")
        mkdirp(prefix.bin)
        install("./qgraf", prefix.bin)
