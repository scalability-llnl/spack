# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffyrnadegradation(RPackage):
    """Analyze and correct probe positional bias in microarray data due to RNA
    degradation.

    The package helps with the assessment and correction of RNA degradation
    effects in Affymetrix 3' expression arrays. The parameter d gives a
    robust and accurate measure of RNA integrity. The correction removes the
    probe positional bias, and thus improves comparability of samples that
    are affected by RNA degradation."""

    bioc = "AffyRNADegradation"

    version("1.46.0", commit="431ae61c9b3809829697ef71672c57171d93311e")
    version("1.44.0", commit="63881f41fc67cc7322b189446dcffb4e1060e303")
    version("1.42.0", commit="5775f41f538b3c8ee4d07d38cec1b49c548cebe6")
    version("1.40.0", commit="8539a91ee464d692a267bb17c91dc1ef9a231f41")
    version("1.36.0", commit="89662b93076659db2967a526899184c12c156bc5")
    version("1.30.0", commit="620c464fb09248e1c7a122828eab59a4fb778cc1")
    version("1.28.0", commit="aff91d78fa9e76edaa3ef6a9a43b98b86cc44c24")
    version("1.26.0", commit="6ab03ad624701464280bf7dfe345d200e846298a")
    version("1.24.0", commit="1f85f3da4720cef94623828713eb84d8accbcf8a")
    version("1.22.0", commit="0fa78f8286494711a239ded0ba587b0de47c15d3")

    depends_on("r@2.9.0:", type=("build", "run"))
    depends_on("r-affy", type=("build", "run"))
