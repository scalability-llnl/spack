# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hapdip(Package):
    """The CHM1-NA12878 benchmark for single-sample SNP/INDEL calling from
    WGS Illumina data."""

    homepage = "https://github.com/lh3/hapdip"
    git = "https://github.com/lh3/hapdip.git"

    version("2018.02.20", commit="7c12f684471999a543fdacce972c9c86349758a3")

    depends_on("k8", type="run")

    def install(self, spec, prefix):
        install_tree(".", prefix.bin)
