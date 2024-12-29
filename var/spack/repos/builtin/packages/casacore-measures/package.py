# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class CasacoreMeasures(Package):
    """Install casacore measures tables, and a tool to maintain them."""

    homepage = "https://gitlab.com/dsa-2000/rcp/casacore-measures"
    url = "https://gitlab.com/dsa-2000/rcp/casacore-measures/-/archive/v1.0.0/casacore-measures-v1.0.0.tar.gz"
    git = "https://gitlab.com/dsa-2000/rcp/casacore-measures.git"

    maintainers("mpokorny")

    license("AGPL-3.0-or-later", checked_by="mpokorny")

    version("main", branch="main")
    version("1.0.0", sha256="2bcd891bc0bd67749d93ec5b0fe92d8c1cbb73253465dd0410a3ab5493b3cee5")

    depends_on("wget", type=("build", "run"))

    def install(self, spec, prefix):
        mkdirp(self.prefix.bin)
        install("bin/update_measures", self.prefix.bin)
        mkdirp(self.prefix.share.data)
        update = Executable(self.prefix.bin.update_measures)
        update()
