# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCallr(RPackage):
    """It is sometimes useful to perform a computation in a separate R
       process, without affecting the current R process at all. This packages
       does exactly that."""

    homepage = "https://github.com/MangoTheCat/callr"
    url      = "https://cloud.r-project.org/src/contrib/callr_1.0.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/callr/"

    version('3.4.3', sha256='01b7277f20c1d662c6bebbfa2798d179922b36d4148b4298853579aeda0382b5')
    version('3.3.1', sha256='bf60da47357d3336aa395b0c9643235a621763c80d28bc9bb2257767d0a37967')
    version('3.2.0', sha256='4bb47b1018e8eb5c683a86c05d0d9b8b25848db1f1b30e92cfebedc0ce14b0e8')
    version('3.0.0', sha256='e36361086c65660a6ecbbc09b5ecfcddee6b59caf75e983e48b21d3b8defabe7')
    version('1.0.0', sha256='2c56808c723aba2ea8a8b6bbdc9b8332c96f59b119079861dd52f5988c27f715')

    depends_on('r-processx@3.4.0:', type=('build', 'run'), when='@3.0.0:')
    depends_on('r-r6', type=('build', 'run'), when='@3.0.0:')
