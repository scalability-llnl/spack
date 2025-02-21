# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPopvar(RPackage):
    """Genomic Breeding Tools: Genetic Variance Prediction and
    Cross-Validation.

    The main attribute of 'PopVar' is the prediction of genetic variance in
    bi-parental populations,  from which the package derives its name. 'PopVar'
    contains a set of functions that use phenotypic and genotypic data from a
    set of candidate parents to 1) predict the mean, genetic variance, and
    superior progeny value of all,  or a defined set of pairwise bi-parental
    crosses, and 2) perform cross-validation to estimate genome-wide prediction
    accuracy of multiple statistical models. More details are available in
    Mohammadi, Tiede, and Smith (2015, <doi:10.2135/cropsci2015.01.0030>).  A
    dataset 'think_barley.rda' is included for reference and examples."""

    cran = "PopVar"

    version("1.3.1", sha256="adb0f6705b7bb984272db31f8ac6612100f7970aa7d0e5cfdef76124dd33ac98")
    version("1.3.0", sha256="3145c41c9aa1588d47aaf76c082e6b1c2fd95cf5014b98bd2867cbf2cec782f9")
    version("1.2.1", sha256="5e3df79634ab63708a431e4b8e6794675972ac6c58d2bc615726aa0f142f5f25")

    depends_on("r@3.1.1:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-bglr", type=("build", "run"))
    depends_on("r-qtl", type=("build", "run"))
    depends_on("r-rrblup", type=("build", "run"))
