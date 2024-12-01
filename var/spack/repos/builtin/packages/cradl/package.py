# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cradl(Package):
    """The CRADL proxy application captured performance metrics during
    inference on data from multiphysics codes, specifically ALE
    hydrodynamics codes."""

    homepage = "https://github.com/LLNL/CRADL"
    url = "https://github.com/LLNL/CRADL/archive/master.zip"
    git = "https://github.com/LLNL/CRADL.git"

    tags = ["proxy-app"]

    license("BSD-3-Clause")

    version("master", branch="master")

    depends_on("py-pandas")
    depends_on("py-torch")
    depends_on("py-torchvision")
    depends_on("py-apex")
    depends_on("py-gputil")
    depends_on("py-matplotlib")
    depends_on("py-mpi4py")

    def install(self, spec, prefix):
        # Mostly  about providing an environment so just copy everything
        install_tree(".", prefix)
