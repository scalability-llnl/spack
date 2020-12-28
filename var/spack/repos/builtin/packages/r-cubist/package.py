# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCubist(RPackage):
    """Regression modeling using rules with added instance-based corrections"""

    homepage = "https://cloud.r-project.org/package=Cubist"
    url      = "https://cloud.r-project.org/src/contrib/Cubist_0.0.19.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Cubist"

    version('0.2.2', sha256='cd3e152cc72ab33f720a8fb6b8b6787171e1c037cfda48f1735ab692ed6d85d4')
    version('0.2.1', sha256='b310c3f166f15fa3e16f8d110d39931b0bb1b0aa8d0c9ac2af5a9a45081588a3')
    version('0.0.19', sha256='101379979acb12a58bcf32a912fef32d497b00263ebea918f2b85a2c32934aae')

    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
