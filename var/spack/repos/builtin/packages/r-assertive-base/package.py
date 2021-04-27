# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAssertiveBase(RPackage):
    """assertive.base: A Lightweight Core of the 'assertive' Package

    A minimal set of predicates and assertions used by the assertive package.
    This is mainly for use by other package developers who want to include run-time
    testing features in their own packages. End-users will usually want to use
    assertive directly."""

    homepage = "https://bitbucket.org/richierocks/assertive.base"
    url      = "https://cloud.r-project.org/src/contrib/assertive.base_0.0-7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/assertive.base"

    version('0.0-7', sha256='f02d4eca849f512500abb266a2a751d1fa2cf064f7142e5161a77c20b7f643f7')
    version('0.0-1', sha256='6a5fb06ad912f01cd8aaf2aa7c8ca03b8ebbb1c5eb2be47fa145930f15f4d258')

    depends_on('r@3.0.0:', type=('build', 'run'))
