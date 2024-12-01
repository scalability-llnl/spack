# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RClipr(RPackage):
    """Read and Write from the System Clipboard.

    Simple utility functions to read from and write to the Windows, OS X, and
    X11 clipboards."""

    cran = "clipr"

    license("GPL-3.0-only")

    version("0.8.0", sha256="32c2931992fbec9c31b71de3e27059f1cbb45b4b1f45fd42e0e8dbcec6de3be9")
    version("0.7.1", sha256="ffad477b07847e3b68f7e4406bbd323025a8dae7e3c768943d4d307ee3248afb")
    version("0.7.0", sha256="03a4e4b72ec63bd08b53fe62673ffc19a004cc846957a335be2b30d046b8c2e2")
    version("0.5.0", sha256="fd303f8b7f29badcdf490bb2d579acdfc4f4e1aa9c90ac77ab9d05ce3d053dbf")
    version("0.4.0", sha256="44a2f1ab4fde53e4fe81cf5800aa6ad45b72b5da93d6fe4d3661d7397220e8af")

    depends_on("r+X")
    depends_on("xclip")
