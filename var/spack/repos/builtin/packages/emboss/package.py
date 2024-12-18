# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Emboss(AutotoolsPackage):
    """EMBOSS is a free Open Source software analysis package specially
    developed for the needs of the molecular biology (e.g. EMBnet) user
    community"""

    homepage = "https://emboss.sourceforge.net/"
    url = "ftp://emboss.open-bio.org/pub/EMBOSS/EMBOSS-6.6.0.tar.gz"

    license("GPL-2.0-only")

    version("6.6.0", sha256="7184a763d39ad96bb598bfd531628a34aa53e474db9e7cac4416c2a40ab10c6e")

    depends_on("c", type="build")  # generated

    depends_on("libxpm")
    depends_on("libgd")
    depends_on("postgresql")

    @run_after("configure")
    def skip_update_checks(self):
        # Delete $(bindir)/embossupdate to skip update checks
        filter_file("$(bindir)/embossupdate", "", "Makefile", string=True)
