# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RCcp(RPackage):
    """Significance Tests for Canonical Correlation Analysis (CCA).

    Significance tests for canonical correlation analysis, including asymptotic
    tests and a Monte Carlo method"""

    cran = "CCP"

    version("1.2", sha256="7e3906abf51f4c7046730760800711b915f52855fbb2bfd33eca8fa75e70f618")
    version("1.1", sha256="9d21cda05221f1a458fe2938cd5ff0e89711ef058865d25f9894a275c7805d1e")
