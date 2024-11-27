# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFlexmix(RPackage):
    """Flexible Mixture Modeling.

    A general framework for finite mixtures of regression models using the EM
    algorithm is implemented. The E-step and all data handling are provided,
    while the M-step can be supplied by the user to easily define new models.
    Existing drivers implement mixtures of standard linear models, generalized
    linear models and model-based clustering."""

    cran = "flexmix"

    license("GPL-2.0-or-later")

    version("2.3-19", sha256="adf5a40cbb6d45e3652c1666cb3ccdb9654e501fd685c091cad0686e62bc12e9")
    version("2.3-18", sha256="462201ef49088845c83083e4ed6725cf069aafb12a814041618aaf09ebd69b51")
    version("2.3-17", sha256="36019b7833032409ac61720dd625fa5a581a1d8bcba9045b04979c90907b5649")
    version("2.3-15", sha256="ba444c0bfe33ab87d440ab590c06b03605710acd75811c1622253171bb123f43")
    version("2.3-14", sha256="837c7f175a211b3c484b2c7b81ec9729889a614c5c6e7d70c95a2c1d60ff846a")

    depends_on("r@2.15.0:", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-modeltools@0.2-16:", type=("build", "run"))
    depends_on("r-nnet", type=("build", "run"))
