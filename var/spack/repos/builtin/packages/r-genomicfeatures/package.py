# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGenomicfeatures(RPackage):
    """Conveniently import and query gene models.

    A set of tools and methods for making and manipulating transcript
    centric annotations. With these tools the user can easily download the
    genomic locations of the transcripts, exons and cds of a given organism,
    from either the UCSC Genome Browser or a BioMart database (more sources
    will be supported in the future). This information is then stored in a
    local database that keeps track of the relationship between transcripts,
    exons, cds and genes. Flexible methods are provided for extracting the
    desired features in a convenient format."""

    bioc = "GenomicFeatures"

    version("1.52.0", commit="207ff08b38421f0394a8f6450e00fb8713ab463c")
    version("1.50.2", commit="4fc9120ceed9ff59f390c8bbdbd79b212ee35b84")
    version("1.48.4", commit="06e37dc1847d49d91391264caec877ed33abf359")
    version("1.48.3", commit="b0ddea0e101e3861928f3ad353348df047d90382")
    version("1.46.4", commit="d3ab6fd069624904ce7fcdf75dad884473f97975")
    version("1.42.1", commit="2e82891974138b0e976799d64a8938f0be61284d")
    version("1.36.4", commit="28082ec465c91ccaec6881ff348b380edac1b555")
    version("1.34.8", commit="c798b3bb111f4de30632303540074ec1875c1387")
    version("1.32.3", commit="80807d88048858846de3750cecb9431a0e5e69e1")
    version("1.30.3", commit="496bbf81beebd7c934b8d3dcea001e3e4a7d7dee")
    version("1.28.5", commit="ba92381ae93cb1392dad5e6acfab8f6c1d744834")

    depends_on("r@3.5.0:", type=("build", "run"), when="@1.48.3:")
    depends_on("r-biocgenerics@0.1.0:", type=("build", "run"))
    depends_on("r-s4vectors@0.9.47:", type=("build", "run"))
    depends_on("r-s4vectors@0.17.29:", type=("build", "run"), when="@1.32.3:")
    depends_on("r-iranges@2.9.19:", type=("build", "run"))
    depends_on("r-iranges@2.11.16:", type=("build", "run"), when="@1.30.3:")
    depends_on("r-iranges@2.13.23:", type=("build", "run"), when="@1.32.3:")
    depends_on("r-genomeinfodb@1.11.4:", type=("build", "run"))
    depends_on("r-genomeinfodb@1.13.1:", type=("build", "run"), when="@1.30.3:")
    depends_on("r-genomeinfodb@1.15.4:", type=("build", "run"), when="@1.32.3:")
    depends_on("r-genomeinfodb@1.25.7:", type=("build", "run"), when="@1.42.1:")
    depends_on("r-genomeinfodb@1.34.1:", type=("build", "run"), when="@1.50.2:")
    depends_on("r-genomeinfodb@1.35.8:", type=("build", "run"), when="@1.52.0:")
    depends_on("r-genomicranges@1.27.6:", type=("build", "run"))
    depends_on("r-genomicranges@1.29.14:", type=("build", "run"), when="@1.30.3:")
    depends_on("r-genomicranges@1.31.17:", type=("build", "run"), when="@1.32.3:")
    depends_on("r-annotationdbi@1.33.15:", type=("build", "run"))
    depends_on("r-annotationdbi@1.41.4:", type=("build", "run"), when="@1.32.3:")
    depends_on("r-dbi", type=("build", "run"))
    depends_on("r-rsqlite@2.0:", type=("build", "run"))
    depends_on("r-rcurl", type=("build", "run"))
    depends_on("r-xvector", type=("build", "run"))
    depends_on("r-xvector@0.19.7:", type=("build", "run"), when="@1.32.3:")
    depends_on("r-biostrings@2.23.3:", type=("build", "run"))
    depends_on("r-biostrings@2.47.6:", type=("build", "run"), when="@1.32.3:")
    depends_on("r-biocio", type=("build", "run"), when="@1.46.4:")
    depends_on("r-rtracklayer@1.29.24:", type=("build", "run"))
    depends_on("r-rtracklayer@1.39.7:", type=("build", "run"), when="@1.32.3:")
    depends_on("r-rtracklayer@1.51.5:", type=("build", "run"), when="@1.46.4:")
    depends_on("r-biomart@2.17.1:", type=("build", "run"))
    depends_on("r-biobase@2.15.1:", type=("build", "run"))

    depends_on("r-rmysql", type=("build", "run"), when="@1.30.3")
