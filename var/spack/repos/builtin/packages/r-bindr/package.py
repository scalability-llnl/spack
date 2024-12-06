# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBindr(RPackage):
    """Parametrized Active Bindings.

    Provides a simple interface for creating active bindings where the bound
    function accepts additional arguments."""

    cran = "bindr"

    license("MIT")

    version("0.1.1", sha256="7c785ca77ceb3ab9282148bcecf64d1857d35f5b800531d49483622fe67505d0")
    version("0.1", sha256="cca166612eeafd6e1c961b34aaf177f9b47f8b4bc37520e277b9920eaa8b2535")
