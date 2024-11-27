# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class EcpVizSdk(Package):
    """Package that has a dependency with a variant which
    adds a transitive dependency forced to use non default
    values.
    """

    homepage = "https://dev.null"

    version("1.0")

    depends_on("conditional-constrained-dependencies")
