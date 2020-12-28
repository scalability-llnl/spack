# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDesc(RPackage):
    """desc: Manipulate DESCRIPTION Files"""

    homepage = "https://cloud.r-project.org/package=desc"
    url      = "https://cloud.r-project.org/src/contrib/desc_1.2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/desc/"

    version('1.2.0', sha256='e66fb5d4fc7974bc558abcdc107a1f258c9177a29dcfcf9164bc6b33dd08dae8')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-assertthat', type=('build', 'run'))
    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-crayon', type=('build', 'run'))
    depends_on('r-rprojroot', type=('build', 'run'))
