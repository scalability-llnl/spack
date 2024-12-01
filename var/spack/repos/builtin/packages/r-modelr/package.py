# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RModelr(RPackage):
    """Modelling Functions that Work with the Pipe.

    Functions for modelling that help you seamlessly integrate modelling into a
    pipeline of data manipulation and visualisation."""

    cran = "modelr"

    license("GPL-3.0-only")

    version("0.1.11", sha256="94ebd506e9ccf3bf25318be6a182f8f89c3669a77b41864a0b9dbcc1d4337bd3")
    version("0.1.9", sha256="10e9fde89e4695bbab3de2490336f68805cc327807a809982231169963dfa9c9")
    version("0.1.8", sha256="825ba77d95d60cfb94920bec910872ca2ffe7790a44148b2992be2759cb361c4")
    version("0.1.5", sha256="45bbee387c6ba154f9f8642e9f03ea333cce0863c324ff15d23096f33f85ce5a")
    version("0.1.4", sha256="b4da77c1244bbda512ce323751c8338741eeaa195283f172a0feec2917bcfdd9")
    version("0.1.3", sha256="e536b247c17d6cacf10565dd8a1b744efc90a8815c70edd54371e413e6d1b423")
    version("0.1.1", sha256="25b95198d6aa23e28a0bd97dcdc78264ef168ae403928bff01e1ee81ca021ce7")

    depends_on("r@3.1:", type=("build", "run"), when="@:0.1.4")
    depends_on("r@3.2:", type=("build", "run"), when="@0.1.5:")
    depends_on("r-broom", type=("build", "run"))
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-purrr@0.2.2:", type=("build", "run"))
    depends_on("r-rlang@0.2.0:", type=("build", "run"), when="@0.1.3:")
    depends_on("r-rlang@1.0.6:", type=("build", "run"), when="@0.1.11:")
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-tidyr@0.8.0:", type=("build", "run"))
    depends_on("r-tidyselect", type=("build", "run"), when="@0.1.8:")
    depends_on("r-vctrs", type=("build", "run"), when="@0.1.8:")

    depends_on("r-lazyeval@0.2.0:", type=("build", "run"), when="@:0.1.1")
    depends_on("r-dplyr", type=("build", "run"), when="@:0.1.5")
