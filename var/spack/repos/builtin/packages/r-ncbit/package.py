# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNcbit(RPackage):
    """Retrieve and build NBCI taxonomic data.

    Making NCBI taxonomic data locally available and searchable as an R
    object."""

    cran = "ncbit"

    license("GPL-2.0-or-later")

    version(
        "2013.03.29.1", sha256="847f570c035d849e775c1cb922d2775e6c535971eb4429cf62904319fd126504"
    )
    version(
        "2013.03.29", sha256="4480271f14953615c8ddc2e0666866bb1d0964398ba0fab6cc29046436820738"
    )

    depends_on("r@2.10:", type=("build", "run"))
