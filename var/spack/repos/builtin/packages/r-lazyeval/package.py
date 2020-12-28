# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLazyeval(RPackage):
    """An alternative approach to non-standard evaluation using formulas.
    Provides a full implementation of LISP style 'quasiquotation', making it
    easier to generate code with other code."""

    homepage = "https://cloud.r-project.org/package=lazyeval"
    url      = "https://cloud.r-project.org/src/contrib/lazyeval_0.2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lazyeval"

    version('0.2.2', sha256='d6904112a21056222cfcd5eb8175a78aa063afe648a562d9c42c6b960a8820d4')
    version('0.2.1', sha256='83b3a43e94c40fe7977e43eb607be0a3cd64c02800eae4f2774e7866d1e93f61')
    version('0.2.0', sha256='13738f55b2044184fe91f53d17516a445dfb508227527921218cda6f01f98dcb')

    depends_on('r@3.1.0:', type=('build', 'run'))
