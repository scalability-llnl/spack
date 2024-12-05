# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Epsic(AutotoolsPackage):
    """Electromagnetic Polarization Simulation in C++."""

    homepage = "https://github.com/straten/epsic"
    git = "https://github.com/straten/epsic.git"

    version("develop")

    # Version to match
    # https://github.com/lwa-project/pulsar/blob/master/SoftwareStack.md
    # last updated 10/17/2020
    version("LWA-10-17-2020", commit="5315cc634f6539ea0a34e403e492472b97e0f086")

    depends_on("cxx", type="build")  # generated
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("yacc", when="@develop", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    configure_directory = "src"
