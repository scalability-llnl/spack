# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTopgo(RPackage):
    """Enrichment Analysis for Gene Ontology.

    topGO package provides tools for testing GO terms while accounting for
    the topology of the GO graph. Different test statistics and different
    methods for eliminating local similarities and dependencies between GO
    terms can be implemented and applied."""

    bioc = "topGO"

    version("2.52.0", commit="214db210d1757231eb9b2889288dc385553525cd")
    version("2.50.0", commit="befbff4e67c1b01e23f111d147274641a8b7b0f5")
    version("2.48.0", commit="a47f0079319c7d74db4aeda6399e06f12a34b585")
    version("2.46.0", commit="2bfa9dff41fff261aa6188f8368aebd6e8250b18")
    version("2.42.0", commit="3a33cf53883de45bda506953303e1809ab982adc")
    version("2.36.0", commit="c2f6c187b41c4aa44cc92ac781fdd878491a4019")
    version("2.34.0", commit="44cb5eaba515b365b7b2a8c22df0a45883db6b4d")
    version("2.32.0", commit="78ce3068fc06ae38d55219759fa177e2fcb3f596")
    version("2.30.1", commit="b1469ce1d198ccb73ef79ca22cab81659e16dbaa")
    version("2.28.0", commit="066a975d460046cce33fb27e74e6a0ebc33fd716")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r-biocgenerics@0.13.6:", type=("build", "run"))
    depends_on("r-graph@1.14.0:", type=("build", "run"))
    depends_on("r-biobase@2.0.0:", type=("build", "run"))
    depends_on("r-go-db@2.3.0:", type=("build", "run"))
    depends_on("r-annotationdbi@1.7.19:", type=("build", "run"))
    depends_on("r-sparsem@0.73:", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-matrixstats", type=("build", "run"))
    depends_on("r-dbi", type=("build", "run"))
