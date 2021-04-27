# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RLocfit(RPackage):
    """Local regression, likelihood and density estimation

    Local regression, likelihood and density estimation methods as described in
    the 1999 book by Loader.
    """

    homepage = "https://cloud.r-project.org/package=locfit"
    url      = "https://cloud.r-project.org/src/contrib/locfit_1.5-9.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/locfit"

    version('1.5-9.4', sha256='d9d3665c5f3d49f698fb4675daf40a0550601e86db3dc00f296413ceb1099ced')
    version('1.5-9.1', sha256='f524148fdb29aac3a178618f88718d3d4ac91283014091aa11a01f1c70cd4e51')

    depends_on('r@2.0.1:', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@1.5-9.4:', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
