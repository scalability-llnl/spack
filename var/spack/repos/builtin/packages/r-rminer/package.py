# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRminer(RPackage):
    """Data Mining Classification and Regression Methods.

    Facilitates the use of data mining algorithms in classification and
    regression (including time series forecasting) tasks by presenting a short
    and coherent set of functions. Versions: 1.4.6 / 1.4.5 / 1.4.4 new
    automated machine learning (AutoML) and ensembles, via improved fit(),
    mining() and mparheuristic() functions, and new categorical preprocessing,
    via improved delevels() function; 1.4.3 new metrics (e.g., macro precision,
    explained variance), new "lssvm" model and improved mparheuristic()
    function; 1.4.2 new "NMAE" metric, "xgboost" and "cv.glmnet" models (16
    classification and 18 regression models); 1.4.1 new tutorial and more
    robust version; 1.4 - new classification and regression models, with a
    total of 14 classification and 15 regression methods, including: Decision
    Trees, Neural Networks, Support Vector Machines, Random Forests, Bagging
    and Boosting; 1.3 and 1.3.1 - new classification and regression metrics;
    1.2 - new input importance methods via improved Importance() function; 1.0
    - first version."""

    cran = "rminer"

    license("GPL-2.0-only")

    version("1.4.6", sha256="1f8bf7b3fbc887fd766568c1ec1f861021c962259354bd8967a61c1d0761cdf7")
    version("1.4.2", sha256="64444dcedcd17f2f26129819d6bd2f84d4bb59c8f65328b6054ef32cb9624fc2")

    depends_on("r-plotrix", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-nnet", type=("build", "run"))
    depends_on("r-kknn", type=("build", "run"))
    depends_on("r-pls", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-mda", type=("build", "run"))
    depends_on("r-rpart", type=("build", "run"))
    depends_on("r-randomforest", type=("build", "run"))
    depends_on("r-adabag", type=("build", "run"))
    depends_on("r-party", type=("build", "run"))
    depends_on("r-cubist", type=("build", "run"))
    depends_on("r-kernlab", type=("build", "run"))
    depends_on("r-e1071", type=("build", "run"))
    depends_on("r-glmnet", type=("build", "run"))
    depends_on("r-xgboost", type=("build", "run"))
