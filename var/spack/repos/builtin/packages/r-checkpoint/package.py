# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCheckpoint(RPackage):
    """The goal of checkpoint is to solve the problem of package
    reproducibility in R. Specifically, checkpoint allows you to
    install packages as they existed on CRAN on a specific snapshot
    date as if you had a CRAN time machine."""

    homepage = "https://cloud.r-project.org/package=checkpoint"
    url      = "https://cloud.r-project.org/src/contrib/checkpoint_0.3.18.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/checkpoint"

    version('0.4.3', sha256='c3e862f89f8838183d6028f7ed13683aec562e6dab77ad4b6a5e24ec653cfb64')
    version('0.3.18', '021d7faeb72c36167951e103b2b065ea')
    version('0.3.15', 'a4aa8320338f1434a330d984e97981ea')

    depends_on('r@3.0.0:')
