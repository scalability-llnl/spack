# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class X(Package):
    version("1.1")
    version("1.0")
    version("0.9")

    variant("shared", default=True, description="Build shared libraries")

    depends_on("y")
    depends_on("c", type="build")
