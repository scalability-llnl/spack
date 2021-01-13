# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertiveDataUk(RPackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://cloud.r-project.org/package=assertive.data.uk"
    url      = "https://cloud.r-project.org/src/contrib/assertive.data.uk_0.0-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/assertive.data.uk"

    version('0.0-2', sha256='ab48dab6977e8f43d6fffb33228d158865f68dde7026d123c693d77339dcf2bb')

    extends('r')
    depends_on('r@3.0.0', type=('build', 'run'))
    depends_on('r-assertive-base@0.0.2:', type=('build', 'run'))
    depends_on('r-assertive-strings', type=('build', 'run'))
