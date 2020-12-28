# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMitools(RPackage):
    """Tools to perform analyses and combine results from multiple-imputation
    datasets."""

    homepage = "https://cloud.r-project.org/package=mitools"
    url      = "https://cloud.r-project.org/src/contrib/mitools_2.4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mitools"

    version('2.4', sha256='f204f3774e29d79810f579f128de892539518f2cbe6ed237e08c8e7283155d30')

    depends_on('r-dbi', type=('build', 'run'))
