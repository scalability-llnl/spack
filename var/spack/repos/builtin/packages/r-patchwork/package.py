# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RPatchwork(RPackage):
    """The Composer of Plots

    The 'ggplot2' package provides a strong API for sequentially building up a
    plot, but does not concern itself with composition of multiple plots.
    'patchwork' is a package that expands the API to allow for arbitrarily
    complex composition of plots by, among others, providing mathematical
    operators for combining multiple plots. Other packages that try to address
    this need (but with a different approach) are 'gridExtra' and 'cowplot'."""

    homepage = "https://patchwork.data-imaginist.com/"
    url      = "https://cloud.r-project.org/src/contrib/patchwork_1.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/patchwork"

    version('1.1.1', sha256='cf0d7d9f92945729b499d6e343441c55007d5b371206d5389b9e5154dc7cf481')

    depends_on('r-ggplot2@3.0.0:', type=('build', 'run'))
    depends_on('r-gtable', type=('build', 'run'))
