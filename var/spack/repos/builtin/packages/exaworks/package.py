# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Exaworks(BundlePackage):
    """
    Virtual package for the Exaworks SDK packages.
    """

    homepage = "https://exaworks.org/"
    maintainers("andre-merzky")

    version("0.1.0")

    depends_on("stc", type=("build", "run"))

    depends_on("flux-core", type=("build", "run"))
    depends_on("flux-sched", type=("build", "run"))

    depends_on("py-parsl", type=("build", "run"))

    depends_on("py-radical-gtod", type=("build", "run"))
    depends_on("py-radical-utils", type=("build", "run"))
    depends_on("py-radical-saga", type=("build", "run"))
    depends_on("py-radical-pilot", type=("build", "run"))
    depends_on("py-radical-entk", type=("build", "run"))

    depends_on("py-psij-python", type=("build", "run"))
