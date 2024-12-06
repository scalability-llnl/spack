# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Shapeit(Package):
    """SHAPEIT is a fast and accurate method for estimation of haplotypes (aka
    phasing) from genotype or sequencing data."""

    homepage = "https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.html"
    url = "https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.v2.r837.GLIBCv2.12.Linux.dynamic.tgz"

    version("2.837", sha256="ec2ce728dd754452423ff5a8f7ed39c1c1218a11cedb93fab0c18428e3211874")

    def url_for_version(self, version):
        url = "https://mathgen.stats.ox.ac.uk/genetics_software/shapeit/shapeit.v{0}.r{1}.GLIBCv2.12.Linux.dynamic.tgz"
        return url.format(version[0], version[1])

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        with working_dir("bin"):
            install("shapeit", prefix.bin)
