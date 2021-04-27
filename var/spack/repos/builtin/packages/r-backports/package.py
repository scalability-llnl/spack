# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RBackports(RPackage):
    """Reimplementations of Functions Introduced Since R-3.0.0

    Functions introduced or changed since R v3.0.0 are re-implemented in this
    package. The backports are conditionally exported in order to let R resolve
    the function name to either the implemented backport, or the respective
    base version, if available. Package developers can make use of new
    functions or arguments by selectively importing specific backports to
    support older installations."""

    homepage = "https://cloud.r-project.org/package=backports"
    url      = "https://cloud.r-project.org/src/contrib/backports_1.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/backports"

    version('1.2.1', sha256='a2834bbd57e305e5d8010322f1906ea1789b3b5ba5eca77c5ff4248aceb7c2d5')
    version('1.1.4', sha256='ee4b5efef22fa7ef27d7983ffcd31db52f81e1fbb7189c6e89ee09b69349ff03')
    version('1.1.3', sha256='e41bd146824ec921994f1b176d0e4cca0b36dd3db32ca7a954d872a5ba214cc1')
    version('1.1.1', sha256='494e81a4829339c8f1cc3e015daa807e9138b8e21b929965fc7c00b1abbe8897')
    version('1.1.0', sha256='c5536966ed6ca93f20c9a21d4f569cc1c6865d3352445ea66448f82590349fcd')

    depends_on('r@3.0.0:', type=('build', 'run'))
