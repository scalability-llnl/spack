# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RVctrs(RPackage):
    """Vector Helpers

    Defines new notions of prototype and size that are used to provide tools
    for consistent and well-founded type-coercion and size-recycling, and are
    in turn connected to ideas of type- and size-stability useful for analyzing
    function interfaces."""

    homepage = "https://github.com/r-lib/vctrs"
    url      = "https://github.com/r-lib/vctrs/archive/v0.3.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/vctrs"

    version('0.3.6', sha256='5869a2cc2cb62ccb6f7ff7e8f88c02790d5ea256cccaf51aee56fb28e7ee48ce')
    version('0.3.5', sha256='798dd19809ab99267456ebf488e7aa4e3c03f7f307f5e0abde01dc7ba1cf53ce')
    version('0.2.0', sha256='5bce8f228182ecaa51230d00ad8a018de9cf2579703e82244e0931fe31f20016')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r@3.3:', when='@0.3.5:', type=('build', 'run'))
    depends_on('r-ellipsis@0.2.0:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-rlang@0.4.0:', type=('build', 'run'))
    depends_on('r-rlang@0.4.7:', when='@0.3.5:', type=('build', 'run'))
    depends_on('r-zeallot', when='@:0.2.0', type=('build', 'run'))
