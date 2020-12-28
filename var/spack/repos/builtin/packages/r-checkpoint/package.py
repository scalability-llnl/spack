# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCheckpoint(RPackage):
    """The goal of checkpoint is to solve the problem of package
    reproducibility in R. Specifically, checkpoint allows you to
    install packages as they existed on CRAN on a specific snapshot
    date as if you had a CRAN time machine."""

    homepage = "https://cloud.r-project.org/package=checkpoint"
    url      = "https://cloud.r-project.org/src/contrib/checkpoint_0.4.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/checkpoint"

    version('0.4.6', sha256='fd1a5edb5cb1a40d7ed26bb196de566110fe2ef62e70b4e947c003576a03ebb2')
    version('0.4.3', sha256='c3e862f89f8838183d6028f7ed13683aec562e6dab77ad4b6a5e24ec653cfb64')
    version('0.3.15', sha256='09f1feeb2b5b8b409a2e16a9185827b8da5e555f1aa84442a287f15e452beed7')

    depends_on('r@3.0.0:', type=('build', 'run'))
