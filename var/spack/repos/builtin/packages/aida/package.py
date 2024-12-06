# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Aida(Package):
    """Abstract Interfaces for Data Analysis"""

    homepage = "https://aida.freehep.org/"
    url = "ftp://ftp.slac.stanford.edu/software/freehep/AIDA/v3.2.1/aida-3.2.1.tar.gz"

    tags = ["hep"]

    version("3.2.1", sha256="c51da83e99c0985a7ef3e8bc5a60c3ae61f3ca603b61100c2438b4cdadd5bb2e")

    def install(self, spec, prefix):
        install_tree("src/cpp", prefix.include)
        install_tree("lib", prefix)
