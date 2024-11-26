# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Y(Package):
    version("2.5")
    version("2.4")
    version("2.3", deprecated=True)

    variant("shared", default=True, description="Build shared libraries")

    depends_on("c", type="build")
