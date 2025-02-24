# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPinfsc50(RPackage):
    """Sequence ('FASTA'), Annotation ('GFF') and Variants ('VCF') for 17
    Samples of 'P. Infestans" and 1 'P. Mirabilis'.

    Genomic data for the plant pathogen "Phytophthora infestans." It includes a
    variant file ('VCF'), a sequence file ('FASTA') and an annotation file
    ('GFF'). This package is intended to be used as example data for packages
    that work with genomic data."""

    cran = "pinfsc50"

    maintainers("dorton21")

    license("GPL-2.0-or-later")

    version("1.3.0", sha256="971627cf4567fdb34db26010f2db44cfac5ff07f327d3247e778638cc4e849bf")
    version("1.2.0", sha256="ed1fe214b9261feef8abfbf724c2bd9070d68e99a6ea95208aff2c57bbef8794")

    depends_on("r@3.2.1:", type=("build", "run"))
