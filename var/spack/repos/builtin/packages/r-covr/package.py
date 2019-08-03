# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCovr(RPackage):
    """Track and report code coverage for your package and (optionally)
    upload the results to a coverage service like 'Codecov'
    <http://codecov.io> or 'Coveralls' <http://coveralls.io>. Code
    coverage is a measure of the amount of code being exercised by a
    set of tests. It is an indirect measure of test quality and
    completeness. This package is compatible with any testing methodology
    or framework and tracks coverage of both R code and compiled
    C/C++/FORTRAN code."""

    homepage = "https://cloud.r-project.org/package=covr"
    url      = "https://cloud.r-project.org/src/contrib/covr_3.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/covr"

    version('3.2.0', sha256='b26135306b1d6b14dd4deb481359dd919a7ca1e802ca5479fed394dcf35f0ef9')
    version('3.0.1', 'f88383f751fe5aa830a2b2e5c14aa66a')

    depends_on('r-digest', when='@3.2.0:', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-rex', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-crayon', type=('build', 'run'))
    depends_on('r-withr@1.0.2:', type=('build', 'run'))
