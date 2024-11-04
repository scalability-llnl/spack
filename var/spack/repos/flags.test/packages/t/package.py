# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class T(Package):
    version("5.0")

    depends_on("u")
    depends_on("x+activatemultiflag")
    depends_on("y cflags='-c1 -c2'")

    depends_on("c", type="build")
