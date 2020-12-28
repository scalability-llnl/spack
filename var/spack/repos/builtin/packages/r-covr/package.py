# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


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

    version('3.5.0', sha256='cb919912018130164a40803ac573a37dde2186678c058c03c6303d79604979df')
    version('3.3.0', sha256='c0aa0bd7b2dc05effdc2367c59d45294f46858930d1b14efb393b205021fc65a')
    version('3.2.1', sha256='ea90daa48011e4ac4431ae47ee02fad98f54b529fc3900281cbeef7a2edef0a0')
    version('3.2.0', sha256='b26135306b1d6b14dd4deb481359dd919a7ca1e802ca5479fed394dcf35f0ef9')
    version('3.0.1', sha256='66b799fd03cb83a9ab382d9cf4ff40603d1e3f3a89905a3174546b0c63e8d184')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-digest', when='@3.2.0:', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-rex', type=('build', 'run'))
    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-crayon', type=('build', 'run'))
    depends_on('r-withr@1.0.2:', type=('build', 'run'))
    depends_on('r-yaml', when='@3.3.0:', type=('build', 'run'))
