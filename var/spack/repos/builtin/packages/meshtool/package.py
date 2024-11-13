# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Meshtool(MakefilePackage):
    """Meshtool - A mesh manipulation utility"""

    homepage = "https://bitbucket.org/aneic/meshtool/"
    git = "https://bitbucket.org/aneic/meshtool.git"

    maintainers("MarieHouillon")

    version("master", branch="master", preferred=True)
    # Version to use with openCARP releases
    # It is possible that different openCARP releases rely on the same
    # meshtool version
    version("oc16.0", commit="867431d6bde35ad41104f611aa57130ef58cfb79")
    version("oc15.0", commit="867431d6bde35ad41104f611aa57130ef58cfb79")
    version("oc13.0", commit="867431d6bde35ad41104f611aa57130ef58cfb79")
    version("oc12.0", commit="867431d6bde35ad41104f611aa57130ef58cfb79")
    version("oc11.0", commit="867431d6bde35ad41104f611aa57130ef58cfb79")
    version("oc10.0", commit="6c5cfbd067120901f15a04bf63beec409bda6dc9")
    version("oc9.0", commit="6c5cfbd067120901f15a04bf63beec409bda6dc9")
    version("oc8.2", commit="6c5cfbd067120901f15a04bf63beec409bda6dc9")
    version("oc8.1", commit="6c5cfbd067120901f15a04bf63beec409bda6dc9")
    version("oc7.0", commit="6c5cfbd067120901f15a04bf63beec409bda6dc9")

    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("meshtool", prefix.bin)
