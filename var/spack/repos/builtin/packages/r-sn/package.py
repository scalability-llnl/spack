# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSn(RPackage):
    """Build and manipulate probability distributions of the skew-normal
    family and some related ones, notably the skew-t family, and provide
    related statistical methods for data fitting and diagnostics, in the
    univariate and the multivariate case."""

    homepage = "https://cloud.r-project.org/package=sn"
    url      = "https://cloud.r-project.org/src/contrib/sn_1.5-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/sn"

    version('1.5-4', sha256='46677ebc109263a68f62b5cf53ec59916cda490e5bc5bbb08276757a677f8674')
    version('1.5-3', sha256='cc21b97ddd674c9b1296260f2a72ffb085cdcb877c8332f0bfa96ff028517183')
    version('1.5-0', sha256='0164f7cffbf9e2a0f03f9bed3b96388b08d8a8ca476bbb686aa88be6b4ec073a')
    version('1.4-0', sha256='d363ae1662bc765e491b98c925901fa9d2d3d6cc760987444db35dbe325aefc0')
    version('1.3-0', sha256='926fc4cde1079860572c2829efc83503f3e1f157b8448b6a40450ca7f5470503')
    version('1.2-4', sha256='a812f754abd1ecdbc9de4e5c8b8f5526c08c06a710d390b1fff2a09328637fb6')
    version('1.2-3', sha256='1af8ced9ed33680d731ab5132be4674d170d76c64a3059ff56c33159d8396154')

    depends_on('r@2.15.3:', type=('build', 'run'))
    depends_on('r-mnormt@1.5-4:', type=('build', 'run'))
    depends_on('r-numderiv', type=('build', 'run'))
