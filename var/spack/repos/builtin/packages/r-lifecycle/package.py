# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RLifecycle(RPackage):
    """Manage the Life Cycle of your Package Functions

    Manage the life cycle of your exported functions with shared conventions,
    documentation badges, and non-invasive deprecation warnings. The
    'lifecycle' package defines four development stages (experimental,
    maturing, stable, and questioning) and three deprecation stages
    (soft-deprecated, deprecated, and defunct). It makes it easy to insert
    badges corresponding to these stages in your documentation. Usage of
    deprecated functions are signalled with increasing levels of non-invasive
    verbosity."""

    homepage = "https://lifecycle.r-lib.org/"
    url      = "https://cloud.r-project.org/src/contrib/lifecycle_0.2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lifecycle"

    version('0.2.0', sha256='29746e8dee05d4e36f9c612e8c7a903a4f648a36b3b94c9776e518c38a412224')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-rlang@0.4.0:', type=('build', 'run'))
