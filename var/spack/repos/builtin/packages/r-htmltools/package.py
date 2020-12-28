# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHtmltools(RPackage):
    """Tools for HTML generation and output."""

    homepage = "https://github.com/rstudio/htmltools"
    url      = "https://cloud.r-project.org/src/contrib/htmltools_0.3.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/htmltools"

    version('0.3.6', sha256='44affb82f9c2fd76c9e2b58f9229adb003217932b68c3fdbf1327c8d74c868a2')
    version('0.3.5', sha256='29fb7e075744bbffdff8ba4fce3860076de66f39a59a100ee4cfb4fc00722b49')

    depends_on('r@2.14.1:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
