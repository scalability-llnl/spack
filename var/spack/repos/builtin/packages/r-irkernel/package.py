# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RIrkernel(RPackage):
    """R kernel for Jupyter"""

    homepage = "https://irkernel.github.io/"
    git      = "https://github.com/IRkernel/IRkernel.git"

    version('master', tag='0.7')

    depends_on('r-repr', type=('build', 'run'))
    depends_on('r-irdisplay', type=('build', 'run'))
    depends_on('r-evaluate', type=('build', 'run'))
    depends_on('r-crayon', type=('build', 'run'))
    depends_on('r-pbdzmq', type=('build', 'run'))
    depends_on('r-devtools', type=('build', 'run'))
    depends_on('r-uuid', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
