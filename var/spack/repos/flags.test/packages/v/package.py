# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class V(Package):
    version("4.1")
    version("4.0")

    depends_on("y")

    depends_on("c", type="build")
