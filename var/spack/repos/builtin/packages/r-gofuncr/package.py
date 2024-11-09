# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGofuncr(RPackage):
    """Gene ontology enrichment using FUNC.

    GOfuncR performs a gene ontology enrichment analysis based on the
    ontology enrichment software FUNC. GO-annotations are obtained from
    OrganismDb or OrgDb packages ('Homo.sapiens' by default); the GO-graph
    is included in the package and updated regularly (27-Mar-2019). GOfuncR
    provides the standard candidate vs. background enrichment analysis using
    the hypergeometric test, as well as three additional tests: (i) the
    Wilcoxon rank-sum test that is used when genes are ranked, (ii) a
    binomial test that is used when genes are associated with two counts and
    (iii) a Chi-square or Fisher's exact test that is used in cases when
    genes are associated with four counts. To correct for multiple testing
    and interdependency of the tests, family-wise error rates are computed
    based on random permutations of the gene-associated variables. GOfuncR
    also provides tools for exploring the ontology graph and the
    annotations, and options to take gene-length or spatial clustering of
    genes into account. It is also possible to provide custom gene
    coordinates, annotations and ontologies."""

    bioc = "GOfuncR"

    version("1.20.0", commit="2374d68fdd13a72bc8d43cc3b5e6735228996ff1")
    version("1.18.0", commit="49182411e40a5d72abf99a5cca9287f34f870b19")
    version("1.16.0", commit="603fc79e13b58ec4612b6092f37d2450078dbfe1")
    version("1.14.0", commit="b3d445acf95851241d1fdb673d108ee115bdc17b")
    version("1.10.0", commit="51b01a2b9afa03fde2e1628036096cbeafaa2ef4")
    version("1.4.0", commit="2f633dc28e3faeddc5346fcdcadf1c29e3fcf709")
    version("1.2.0", commit="140a3cea4fe34d32fef9be756f85e337ce3deded")
    version("1.0.0", commit="becd4ddde085c5477042adb856e7a4f40dbd648e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r+X", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"))
    depends_on("r-vioplot@0.2:", type=("build", "run"))
    depends_on("r-rcpp@0.11.5:", type=("build", "run"))
    depends_on("r-mapplots@1.5:", type=("build", "run"))
    depends_on("r-gtools@3.5.0:", type=("build", "run"))
    depends_on("r-genomicranges@1.28.4:", type=("build", "run"))
    depends_on("r-iranges", type=("build", "run"), when="@1.2.0:")
    depends_on("r-annotationdbi", type=("build", "run"))
