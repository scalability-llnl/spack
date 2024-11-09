# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Millepede(MakefilePackage):
    """Millepede II is a package for linear least squares fits
    with a large number of parameters. Developed for the
    alignment and calibration of tracking detectors."""

    homepage = "https://gitlab.desy.de/claus.kleinwort/millepede-ii"
    url = "https://gitlab.desy.de/claus.kleinwort/millepede-ii/-/archive/V04-11-01/millepede-ii-V04-11-01.tar.gz"

    parallel = False

    license("LGPL-2.0-only")

    version("04-13-03", sha256="669a6e46a6f02ba3c78b2760e2ffb2c90d25b582ccd1a5c0770eef81c7bcbbe9")
    version("04-11-01", sha256="9869eb84d8d07cecfab15c396f3faa36aef10906e39f8641c48b58e0325b3205")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("zlib-api")

    def install(self, spec, prefix):
        make("install", "PREFIX=" + prefix)
