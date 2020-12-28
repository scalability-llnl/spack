# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RReticulate(RPackage):
    """Interface to 'Python' modules, classes, and functions. When calling into
    'Python', R data types are automatically converted to their equivalent
    'Python' types. When values are returned from 'Python' to R they are
    converted back to R types. Compatible with all versions of 'Python' >=
    2.7."""

    homepage = "https://github.com/rstudio/reticulate"
    url      = "https://cloud.r-project.org/src/contrib/reticulate_1.13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/reticulate"

    version('1.15', sha256='47db3e9c9424263ade15287da8e74f6ba261a936b644b197dba6772853b7b50d')
    version('1.13', sha256='adbe41d556b667c4419d563680f8608a56b0f792b8bc427b3bf4c584ff819de3')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-rcpp@0.12.7:', type=('build', 'run', 'link'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-rappdirs', when='@1.15:', type=('build', 'run'))
    depends_on('python@2.7.0:')
