# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RSpam(RPackage):
    """SPArse Matrix

    Set of functions for sparse matrix algebra. Differences with other sparse
    matrix packages are: (1) we only support (essentially) one sparse matrix
    format, (2) based on transparent and simple structure(s), (3) tailored for
    MCMC calculations within G(M)RF. (4) and it is fast and scalable (with the
    extension package spam64). Documentation about 'spam' is provided by
    vignettes included in this package, see also Furrer and Sain (2010)
    <doi:10.18637/jss.v036.i10>; see 'citation("spam")' for details."""

    homepage = "https://www.math.uzh.ch/pages/spam/"
    url      = "https://cloud.r-project.org/src/contrib/spam_2.3-0.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/spam"

    version('2.6-0', sha256='638fdd658e94f7544b46f6b6568b20a9f390bcd703aff572a3a5249fef66be5c')
    version('2.3-0.2', sha256='848fa95c0a71ac82af6344539af7b1c33563c687f06ead42851a68b621fff533')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-dotcall64', type=('build', 'run'))
