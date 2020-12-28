# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSnpstats(RPackage):
    """SnpMatrix and XSnpMatrix classes and methods.

       Classes and statistical methods for large SNP association studies. This
       extends the earlier snpMatrix package, allowing for uncertainty in
       genotypes."""

    homepage = "https://bioconductor.org/packages/snpStats"
    git      = "https://git.bioconductor.org/packages/snpStats.git"

    version('1.34.0', commit='e31cdfb18a9e12d70d6a3e8e6fbf7cf8faa3ea5b')
    version('1.32.0', commit='7c31158183b4e39da6dc30c7da275acc36b2e32f')
    version('1.30.0', commit='0dc1e4246f015feaf2579d60268b10ab5149ce09')
    version('1.28.0', commit='8df9f4188f720dfbb4f4f4ec255cd2e22f3f4426')
    version('1.26.0', commit='7c9b3304073e0556d694a8531882b349822fdda8')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-zlibbioc', type=('build', 'run'))
