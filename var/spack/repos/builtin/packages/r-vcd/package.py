# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVcd(RPackage):
    """Visualization techniques, data sets, summary and inference procedures
    aimed particularly at categorical data. Special emphasis is given to highly
    extensible grid graphics. The package was package was originally inspired
    by the book "Visualizing Categorical Data" by Michael Friendly and is now
    the main support package for a new book, "Discrete Data Analysis with R" by
    Michael Friendly and David Meyer (2015)."""

    homepage = "https://cloud.r-project.org/package=vcd"
    url      = "https://cloud.r-project.org/src/contrib/vcd_1.4-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/vcd"

    version('1.4-4', sha256='a561adf120b5ce41b66e0c0c321542fcddc772eb12b3d7020d86e9cd014ce9d2')
    version('1.4-3', sha256='17ce89927421d9cd01285b6093eeaaecb1e7252388007f66d3b9222e58cc5f15')
    version('1.4-1', sha256='af4c77522efef28271afab7d90679824826132c6bc61abe17df763ed1fc24994')

    depends_on('r@2.4.0:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-colorspace', type=('build', 'run'))
    depends_on('r-lmtest', type=('build', 'run'))
