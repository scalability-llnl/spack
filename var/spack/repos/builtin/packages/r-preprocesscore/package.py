# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPreprocesscore(RPackage):
    """A collection of pre-processing functions.

       A library of core preprocessing routines."""

    homepage = "https://bioconductor.org/packages/preprocessCore"
    git      = "https://git.bioconductor.org/packages/preprocessCore.git"

    version('1.46.0', commit='8cfc3938c1b08424587f437ed6cd2ec43512500e')
    version('1.44.0', commit='dc1dc61fc562aaff3fd9b11ab0d48c2d6b3a5b81')
    version('1.42.0', commit='2e3a8baeacfaa1526d51252642772ea951015bba')
    version('1.40.0', commit='969bb0e5cbd63d569502ae4e6eaadc1e216646dd')
    version('1.38.1', commit='c58cb4c720eda0f1c733b989b14912093a7c5fbc')
