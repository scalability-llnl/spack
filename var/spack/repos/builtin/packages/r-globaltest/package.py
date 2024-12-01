# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGlobaltest(RPackage):
    """Testing Groups of Covariates/Features for Association with a Response
    Variable, with Applications to Gene Set Testing.

    The global test tests groups of covariates (or features) for association
    with a response variable. This package implements the test with diagnostic
    plots and multiple testing utilities, along with several functions to
    facilitate the use of this test for gene set testing of GO and KEGG
    terms."""

    bioc = "globaltest"

    version("5.54.0", commit="bb8bc5f757c8b7c020da31b6a3f500075715ab8e")
    version("5.52.0", commit="a1fc3ad206454d1151bcc940644fd8a5c4164d63")
    version("5.50.0", commit="08612a06eb1cc7381f9bf70f6fe198bb401a21df")
    version("5.48.0", commit="86c2c8f35734dcbc8c8ca791d8a190dc525beac9")
    version("5.44.0", commit="571933d5c779a241740be913ff49ecdd59bcbc45")

    depends_on("r-survival", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-annotate", type=("build", "run"))
