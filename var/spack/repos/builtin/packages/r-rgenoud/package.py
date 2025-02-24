# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRgenoud(RPackage):
    """R Version of GENetic Optimization Using Derivatives.

    A genetic algorithm plus derivative optimizer."""

    cran = "rgenoud"

    license("GPL-3.0-only")

    version("5.9-0.10", sha256="e644ee640a097ed2d32be03db3603259981656fa459922035a8c531d692acde9")
    version("5.9-0.3", sha256="31560a8dad791f9c47a673e90d397b3fc60da1a58be1ae1486ace90d988eb55f")
    version("5.8-3.0", sha256="9beb11b5edab3ab3aa6001daa39668b240a8e0328be9d55db4e23ff88ce3235d")
    version("5.8-2.0", sha256="106c4f6a6df5159578e929a0141b3cfbaa88141a70703ff59a1fc48a27e2d239")
    version("5.8-1.0", sha256="9deca354be6887f56bf9f4ca9a7291296050e51149ae9a3b757501704126c38a")

    depends_on("r@2.15:", type=("build", "run"))
