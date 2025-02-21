# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFpc(RPackage):
    """Flexible Procedures for Clustering.

    Various methods for clustering and cluster validation. Fixed point
    clustering. Linear regression clustering. Clustering by  merging Gaussian
    mixture components. Symmetric  and asymmetric discriminant projections for
    visualisation of the  separation of groupings. Cluster validation
    statistics for distance based clustering including corrected Rand index.
    Standardisation of cluster validation statistics by random clusterings and
    comparison between many clustering methods and numbers of clusters based on
    this.   Cluster-wise cluster stability assessment. Methods for estimation
    of  the number of clusters: Calinski-Harabasz, Tibshirani and Walther's
    prediction strength, Fang and Wang's bootstrap stability.
    Gaussian/multinomial mixture fitting for mixed  continuous/categorical
    variables. Variable-wise statistics for cluster interpretation. DBSCAN
    clustering. Interface functions for many  clustering methods implemented in
    R, including estimating the number of clusters with kmeans, pam and clara.
    Modality diagnosis for Gaussian mixtures. For an overview see
    package?fpc."""

    cran = "fpc"

    license("GPL-2.0-or-later")

    version("2.2-12", sha256="555996b4c7e78a28067df25ac657b5065ec79b6b2cd76080382c2d5b43104787")
    version("2.2-10", sha256="99b4548f2eca1a092a31bc2fa4e4bd1d6b50fdfacf3218588c879ceec99147d2")
    version("2.2-9", sha256="29b0006e96c8645645d215d3378551bd6525aaf45abde2d9f12933cf6e75fa38")
    version("2.2-3", sha256="8100a74e6ff96b1cd65fd22494f2d200e54ea5ea533cfca321fa494914bdc3b7")
    version("2.2-2", sha256="b6907019eb161d5c8c814cf02a4663cc8aae6322699932881ce5b02f45ecf8d3")
    version("2.1-10", sha256="5d17c5f475c3f24a4809678cbc6186a357276240cf7fcb00d5670b9e68baa096")

    depends_on("r@2.0.0:", type=("build", "run"))
    depends_on("r@2.0:", type=("build", "run"), when="@2.2-10:")
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-cluster", type=("build", "run"))
    depends_on("r-mclust", type=("build", "run"))
    depends_on("r-flexmix", type=("build", "run"))
    depends_on("r-prabclus", type=("build", "run"))
    depends_on("r-class", type=("build", "run"))
    depends_on("r-diptest", type=("build", "run"))
    depends_on("r-robustbase", type=("build", "run"))
    depends_on("r-kernlab", type=("build", "run"))

    depends_on("r-trimcluster", type=("build", "run"), when="@:2.1-10")
    depends_on("r-mvtnorm", type=("build", "run"), when="@:2.2-2")
