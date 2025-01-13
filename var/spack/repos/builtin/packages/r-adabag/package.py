# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAdabag(RPackage):
    """Applies Multiclass AdaBoost.M1, SAMME and Bagging.

    It implements Freund and Schapire's Adaboost.M1 algorithm and Breiman's
    Bagging algorithm using classification trees as individual classifiers.
    Once these classifiers have been trained, they can be used to predict on
    new data. Also, cross validation estimation of the error can be done. Since
    version 2.0 the function margins() is available to calculate the margins
    for these classifiers. Also a higher flexibility is achieved giving access
    to the rpart.control() argument of 'rpart'. Four important new features
    were introduced on version 3.0, AdaBoost-SAMME (Zhu et al., 2009) is
    implemented and a new function errorevol() shows the error of the ensembles
    as a function of the number of iterations. In addition, the ensembles can
    be pruned using the option 'newmfinal' in the predict.bagging() and
    predict.boosting() functions and the posterior probability of each class
    for observations can be obtained. Version 3.1 modifies the relative
    importance measure to take into account the gain of the Gini index given by
    a variable in each tree and the weights of these trees. Version 4.0
    includes the margin-based ordered aggregation for Bagging pruning (Guo and
    Boukir, 2013) and a function to auto prune the 'rpart' tree. Moreover,
    three new plots are also available importanceplot(), plot.errorevol() and
    plot.margins(). Version 4.1 allows to predict on unlabeled data. Version
    4.2 includes the parallel computation option for some of the functions."""

    cran = "adabag"

    license("GPL-2.0-or-later")

    version("5.0", sha256="ec58756fda2e64753d21e28d9e27ed34f28020045b199a58dcea06a3e2c3d60e")
    version("4.2", sha256="47019eb8cefc8372996fbb2642f64d4a91d7cedc192690a8d8be6e7e03cd3c81")
    version("4.1", sha256="ff938c36122cdf58a71a59a6bf79a3c7816966ee7cc4907c4a0a3c0732e3d028")

    depends_on("r@4.0.0:", type=("build", "run"), when="@5.0:")
    depends_on("r-rpart", type=("build", "run"))
    depends_on("r-caret", type=("build", "run"))
    depends_on("r-consrank@2.1.3:", type=("build", "run"), when="@5.0:")
    depends_on("r-doparallel", type=("build", "run"))
    depends_on("r-dplyr", type=("build", "run"), when="@5.0:")
    depends_on("r-foreach", type=("build", "run"))
    depends_on("r-tidyr", type=("build", "run"), when="@5.0:")

    depends_on("r-mlbench", type=("build", "run"), when="@:4.1")
