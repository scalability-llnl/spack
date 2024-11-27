# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Impute2(Package):
    """IMPUTE2 is a genotype imputation and haplotype phasing program based on
    ideas from Howie et al. 2009."""

    homepage = "https://mathgen.stats.ox.ac.uk/impute/impute_v2.html#home"
    url = "https://mathgen.stats.ox.ac.uk/impute/impute_v2.3.2_x86_64_dynamic.tgz"

    version("2.3.2", sha256="da4f64ec75aa2787b8f234e5a7ac4503d464e55ef436a9cd3f4867a10f0c2867")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("impute2", prefix.bin)
