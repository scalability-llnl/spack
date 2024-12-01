# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Faircmakemodules(CMakePackage):
    """CMake Modules developed in the context of various FAIR (https://www.gsi.de/en/researchaccelerators/fair) projects"""

    homepage = "https://fairrootgroup.github.io/FairCMakeModules/latest/"
    url = "https://github.com/FairRootGroup/FairCMakeModules/archive/refs/tags/v1.0.0.tar.gz"
    git = "https://github.com/FairRootGroup/FairCMakeModules.git"
    maintainers("dennisklein", "ChristianTackeGSI")

    license("LGPL-3.0-or-later")

    version("main", branch="main", get_full_repo=True)
    version("1.0.0", sha256="ec60c31f38050c1173d512c58c684650db66736877c580936f7ecca33eeaf696")

    generator("make", "ninja", default="ninja")

    depends_on("cmake@3.15:", type="build")
