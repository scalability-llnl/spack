# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class U(Package):
    version("6.0")

    depends_on("y cflags='-e1 -e2'")

    depends_on("c", type="build")
