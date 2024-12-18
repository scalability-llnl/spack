# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Funwave(MakefilePackage):
    """
    What is FUNWAVE-TVD?
    FUNWAVE-TVD is the Total Variation Diminishing (TVD) version of the fully nonlinear Boussinesq
    wave model (FUNWAVE) developed by Shi et al. (2012). The FUNWAVE model was initially developed
    by Kirby et al. (1998) based on Wei et al. (1995). The development of the present version was
    motivated by recent needs for modeling of surfzone--cale optical properties in a Boussinesq
    model framework, and modeling of Tsunami waves in both a global/coastal scale for prediction
    of coastal inundation and a basin scale for wave propagation.
    """

    homepage = "https://fengyanshi.github.io/build/html/index.html"
    git = "https://github.com/fengyanshi/FUNWAVE-TVD"

    maintainers("stevenrbrandt", "fengyanshi")

    version("3.2", tag="v3.2", commit="6e57952d1cef1bb6c0930f07387ed41694bd604b")
    version("3.1", tag="v3.1", commit="d99502f9288380e0c823f7cc619c6c7c1897f2b9")
    version("3.0", tag="v3.0", commit="b569dfe08ab379d7ec375c71304ff95bd6f5ddb6")

    depends_on("fortran", type="build")  # generated

    depends_on("mpi")

    parallel = False

    def build(self, spec, prefix):
        with working_dir("./src"):
            make()

    def install(self, spec, prefix):
        bin = os.path.join(prefix, "bin")
        os.makedirs(bin, exist_ok=True)
        copy("./src/funwave_vessel", os.path.join(bin, "funwave"))

    def edit(self, spec, prefix):
        with working_dir("./src"):
            makefile = FileFilter("Makefile")
            makefile.filter("FLAG_8 = -DCOUPLING", "#FLAG_8 = -DCOUPLING")
