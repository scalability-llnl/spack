# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGlobaloptions(RPackage):
    """It provides more controls on the option values such as validation and
       filtering on the values, making options invisible or private."""

    homepage = "https://cloud.r-project.org/package=GlobalOptions"
    url      = "https://cloud.r-project.org/src/contrib/GlobalOptions_0.0.12.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/GlobalOptions"

    version('0.1.0', sha256='567a0a51f6b7b14127302f00e6e4944befd4964c069f96a9e61256e8c3c79ef2')
    version('0.0.12', sha256='c09da3f9b1646d0f815056cdbeb5fff7dda29f7dd8742d245f5f6dc7066077a9')

    depends_on('r@2.10:', when='@:0.0.12', type=('build', 'run'))
    depends_on('r@3.3.0:', when='@0.0.13:', type=('build', 'run'))
