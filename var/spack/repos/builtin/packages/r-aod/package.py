# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAod(RPackage):
    """Provides a set of functions to analyse overdispersed counts or
    proportions. Most of the methods are already available elsewhere but are
    scattered in different packages. The proposed functions should be
    considered as complements to more sophisticated methods such as generalized
    estimating equations (GEE) or generalized linear mixed effect models
    (GLMM)."""

    homepage = "https://cloud.r-project.org/package=aod"
    url      = "https://cloud.r-project.org/src/contrib/aod_1.3.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/aod"

    version('1.3.1', sha256='052d8802500fcfdb3b37a8e3e6f3fbd5c3a54e48c3f68122402d2ea3a15403bc')

    depends_on('r@2.10:', type=('build', 'run'))
