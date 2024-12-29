# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PmgrCollective(Package):
    """PMGR_COLLECTIVE provides a scalable network for bootstrapping
    MPI jobs."""

    homepage = "https://www.sourceforge.net/projects/pmgrcollective"
    url = "https://downloads.sourceforge.net/project/pmgrcollective/pmgrcollective/PMGR_COLLECTIVE-1.0/pmgr_collective-1.0.tgz"

    version("1.0", sha256="c8022d1128ce5e8f637166af6e55c13700e665550e468b8cdb1531441c6bb7f5")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        make('PREFIX="' + prefix + '"')
        make('PREFIX="' + prefix + '"', "install")
