# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNfactors(RPackage):
    """Parallel Analysis and Other Non Graphical Solutions to the Cattell Scree
    Test.

    Indices, heuristics and strategies to help determine the number of
    factors/components to retain: 1. Acceleration factor (af with or without
    Parallel Analysis); 2. Optimal Coordinates (noc with or without Parallel
    Analysis); 3. Parallel analysis (components, factors and bootstrap); 4.
    lambda > mean(lambda) (Kaiser, CFA and related); 5. Cattell-Nelson-Gorsuch
    (CNG); 6. Zoski and Jurs multiple regression (b, t and p); 7. Zoski and
    Jurs standard error of the regression coeffcient (sescree); 8. Nelson R2;
    9. Bartlett khi-2; 10.  Anderson khi-2; 11. Lawley khi-2 and 12.
    Bentler-Yuan khi-2."""

    cran = "nFactors"

    version("2.4.1.1", sha256="bb376621d870c52ac9c29bfe4d22f71ffc5a9885a3996be3e032fe30c46cfe21")
    version("2.4.1", sha256="028eb4ebd42a29f6a01297d728c7e353cabb37b46701639b4a52f17ba25a3eb6")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-psych", type=("build", "run"))
