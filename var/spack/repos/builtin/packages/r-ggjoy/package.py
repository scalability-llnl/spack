# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgjoy(RPackage):
    """Joyplots in 'ggplot2'.

    Joyplots provide a convenient way of visualizing changes in
    distributions over time or space."""

    cran = "ggjoy"

    license("GPL-2.0-only OR custom")

    version("0.4.1", sha256="d2f778bc40203d7fbb7c81b40beed8614c36ea10448e911663cc6109aa685504")
    version("0.4.0", sha256="cb9ef790921ffcd3cfb6a55b409d17ccae9e8f5fdd2a28e55ea2ccfa8efd44e8")
    version("0.3.0", sha256="bb6d5172deda6cc54d2647644c1056944bc886d48fe1f11a23afd518eaf5cc97")
    version("0.2.0", sha256="27c28e9b3aa333ee6f518ee5c1cf6533fdaefa4e205396cd4636bcf0d193e6a2")

    depends_on("r@3.2:", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-ggridges@0.4.0:", type=("build", "run"))
