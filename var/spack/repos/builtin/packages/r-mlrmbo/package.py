# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMlrmbo(RPackage):
    """Bayesian Optimization and Model-Based Optimization of Expensive
    Black-Box Functions.

    Flexible and comprehensive R toolbox for model-based optimization ('MBO'),
    also known as Bayesian optimization. It is designed for both single- and
    multi-objective optimization with mixed continuous, categorical and
    conditional parameters. The machine learning toolbox 'mlr' provide dozens
    of regression learners to model the performance of the target algorithm
    with respect to the parameter settings. It provides many different infill
    criteria to guide the search process. Additional features include
    multi-point batch proposal, parallel execution as well as visualization and
    sophisticated logging mechanisms, which is especially useful for teaching
    and understanding of algorithm behavior.  'mlrMBO' is implemented in a
    modular fashion, such that single components can be easily replaced or
    adapted by the user for specific use cases."""

    cran = "mlrMBO"

    version("1.1.5.1", sha256="0cf26e5e9b180d15b932541cf081a552703a60edf762aafca9933c24ea91dc99")
    version("1.1.5", sha256="7ab9d108ad06f6c5c480fa4beca69e09ac89bb162ae6c85fe7d6d25c41f359b8")
    version("1.1.2", sha256="8e84caaa5d5d443d7019128f88ebb212fb095870b3a128697c9b64fe988f3efe")
    version("1.1.1", sha256="e87d9912a9b4a968364584205b8ef6f7fea0b5aa043c8d31331a7b7be02dd7e4")
    version("1.1.0", sha256="6ae82731a566333f06085ea2ce23ff2a1007029db46eea57d06194850350a8a0")

    depends_on("c", type="build")  # generated

    depends_on("r+X", type=("build", "run"))
    depends_on("r-mlr@2.10:", type=("build", "run"))
    depends_on("r-paramhelpers@1.10:", type=("build", "run"))
    depends_on("r-smoof@1.5.1:", type=("build", "run"))
    depends_on("r-backports@1.1.0:", type=("build", "run"))
    depends_on("r-bbmisc@1.11:", type=("build", "run"))
    depends_on("r-checkmate@1.8.2:", type=("build", "run"))
    depends_on("r-data-table", type=("build", "run"))
    depends_on("r-lhs", type=("build", "run"))
    depends_on("r-parallelmap@1.3:", type=("build", "run"))
