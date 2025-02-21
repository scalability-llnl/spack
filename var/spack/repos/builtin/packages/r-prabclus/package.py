# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPrabclus(RPackage):
    """Functions for Clustering of Presence-Absence, Abundance and Multilocus
    Genetic Data.

    Distance-based parametric bootstrap tests for clustering with  spatial
    neighborhood information. Some distance measures,  Clustering of
    presence-absence, abundance and multilocus genetic data  for species
    delimitation, nearest neighbor  based noise detection. Genetic distances
    between communities. Tests whether various distance-based regressions are
    equal. Try package?prabclus for on overview."""

    cran = "prabclus"

    license("GPL-2.0-or-later")

    version("2.3-3", sha256="005d000a9ac357e670de26e5b8fc4ddb1617351275fa43bf6d2e88b8774358c1")
    version("2.3-2", sha256="f421bcbcb557281e0de4a06b15f9a496adb5c640e883c0f7bb12051efc69e441")
    version("2.3-1", sha256="ef3294767d43bc3f72478fdaf0d1f13c8de18881bf9040c9f1add68af808b3c0")
    version("2.2-7.1", sha256="2c5bf3bbb0d225e04c53bb0e11e9c2a6809f0e46d95b8f6dc14b9dd6a2452975")
    version("2.2-6", sha256="41792980e40ba18204fab92d85120dcd468860e2204e52fb42636c6f7aee5a62")

    depends_on("r@2.1.0:", type=("build", "run"))
    depends_on("r@2.10:", type=("build", "run"), when="@2.2-2:")
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-mclust", type=("build", "run"))
