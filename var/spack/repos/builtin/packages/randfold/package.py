# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Randfold(MakefilePackage):
    """Minimum free energy of folding randomization test software"""

    homepage = "http://bioinformatics.psb.ugent.be/supplementary_data/erbon/nov2003/"
    url = "http://bioinformatics.psb.ugent.be/supplementary_data/erbon/nov2003/downloads/randfold-2.0.1.tar.gz"

    license("GPL-2.0-only")

    version("2.0.1", sha256="b286145deb9ac6197062d98e209da095f00c45a5a615616bcf2b2a6609ed113f")

    depends_on("c", type="build")  # generated

    depends_on("squid")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("randfold", prefix.bin)
