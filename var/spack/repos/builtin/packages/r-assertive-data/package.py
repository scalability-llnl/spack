# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertiveData(RPackage):
    """assertive.data: Assertions to Check Properties of Data

    A set of predicates and assertions for checking the
    properties of (country independent) complex data types.
    This is mainly for use by other package developers who want
    to include run-time testing features in their own packages.
    End-users will usually want to use assertive directly."""

    homepage = "https://bitbucket.org/richierocks/assertive.data"
    url      = "https://cloud.r-project.org/src/contrib/assertive.data_0.0-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/assertive.data"

    version('0.0-3', sha256='5a00fb48ad870d9b3c872ce3d6aa20a7948687a980f49fe945b455339e789b01')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-assertive-base@0.0-2:', type=('build', 'run'))
    depends_on('r-assertive-strings', type=('build', 'run'))
