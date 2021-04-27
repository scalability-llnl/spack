# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RBlockmodeling(RPackage):
    """Generalized and Classical Blockmodeling of Valued Networks

    This is primarily meant as an implementation of generalized blockmodeling
    for valued networks."""

    homepage = "https://cloud.r-project.org/package=blockmodeling"
    url      = "https://cloud.r-project.org/src/contrib/blockmodeling_0.3.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/blockmodeling/"

    version('1.0.0', sha256='f10c41fff56dc7dc46dffbceacb8ff905eca06578d610a5a590fb408f0149cfc')
    version('0.3.4', sha256='a269c83669dd5294cff0adddab36bc023db6a276a06b74b1fa94b7e407486987')
    version('0.3.1', sha256='39e8360400cec6baa920d5589d4e779568bdf2954f7331be0e3cadf22a217d31')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-doparallel', when='@:0.3.4', type=('build', 'run'))
    depends_on('r-dorng', when='@:0.3.4', type=('build', 'run'))
    depends_on('r-foreach', when='@:0.3.4', type=('build', 'run'))
