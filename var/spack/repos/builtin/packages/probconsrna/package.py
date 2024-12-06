# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Probconsrna(Package):
    """Experimental version of PROBCONS with parameters estimated via
    unsupervised training on BRAliBASE"""

    homepage = "http://probcons.stanford.edu/"
    url = "http://probcons.stanford.edu/probconsRNA.tar.gz"

    version("2005-6-7", sha256="7fe4494bd423db1d5f33f5ece2c70f9f66a0d9112e28d3eaa7dfdfe7fa66eba8")

    depends_on("cxx", type="build")  # generated

    def install(self, build, prefix):
        mkdirp(prefix.bin)
        install("compare", prefix.bin)
        install("makegnuplot", prefix.bin)
        install("probcons", prefix.bin)
        # needed for tcoffee
        install("probcons", prefix.bin.probconsRNA)
        install("project", prefix.bin)
