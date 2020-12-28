# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVarselrf(RPackage):
    """Variable selection from random forests using both backwards variable
    elimination (for the selection of small sets of non-redundant variables)
    and selection based on the importance spectrum (somewhat similar to scree
    plots; for the selection of large, potentially highly-correlated variables)
    . Main applications in high-dimensional data (e.g., microarray data,
    and other genomics and proteomics applications)."""

    homepage = "http://ligarto.org/rdiaz/Software/Software.html"
    url      = "https://cloud.r-project.org/src/contrib/varSelRF_0.7-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/varSelRF"

    version('0.7-8', sha256='719487fb560cb4733816bafe4cbc958a132674825e3b9d4f82ce8f2003cd8940')

    depends_on('r@2.0.0:', type=('build', 'run'))
    depends_on('r-randomforest', type=('build', 'run'))
