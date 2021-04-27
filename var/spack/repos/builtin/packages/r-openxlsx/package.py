# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class ROpenxlsx(RPackage):
    """Read, Write and Edit xlsx Files

    Simplifies the creation of Excel .xlsx files by providing a high level
    interface to writing, styling and editing worksheets. Through the use of
    'Rcpp', read/write times are comparable to the 'xlsx' and 'XLConnect'
    packages with the added benefit of removing the dependency on Java."""

    homepage = "https://github.com/awalker89/openxlsx"
    url      = "https://cloud.r-project.org/src/contrib/openxlsx_4.1.0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/openxlsx"

    version('4.2.3', sha256='cdef89d826e50bef772af3e5eae935ca0316626a6e22f55f7631eac733b5e46f')
    version('4.1.0.1', sha256='8b7011debe14714de035ef42797c8caa923162d5dc3cc3c2a299fc10eff3d4d1')

    depends_on('r@3.3.0:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-zip', type=('build', 'run'))
    depends_on('r-stringi', when='@4.2.3:', type=('build', 'run'))
