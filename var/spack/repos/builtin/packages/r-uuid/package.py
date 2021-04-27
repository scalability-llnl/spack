# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RUuid(RPackage):
    """Tools for Generating and Handling of UUIDs

    Tools for generating and handling of UUIDs (Universally Unique
    Identifiers)."""

    homepage = "http://www.rforge.net/uuid"
    url      = "https://cloud.r-project.org/src/contrib/uuid_0.1-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/uuid"

    version('0.1-4', sha256='98e0249dda17434bfa209c2058e9911e576963d4599be9f7ea946e664f8ca93e')
    version('0.1-2', sha256='dd71704dc336b0857981b92a75ed9877d4ca47780b1682def28839304cd3b1be')

    depends_on('r@2.9.0:', type=('build', 'run'))
