# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBigmemory(RPackage):
    """Create, store, access, and manipulate massive matrices.
       Matrices are allocated to shared memory and may use
       memory-mapped files. Packages 'biganalytics', 'bigtabulate',
       'synchronicity', and 'bigalgebra' provide advanced functionality."""

    homepage = "https://cloud.r-project.org/web/packages/bigmemory/index.html"
    url      = "https://cloud.r-project.org/src/contrib/bigmemory_4.5.36.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/bigmemory"

    version('4.5.36', sha256='18c67fbe6344b2f8223456c4f19ceebcf6c1166255eab81311001fd67a45ef0e')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-bh', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-bigmemory-sri', type=('build', 'run'))
