# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBrew(RPackage):
    """Templating Framework for Report Generation.

    Brew implements a templating framework for mixing text and R code for
    report generation. brew template syntax is similar to PHP, Ruby's erb
    module, Java Server Pages, and Python's psp module."""

    cran = "brew"

    license("GPL-2.0-only")

    version("1.0-10", sha256="4181f7334e032ae0775c5dec49d6137eb25d5430ca3792d321793307b3dda38f")
    version("1.0-8", sha256="11652d5a7042d645cc5be5f9f97ff4d46083cea7d3ad2dd6ad1570b52c097826")
    version("1.0-7", sha256="38b859c1dca63479f6937c593da8f806f2b3279585bb6e20ecff1b898469e76e")
    version("1.0-6", sha256="d70d1a9a01cf4a923b4f11e4374ffd887ad3ff964f35c6f9dc0f29c8d657f0ed")
