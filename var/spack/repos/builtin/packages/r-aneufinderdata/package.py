# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAneufinderdata(RPackage):
    """WGSCS Data for Demonstration Purposes.

       Whole-genome single cell sequencing data for demonstration purposes in
       the AneuFinder package."""

    homepage = "https://bioconductor.org/packages/AneuFinderData"
    git      = "https://git.bioconductor.org/packages/AneuFinderData.git"

    version('1.12.0', commit='7350f38856b6278e07eca141f7f3cb24bc60c3a1')
    version('1.10.0', commit='ef7fc27f9af4f178fa45a21aba30709e1ebde035')
    version('1.8.0', commit='4f00f8d5f2e968fea667a7feafc0a4607d6e0c6e')
    version('1.6.0', commit='8fe5b221619aab75fe84c9094708d240dd1e6730')
    version('1.4.0', commit='55c8807ee4a37a2eb6d0defafaf843f980b22c40')

    depends_on('r@3.3:', type=('build', 'run'))
